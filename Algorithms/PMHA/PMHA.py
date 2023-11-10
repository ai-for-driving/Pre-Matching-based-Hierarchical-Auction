from typing import List
import numpy as np
from player import buyer, seller
from Objectives.task import task
from Objectives.vehicle import vehicle
from Objectives.edge_node import edge_node
from Objectives.cloud_server import cloud_server
from Strategy.strategy import action
from best_k_matching import init_preference_list, best_k_offloading_node_matching, get_connection_time_of_vehicles_under_V2V_communication_range, get_connection_time_of_vehicle_under_V2I_communication_range
from vehicle_edge_auction import init_buyers_and_sellers_at_vehicle_edge_auction, init_bids_and_asks_of_vehicle_edge_auction, resource_allocation_and_pricing
from edge_cloud_auction import init_buyers_and_sellers_at_edge_cloud_auction, init_bids_and_asks_of_edge_cloud_auction, find_key_index, resource_allocation_of_edge_cloud_auction, payment_pricing

class PMHA(object):
    
    def __init__(
        self,
        client_vehicle_number: int,
        server_vehicle_number: int,
        edge_node_number: int,
        cloud_server_number: int,
        k_offloading_node_num: int,
        random_change_matching_probability: float,
        path_loss_exponent: int,
    ) -> None:
        self._k_offloading_node_num = k_offloading_node_num
        self._random_change_matching_probability = random_change_matching_probability
        self._path_loss_exponent = path_loss_exponent
        self._action = action(
            client_vehicle_number=client_vehicle_number,
            server_vehicle_number=server_vehicle_number,
            edge_node_number=edge_node_number,
            cloud_server_number=cloud_server_number,
        )

    def generate_action(
        self,
        client_vehicles: List[vehicle],
        server_vehicles: List[vehicle],
        edge_nodes: List[edge_node],
        cloud: cloud_server,
        tasks: List[task],
        now: int,
        distance_matrix_between_client_vehicles_and_server_vehicles: np.ndarray,
        distance_matrix_between_client_vehicles_and_edge_nodes: np.ndarray,
        vehicles_under_V2V_communication_range: np.ndarray,
        vehicles_under_V2I_communication_range: np.ndarray,
    ) -> action:
        
        connection_time_of_vehicles_under_V2V_communication_range = get_connection_time_of_vehicles_under_V2V_communication_range(
            distance_matrix=distance_matrix_between_client_vehicles_and_server_vehicles,
            vehicles_under_V2V_communication_range=vehicles_under_V2V_communication_range,
            client_vehicles=client_vehicles,
            server_vehicles=server_vehicles,
            now=now,
        )
    
        connection_time_of_vehicles_under_V2I_communication_range = get_connection_time_of_vehicle_under_V2I_communication_range(
            vehicles_under_V2I_communication_range=vehicles_under_V2I_communication_range,
            client_vehicles=client_vehicles,
            edge_nodes=edge_nodes,
            now=now,
        )
        
        preference_list = init_preference_list(
            client_vehicles=client_vehicles,
            server_vehicles=server_vehicles,
            edge_nodes=edge_nodes,
            vehicles_under_V2V_communication_range=vehicles_under_V2V_communication_range,
            vehicles_under_V2I_communication_range=vehicles_under_V2I_communication_range,
            connection_time_of_vehicles_under_V2V_communication_range=connection_time_of_vehicles_under_V2V_communication_range,
            connection_time_of_vehicles_under_V2I_communication_range=connection_time_of_vehicles_under_V2I_communication_range,
            now=now,
        )
        
        best_k_nodes = best_k_offloading_node_matching(
            client_vehicles=client_vehicles,
            server_vehicles=server_vehicles,
            edge_nodes=edge_nodes,
            k_offloading_node_num=self._k_offloading_node_num,
            distance_matrix_between_client_vehicles_and_server_vehicles=distance_matrix_between_client_vehicles_and_server_vehicles,
            distance_matrix_between_client_vehicles_and_edge_nodes=distance_matrix_between_client_vehicles_and_edge_nodes,
            preference_list=preference_list,
            random_change_matching_probability=self._random_change_matching_probability,
            path_loss_exponent=self._path_loss_exponent,
        )
        
        
        self._action, vehicle_edge_auction_buyer_list, vehicle_edge_auction_seller_list = init_buyers_and_sellers_at_vehicle_edge_auction(
            client_vehicles=client_vehicles,
            server_vehicles=server_vehicles,
            edge_nodes=edge_nodes,
            tasks=tasks,
            action=self._action,
            best_k_nodes=best_k_nodes,
            now=now,
        )
        
        vehicle_edge_auction_buyer_list, vehicle_edge_auction_seller_list = init_bids_and_asks_of_vehicle_edge_auction(
            buyers_list=vehicle_edge_auction_buyer_list,
            sellers_list=vehicle_edge_auction_seller_list,
        )
        
        self._action, vehicle_edge_auction_offloading_decision, vehicle_edge_auction_buyer_list, vehicle_edge_auction_seller_list = resource_allocation_and_pricing(
            client_vehicle_number=len(client_vehicles),
            server_vehicle_number=len(server_vehicles),
            edge_node_number=len(edge_nodes),
            buyers_list=vehicle_edge_auction_buyer_list,
            sellers_list=vehicle_edge_auction_seller_list,
            action=self._action,
        )
        
        self._action, edge_cloud_auction_buyers, edge_cloud_auction_sellers = init_buyers_and_sellers_at_edge_cloud_auction(
            client_vehicles=client_vehicles,
            edge_nodes=edge_nodes,
            cloud=cloud,
            tasks=tasks,
            offloading_decision=vehicle_edge_auction_offloading_decision,
            action=self._action,
            now=now,
        )
        
        edge_cloud_auction_buyers, edge_cloud_auction_sellers = init_bids_and_asks_of_edge_cloud_auction(
            buyers=edge_cloud_auction_buyers,
            sellers=edge_cloud_auction_sellers,
        )
        
        buyer_key_index, seller_key_index = find_key_index(
            sorted_buyers=edge_cloud_auction_buyers,
            sorted_sellers=edge_cloud_auction_sellers,
        )
        
        self._action, edge_cloud_auction_offloading_decision = resource_allocation_of_edge_cloud_auction(
            sorted_buyers=edge_cloud_auction_buyers,
            sorted_sellers=edge_cloud_auction_sellers,
            buyer_key_index=buyer_key_index,
            seller_key_index=seller_key_index,
            action=self._action,
        )
        
        
        edge_cloud_auction_buyers, edge_cloud_auction_sellers = payment_pricing(
            buyers=edge_cloud_auction_buyers,
            sellers=edge_cloud_auction_sellers,
            buyer_key_index=buyer_key_index,
            seller_key_index=seller_key_index,
            offloading_decision=edge_cloud_auction_offloading_decision,
        )
        
        return self._action