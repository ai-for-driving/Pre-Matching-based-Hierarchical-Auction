from typing import List
import numpy as np
import sys
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")
from Algorithms.PMHA.player import auction_buyer, auction_seller
from Objects.task_object import task
from Objects.vehicle_object import vehicle
from Objects.edge_node_object import edge_node
from Objects.cloud_server_object import cloud_server
from Strategy.strategy import action
from Utilities.conversion import cover_MB_to_bit, cover_GHz_to_Hz

def init_buyers_and_sellers_at_edge_cloud_auction(
    client_vehicles: List[vehicle],
    edge_nodes: List[edge_node],
    cloud: cloud_server,
    tasks: List[task],
    offloading_decision: np.ndarray,  # client vehicle index * (1 + server_vehicle_number + edge_node_number + cloud_node_number)
    action: action,
    now: int,
) -> tuple[action, List[auction_buyer], List[auction_seller]]:
    buyers = list()
    sellers = list()
    output_action = action
    for edge_node_index in range(len(edge_nodes)):
        edge_node = edge_nodes[edge_node_index]
        tasks_tuple_list = list()
        for client_vehicle_index in range(len(client_vehicles)):
            if offloading_decision[client_vehicle_index][edge_node_index] == 1:
                tasks_list = client_vehicles[client_vehicle_index].get_tasks_by_time(now=now)
                for task_tuple in tasks_list:
                    tasks_tuple_list.append((client_vehicle_index, task_tuple[1]))
        requested_computing_resources = 0       # cycles
        requested_storage_resources = 0         # bits
        for task_tuple in tasks_tuple_list:
            requested_computing_resources += tasks[task_tuple[1]].get_requested_computing_resources()
            requested_storage_resources += cover_MB_to_bit(tasks[task_tuple[1]].get_input_data_size())
        
        vehicle_indexs = list()
        edge_node_available_computing_capability = cover_GHz_to_Hz(edge_node.get_available_computing_capability(now=now))
        edge_node_available_storage_capability = cover_MB_to_bit(edge_node.get_available_storage_capability(now=now))
        
        for task_tuple in tasks_tuple_list:
            if tasks[task_tuple[1]].get_requested_computing_resources() < cover_GHz_to_Hz(edge_node.get_available_computing_capability(now=now)) and \
                cover_MB_to_bit(tasks[task_tuple[1]].get_input_data_size()) < cover_MB_to_bit(edge_node.get_available_storage_capability(now=now)):
                output_action.set_offloading_decision_of_vehicle_to_edge_node(
                    client_vehicle_index=task_tuple[0],
                    edge_node_index=edge_node_index,
                    offloading_decision=1,
                )
                output_action.set_computing_resource_decision_of_vehicle_to_edge_node(
                    client_vehicle_index=task_tuple[0],
                    edge_node_index=edge_node_index,
                    computing_resource_decision=tasks[task_tuple[1]].get_requested_computing_resources() / cover_GHz_to_Hz(edge_node.get_available_computing_capability(now=now)),
                )
                requested_computing_resources -= tasks[task_tuple[1]].get_requested_computing_resources()
                requested_storage_resources -= cover_MB_to_bit(tasks[task_tuple[1]].get_input_data_size())
                
                edge_node_available_computing_capability -= tasks[task_tuple[1]].get_requested_computing_resources()
                edge_node_available_storage_capability -= cover_MB_to_bit(tasks[task_tuple[1]].get_input_data_size())
                
            else:
                output_action.set_offloading_decision_of_vehicle_to_edge_node(
                    client_vehicle_index=task_tuple[0],
                    edge_node_index=edge_node_index,
                    offloading_decision=0,
                )
                output_action.set_computing_resource_decision_of_vehicle_to_edge_node(
                    client_vehicle_index=task_tuple[0],
                    edge_node_index=edge_node_index,
                    computing_resource_decision=0,
                )
                vehicle_indexs.append(task_tuple[0])
        
        if requested_computing_resources > 0 and requested_storage_resources > 0:
            buyers.append(auction_buyer(
                buyer_type="edge_node",
                index=edge_node_index,
                vehicle_indexs=vehicle_indexs,
                time_slot_index=now,
                requested_computing_resources=requested_computing_resources,
                requested_storage_resources=requested_storage_resources,
                bid=0,
                payment=0,
            ))
        if edge_node_available_computing_capability > 0 and edge_node_available_storage_capability > 0:
            sellers.append(auction_seller(
                seller_type="edge_node",
                index=edge_node_index,
                time_slot_index=now,
                offered_computing_resources=edge_node_available_computing_capability,
                offered_storage_resources=edge_node_available_storage_capability,
                ask=0,
                payment=0,
            ))
    
    sellers.append(auction_seller(
        seller_type="cloud",
        index=0,
        time_slot_index=now,
        offered_computing_resources=cover_GHz_to_Hz(cloud.get_available_computing_capability(now=now)),
        offered_storage_resources=cover_MB_to_bit(cloud.get_available_storage_capability(now=now)),
        ask=0,
        payment=0,
    ))
    
    return output_action, buyers, sellers

