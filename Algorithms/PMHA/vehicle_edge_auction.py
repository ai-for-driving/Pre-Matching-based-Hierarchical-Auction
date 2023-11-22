from typing import List
import numpy as np
from Algorithms.PMHA.player import auction_buyer, auction_seller
from Objects.task import task
from Objects.vehicle import vehicle
from Objects.edge_node import edge_node
from Strategy.strategy import action
from Utilities.conversion import cover_MB_to_bit, cover_GHz_to_Hz, cover_bit_to_MB, cover_Hz_to_GHz

def init_buyers_and_sellers_at_vehicle_edge_auction(
    client_vehicles: List[vehicle],
    server_vehicles: List[vehicle],
    edge_nodes: List[edge_node],
    tasks: List[task],
    action: action,
    best_k_nodes: np.ndarray,
    now: int,
) -> tuple[action, List[List[auction_buyer]], List[List[auction_seller]]]:
    buyers = list()
    sellers = list()
    output_action = action
    for client_vehicle_index in range(len(client_vehicles)):
        client_vehicle = client_vehicles[client_vehicle_index]
        tasks_list = client_vehicle.get_tasks_by_time(now=now)
        requested_computing_resources = 0       # cycles
        requested_storage_resources = 0         # bits
        for task_tuple in tasks_list:
            requested_computing_resources += tasks[task_tuple[1]].get_requested_computing_resources()
            requested_storage_resources += cover_MB_to_bit(tasks[task_tuple[1]].get_input_data_size())
        
        # print("*" * 50)
        # print("client_vehicle_index: ", client_vehicle_index)
        # print("requested_computing_resources: ", cover_Hz_to_GHz(requested_computing_resources))
        # print("requested_storage_resources: ", cover_bit_to_MB(requested_storage_resources))
        # print("client_vehicle.get_available_computing_capability(now=now)): ", client_vehicle.get_available_computing_capability(now=now))
        # print("client_vehicle.get_available_storage_capability(now=now)): ", client_vehicle.get_available_storage_capability(now=now))
        # print("requested_computing_resources <= cover_GHz_to_Hz(client_vehicle.get_available_computing_capability(now=now)): ", requested_computing_resources <= cover_GHz_to_Hz(client_vehicle.get_available_computing_capability(now=now)))
        # print("requested_storage_resources <= cover_MB_to_bit(client_vehicle.get_available_storage_capability(now=now)): ", requested_storage_resources <= cover_MB_to_bit(client_vehicle.get_available_storage_capability(now=now)))
        
        if requested_computing_resources <= cover_GHz_to_Hz(client_vehicle.get_available_computing_capability(now=now)) and \
            requested_storage_resources <= cover_MB_to_bit(client_vehicle.get_available_storage_capability(now=now)):
            output_action.set_offloading_decision_at_local(
                client_vehicle_index=client_vehicle_index,
                offloading_decision=1,
            )
            output_action.set_computing_resource_decision_at_local(
                client_vehicle_index=client_vehicle_index,
                computing_resource_decision=requested_computing_resources / cover_GHz_to_Hz(client_vehicle.get_available_computing_capability(now=now)),
            )
            continue
        
        buyers.append(auction_buyer(
            buyer_type="vehicle",
            index=client_vehicle_index,
            vehicle_indexs=client_vehicle_index,
            time_slot_index=now,
            requested_computing_resources=requested_computing_resources,
            requested_storage_resources=requested_storage_resources,
            bid=0,
            payment=0,
        ))
    
    for server_vehicle_index in range(len(server_vehicles)):
        server_vehicle = server_vehicles[server_vehicle_index]
        sellers.append(auction_seller(
            seller_type="server_vehicle",
            index=server_vehicle_index,
            time_slot_index=now,
            offered_computing_resources=cover_GHz_to_Hz(server_vehicle.get_available_computing_capability(now=now)),
            offered_storage_resources=cover_MB_to_bit(server_vehicle.get_available_storage_capability(now=now)),
            ask=0,
            payment=0,
        ))
    for edge_node_index in range(len(edge_nodes)):
        edge_node = edge_nodes[edge_node_index]
        sellers.append(auction_seller(
            seller_type="edge_node",
            index=edge_node_index,
            time_slot_index=now,
            offered_computing_resources=cover_GHz_to_Hz(edge_node.get_available_computing_capability(now=now)),
            offered_storage_resources=cover_MB_to_bit(edge_node.get_available_storage_capability(now=now)),
            ask=0,
            payment=0,
        ))
        
    # print("output_action: \n", output_action)
    
    output_buyer_list = list()
    output_seller_list = list()
    
    # print("best_k_nodes: \n", best_k_nodes)
    
    for server_vehicle_index in range(len(server_vehicles)):
        buyer_list = list()
        for client_vehicle_index in range(len(client_vehicles)):
            if best_k_nodes[client_vehicle_index][server_vehicle_index] == 1:
                for buyer in buyers:
                    if buyer.get_type() == "vehicle" and \
                        buyer.get_index() == client_vehicle_index:
                        buyer_list.append(buyer)
                        break
        seller_list = list()
        for seller in sellers:
            if seller.get_type() == "vehicle" and \
                seller.get_index() == server_vehicle_index:
                seller_list.append(seller)
                break
        output_buyer_list.append(buyer_list)
        output_seller_list.append(seller_list)
        
    for edge_node_index in range(len(edge_nodes)):
        buyer_list = list()
        for client_vehicle_index in range(len(client_vehicles)):
            if best_k_nodes[client_vehicle_index][len(server_vehicles) + edge_node_index] == 1:
                for buyer in buyers:
                    if buyer.get_type() == "vehicle" and \
                        buyer.get_index() == client_vehicle_index:
                        buyer_list.append(buyer)
                        break
        seller_list = list()
        for seller in sellers:
            if seller.get_type() == "edge_node" and \
                seller.get_index() == edge_node_index:
                seller_list.append(seller)
                break
        output_buyer_list.append(buyer_list)
        output_seller_list.append(seller_list)
    
    return output_action, output_buyer_list, output_seller_list
    