def init_bids_and_asks_of_edge_cloud_auction(
    buyers: List[auction_buyer],
    sellers: List[auction_seller],
) -> tuple[List[auction_buyer], List[auction_seller]]:
    buyer_num = len(buyers)
    random_bids = np.random.uniform(0, 1, buyer_num)
    for buyer_index in range(buyer_num):
        random_bid_price = random_bids[buyer_index]
        bid = random_bid_price * buyers[buyer_index].get_requested_computing_resources()
        buyers[buyer_index].set_bid(bid)
    sorted_buyers = sorted(buyers, key=lambda x: x.get_bid(), reverse=True)
    seller_num = len(sellers)
    random_asks = np.random.uniform(0, 1, seller_num)
    for seller_index in range(seller_num):
        random_ask_price = random_asks[seller_index]
        sellers[seller_index].set_ask(random_ask_price)
    sorted_sellers = sorted(sellers, key=lambda x: x.get_ask())
    return sorted_buyers, sorted_sellers

def find_key_index(
    sorted_buyers: List[auction_buyer],
    sorted_sellers: List[auction_seller],
) -> tuple[int, int]:
    max_buyer_number = 0
    buyer_key_index = 0
    seller_key_index = 0
    for buyer_index in range(len(sorted_buyers)):
        for seller_index in range(len(sorted_sellers)):
            buyer_bid = sorted_buyers[buyer_index].get_bid()
            seller_ask = sorted_sellers[seller_index].get_ask()
            if buyer_bid < seller_ask:
                continue
            else:
                if (buyer_index == len(sorted_buyers) - 1) or (seller_index == len(sorted_sellers) - 1) \
                    or ((buyer_index < len(sorted_buyers) - 1) and \
                        (seller_index < len(sorted_sellers) - 1) and \
                        (sorted_buyers[buyer_index + 1].get_bid() < sorted_sellers[seller_index + 1].get_ask())):
                    offered_computing_resource_sum = 0
                    offered_storage_resource_sum = 0
                    for _ in range(seller_index - 1):
                        offered_computing_resource_sum += sorted_sellers[_].get_offered_computing_resources()
                        offered_storage_resource_sum += sorted_sellers[_].get_offered_storage_resources()
                    for buyer_prime_index in range(buyer_index - 1):
                        offered_computing_resource_sum -= sorted_buyers[buyer_prime_index].get_requested_computing_resources()
                        offered_storage_resource_sum -= sorted_buyers[buyer_prime_index].get_requested_storage_resources()
                        if offered_computing_resource_sum < 0 or offered_storage_resource_sum < 0:
                            if buyer_prime_index > max_buyer_number + 1:
                                max_buyer_number = buyer_prime_index - 1
                                buyer_key_index = buyer_prime_index - 1
                                seller_key_index = seller_index
                                break

    return buyer_key_index, seller_key_index

def resource_allocation_of_edge_cloud_auction(
    sorted_buyers: List[auction_buyer],
    sorted_sellers: List[auction_seller],
    buyer_key_index: int,
    seller_key_index: int,
    action: action,
) -> tuple[action, np.ndarray]: 
    output_action = action
    new_buyers = sorted_buyers[0: buyer_key_index + 1]
    new_sellers = sorted_sellers[0: seller_key_index + 1]
    
    offloading_decision = np.zeros((len(sorted_buyers), len(sorted_sellers)))
    
    for seller_index in range(len(new_sellers)):
        offered_computing_resources = new_sellers[seller_index].get_offered_computing_resources()
        offered_storage_resources = new_sellers[seller_index].get_offered_storage_resources()
        offered_computing_resources_copy = offered_computing_resources
        for buyer_index in range(len(new_buyers)):
            requested_computing_resources = new_buyers[buyer_index].get_requested_computing_resources()
            requested_storage_resources = new_buyers[buyer_index].get_requested_storage_resources()
            if offered_computing_resources < requested_computing_resources or offered_storage_resources < requested_storage_resources:
                seller_key_index = seller_index - 1
                break
        for buyer_index in range(len(new_buyers)):
            requested_computing_resources = new_buyers[buyer_index].get_requested_computing_resources()
            requested_storage_resources = new_buyers[buyer_index].get_requested_storage_resources()
            if offered_computing_resources >= requested_computing_resources and offered_storage_resources >= requested_storage_resources:
                offloading_decision[buyer_index][seller_index] = 1
                if new_sellers[seller_index].get_type() == "edge_node":
                    vehicle_indexs = new_buyers[buyer_index].get_vehicle_indexs()
                    for vehicle_index in vehicle_indexs:
                        output_action.set_offloading_decision_of_vehicle_to_edge_node(
                            client_vehicle_index=vehicle_index,
                            edge_node_index=new_sellers[seller_index].get_index(),
                            offloading_decision=1,
                        )
                        output_action.set_computing_resource_decision_of_vehicle_to_edge_node(
                            client_vehicle_index=vehicle_index,
                            edge_node_index=new_sellers[seller_index].get_index(),
                            computing_resource_decision=requested_computing_resources / offered_computing_resources_copy,
                        )
                elif new_sellers[seller_index].get_type() == "cloud":
                    vehicle_indexs = new_buyers[buyer_index].get_vehicle_indexs()
                    for vehicle_index in vehicle_indexs:
                        output_action.set_offloading_decision_of_vehicle_to_cloud_node(
                            client_vehicle_index=new_buyers[buyer_index].get_index(),
                            offloading_decision=1,
                        )
                        output_action.set_computing_resource_decision_of_vehicle_to_cloud_node(
                            client_vehicle_index=new_buyers[buyer_index].get_index(),
                            computing_resource_decision=requested_computing_resources / offered_computing_resources_copy,
                        )
                offered_computing_resources -= requested_computing_resources
                offered_storage_resources -= requested_storage_resources
    
    return output_action, offloading_decision

def payment_pricing(
    buyers: List[auction_buyer],
    sellers: List[auction_seller],
    buyer_key_index: int,
    seller_key_index: int,
    offloading_decision: np.ndarray,
    action: action,
) -> tuple[List[auction_buyer], List[auction_seller]]:
    output_buyers = buyers
    output_sellers = sellers
    for buyer_index in range(len(output_buyers)):
        if offloading_decision[buyer_index].sum() == 1:
            bid_high = output_buyers[buyer_index].get_bid()
            if buyer_index == len(output_buyers) - 1:
                bid_low = output_buyers[buyer_index].get_bid()
            else:
                bid_low = output_buyers[buyer_index + 1].get_bid()
            bid_temp = output_buyers[buyer_index].get_bid()
            while bid_high - bid_low > 0.0001:
                bid_now = (bid_high + bid_low) / 2
                output_buyers[buyer_index].set_bid(bid_now)
                sorted_buyers = sorted(output_buyers, key=lambda x: x.get_bid(), reverse=True)
                buyer_key_index, seller_key_index = find_key_index(sorted_buyers, output_sellers)
                output_action, offloading_decision = resource_allocation_of_edge_cloud_auction(
                    sorted_buyers=sorted_buyers,
                    sorted_sellers=output_sellers,
                    buyer_key_index=buyer_key_index,
                    seller_key_index=seller_key_index,
                    action=action,
                )
                if offloading_decision[buyer_index].sum() == 1:
                    bid_low = bid_now
                else:
                    bid_high = bid_now
                output_buyers[buyer_index].set_payment(bid_now)
                bid_now = bid_temp
    
    for seller_index in range(len(output_sellers)):
        if offloading_decision[:, seller_index].sum() > 0:
            output_sellers[seller_index].set_payment(output_sellers[seller_key_index + 1].get_ask())

    return output_buyers, output_sellers