def init_bids_and_asks_of_vehicle_edge_auction(
    buyers_list: List[List[auction_buyer]],
    sellers_list: List[List[auction_seller]],
) -> List[tuple[List[auction_buyer], List[auction_seller]]]:
    
    for i in range(len(buyers_list)):
        buyers = buyers_list[i]
        sellers = sellers_list[i]
        buyer_num = len(buyers)
        random_bids = np.random.uniform(0, 1, buyer_num)
        for _ in range(buyer_num):
            random_bid_price = random_bids[_]
            bid = random_bid_price * buyers[_].get_requested_computing_resources()
            buyers[_].set_bid(bid)
        sorted_buyers = sorted(buyers, key=lambda x: x.get_bid(), reverse=True)
        seller_num = len(sellers)
        random_asks = np.random.uniform(0, 1, seller_num)
        for _ in range(seller_num):
            sellers[_].set_ask(random_asks[_])
        sorted_sellers = sorted(sellers, key=lambda x: x.get_ask())
        buyers_list[i] = sorted_buyers
        sellers_list[i] = sorted_sellers
    return buyers_list, sellers_list

def resource_allocation_and_pricing(
    client_vehicle_number: int,
    server_vehicle_number: int,
    edge_node_number: int,
    buyers_list: List[List[auction_buyer]],
    sellers_list: List[List[auction_seller]],
    action: action,
) -> tuple[action, np.ndarray, List[List[auction_buyer]], List[List[auction_seller]]]:
    output_buyers_list = buyers_list
    output_sellers_list = sellers_list
    output_action = action
    offloading_decision = np.zeros((client_vehicle_number, server_vehicle_number + edge_node_number))
    for seller_index in range(len(output_sellers_list)):
        buyers = output_buyers_list[seller_index]
        sellers = output_sellers_list[seller_index]
        if len(sellers) == 1:
            requested_computing_resources = 0
            requested_storage_resources = 0
            if sellers[0].get_type() == "server_vehicle":
                for buyer in buyers:
                    requested_computing_resources += buyer.get_requested_computing_resources()
                    requested_storage_resources += buyer.get_requested_storage_resources()
                    if requested_computing_resources <= sellers[0].get_offered_computing_resources() and \
                        requested_storage_resources <= sellers[0].get_offered_storage_resources():
                        offloading_decision[buyer.get_index()][sellers[0].get_index()] = 1
                    else:
                        break
            elif sellers[0].get_type() == "edge_node":
                for buyer in buyers:
                    requested_computing_resources += buyer.get_requested_computing_resources()
                    requested_storage_resources += buyer.get_requested_storage_resources()
                    if requested_storage_resources <= sellers[0].get_offered_storage_resources():
                        offloading_decision[buyer.get_index()][server_vehicle_number + sellers[0].get_index()] = 1
                    else:
                        break
        else:
            continue
            # raise ValueError("The number of sellers is not 1.")
        
    for client_vehicle_index in range(client_vehicle_number):
        min_ask = 1
        min_index = -1
        for server_vehicle_index in range(server_vehicle_number):
            if offloading_decision[client_vehicle_index][server_vehicle_index] == 1:
                if min_ask > output_sellers_list[server_vehicle_index][0].get_ask():
                    min_ask = output_sellers_list[server_vehicle_index][0].get_ask()
                    min_index = server_vehicle_index
        for edge_node_index in range(edge_node_number):
            if offloading_decision[client_vehicle_index][server_vehicle_number + edge_node_index] == 1:
                if min_ask > output_sellers_list[server_vehicle_number + edge_node_index][0].get_ask():
                    min_ask = output_sellers_list[server_vehicle_number + edge_node_index][0].get_ask()
                    min_index = server_vehicle_number + edge_node_index
        if min_index != -1:
            offloading_decision[client_vehicle_index][min_index] = 1
            if min_index < server_vehicle_number:
                buyers = output_buyers_list[min_index]
                seller = output_sellers_list[min_index][0]
                requested_computing_resources = 0
                for buyer in buyers:
                    if buyer.get_type() == "vehicle" and \
                        buyer.get_index() == client_vehicle_index:
                        requested_computing_resources = buyer.get_requested_computing_resources()
                output_action.set_offloading_decision_of_vehicle_to_vehicle(
                    client_vehicle_index=client_vehicle_index,
                    server_vehicle_index=min_index,
                    offloading_decision=1,
                )
                output_action.set_computing_resource_decision_of_vehicle_to_vehicle(
                    client_vehicle_index=client_vehicle_index,
                    server_vehicle_index=min_index,
                    computing_resource_decision=requested_computing_resources / seller.get_offered_computing_resources(),
                )
            else:
                buyers = output_buyers_list[min_index]
                seller = output_sellers_list[min_index][0]
                requested_computing_resources = 0
                for buyer in buyers:
                    if buyer.get_type() == "vehicle" and \
                        buyer.get_index() == client_vehicle_index:
                        requested_computing_resources = buyer.get_requested_computing_resources()
                output_action.set_offloading_decision_of_vehicle_to_edge_node(
                    client_vehicle_index=client_vehicle_index,
                    edge_node_index=min_index - server_vehicle_number,
                    offloading_decision=1,
                )
                output_action.set_computing_resource_decision_of_vehicle_to_edge_node(
                    client_vehicle_index=client_vehicle_index,
                    edge_node_index=min_index - server_vehicle_number,
                    computing_resource_decision=requested_computing_resources / seller.get_offered_computing_resources(),
                )
            
    for seller_index in range(len(output_buyers_list)):
        buyers = output_buyers_list[seller_index]
        sellers = output_sellers_list[seller_index]
        seller_payment = 0
        if len(sellers) == 1:
            for buyer_index in range(len(buyers)):
                if offloading_decision[buyer_index][seller_index] == 1:
                    buyers[buyer_index].set_payment(sellers[0].get_ask() * buyers[buyer_index].get_requested_computing_resources())
                    seller_payment += buyers[buyer_index].get_payment()
                else:
                    buyers[buyer_index].set_payment(0)
            sellers[0].set_payment(seller_payment)
            output_buyers_list[seller_index] = buyers
            output_sellers_list[seller_index] = sellers
        else:
            raise ValueError("The number of sellers is not 1.")
        
    return output_action, offloading_decision, output_buyers_list, output_sellers_list