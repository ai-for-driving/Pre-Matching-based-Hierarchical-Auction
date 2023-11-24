from typing import List
import numpy as np
import sys
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")
from Objects.vehicle_object import vehicle
from Utilities.time_calculation import compute_V2I_SINR, compute_V2V_SINR

class matching(object):
    
    def __init__(
        self,
        client_vehicles: List[vehicle],
        client_vehicle_num: int,
        server_vehicle_num: int,
        edge_node_num: int,
        white_gaussian_noise: int,
        preference_list: List[List[dict]]
    ) -> None:
        self._matching = list()
        self._client_vehicles = client_vehicles
        self._client_vehicle_num = client_vehicle_num
        self._server_vehicle_num = server_vehicle_num
        self._edge_node_num = edge_node_num
        self._white_gaussian_noise = white_gaussian_noise
        self._preference_list = preference_list
        for i in range(self._client_vehicle_num):
            if len(self._preference_list[i]) > 0:
                self._matching.append((i, self._preference_list[i][0]))
                
    def get_preference_list(self) -> List[List[dict]]:
        return self._preference_list
    
    def get_matching(self) -> List[tuple]:
        return self._matching
    
    def get_matching_partner_of_client_vehicle(self, client_vehicle_id: int):
        for matching in self._matching:
            if matching[0] == client_vehicle_id:
                return matching[1]
        return None
        # raise ValueError("The client vehicle id is out of range.")
    
    def get_matching_partner_of_server_vehicle(self, server_vehicle_id: int):
        matching_partners = list()
        for matching in self._matching:
            if matching[1]["type"] == "server_vehicle" and matching[1]["id"] == server_vehicle_id:
                matching_partners.append(matching[0])
        return matching_partners
    
    def get_matching_partner_of_edge_node(self, edge_node_id: int):
        matching_partners = list()
        for matching in self._matching:
            if matching[1]["type"] == "edge_node" and matching[1]["id"] == edge_node_id:
                matching_partners.append(matching[0])
        return matching_partners
    
    def is_client_vehicle_matched(self, client_vehicle_id: int) -> bool:
        for matching in self._matching:
            if matching[0] == client_vehicle_id:
                return True
        return False
    
    def delete_matching_of_client_vehicle(self, client_vehicle_id: int):
        for matching in self._matching:
            if matching[0] == client_vehicle_id:
                self._matching.remove(matching)
                break
    
    def insert_matching(self, matching_pair: tuple):
        if matching_pair[0] < self._client_vehicle_num:
            if self.is_client_vehicle_matched(matching_pair[0]):
                self.delete_matching_of_client_vehicle(matching_pair[0])
                self._matching.append(matching_pair)
            else:
                self._matching.append(matching_pair)
        else:
            raise ValueError("The client vehicle id is out of range.")
        
    
    def search_blocking_pairs(self) -> List[tuple]:
        blocking_pairs = list()
    
        # searching the blocking pairs
        for client_vehicle_index in range(self._client_vehicle_num):
            for other_client_vehicle_index in range(self._client_vehicle_num):
                if client_vehicle_index != other_client_vehicle_index:
                    client_vehicle_partner = self.get_matching_partner_of_client_vehicle(client_vehicle_index)
                    if client_vehicle_partner is None:
                        continue
                    other_client_vehicle_partner = self.get_matching_partner_of_client_vehicle(other_client_vehicle_index)
                    if other_client_vehicle_partner is None:
                        continue
                    if client_vehicle_partner["id"] == other_client_vehicle_partner["id"] and client_vehicle_partner["type"] == other_client_vehicle_partner["type"]:
                        continue
                    is_other_client_vehicle_partner_in_preference_list_of_client_vehicle = False
                    is_client_vehicle_partner_in_preference_list_of_other_client_vehicle = False
                    index_of_other_client_vehicle_partner_in_preference_list_of_client_vehicle = 0
                    index_of_client_vehicle_partner_in_preference_list_of_other_client_vehicle = 0
                    for preference in self._preference_list[client_vehicle_index]:
                        if preference["id"] == other_client_vehicle_partner["id"] and preference["type"] == other_client_vehicle_partner["type"]:
                            is_other_client_vehicle_partner_in_preference_list_of_client_vehicle = True
                            index_of_other_client_vehicle_partner_in_preference_list_of_client_vehicle = self._preference_list[client_vehicle_index].index(preference)
                            break
                    for preference in self._preference_list[other_client_vehicle_index]:
                        if preference["id"] == client_vehicle_partner["id"] and preference["type"] == client_vehicle_partner["type"]:
                            is_client_vehicle_partner_in_preference_list_of_other_client_vehicle = True
                            index_of_client_vehicle_partner_in_preference_list_of_other_client_vehicle = self._preference_list[other_client_vehicle_index].index(preference)
                            break
                    if is_other_client_vehicle_partner_in_preference_list_of_client_vehicle and is_client_vehicle_partner_in_preference_list_of_other_client_vehicle and \
                        index_of_other_client_vehicle_partner_in_preference_list_of_client_vehicle < self._preference_list[client_vehicle_index].index(client_vehicle_partner) and \
                        index_of_client_vehicle_partner_in_preference_list_of_other_client_vehicle < self._preference_list[other_client_vehicle_index].index(other_client_vehicle_partner):
                        if blocking_pairs == []:
                            blocking_pairs.append((client_vehicle_index, other_client_vehicle_index))
                        else:
                            is_blocking_pair = True
                            for blocking_pair in blocking_pairs:
                                if client_vehicle_index in blocking_pair or other_client_vehicle_index in blocking_pair:
                                    is_blocking_pair = False
                                    break
                            if is_blocking_pair:
                                blocking_pairs.append((client_vehicle_index, other_client_vehicle_index))
        return blocking_pairs

    def is_stable(self) -> bool:
        if len(self.search_blocking_pairs()) == 0:
            return True
        else:
            return False
        
    def get_v2v_SINR(
        self,
        client_vehicle_index : int,
        server_vehicle_index : int,
        channel_gains_between_client_vehicle_and_server_vehicles : np.ndarray,
    ) -> float:
        intra_vehicle_interference = 0
        client_vehicle_index_list = self.get_matching_partner_of_server_vehicle(server_vehicle_index)
        for other_client_vehicle_index in client_vehicle_index_list:
            if other_client_vehicle_index != client_vehicle_index:
                if np.abs(channel_gains_between_client_vehicle_and_server_vehicles[other_client_vehicle_index][server_vehicle_index]) ** 2 < \
                    np.abs(channel_gains_between_client_vehicle_and_server_vehicles[client_vehicle_index][server_vehicle_index]) ** 2:
                    intra_vehicle_interference += \
                        np.abs(channel_gains_between_client_vehicle_and_server_vehicles[other_client_vehicle_index][server_vehicle_index]) ** 2 * \
                            self._client_vehicles[other_client_vehicle_index].get_transmission_power()
                            
        inter_vehicle_interference = 0
        for other_server_vehicle_index in range(self._server_vehicle_num):
            if other_server_vehicle_index != server_vehicle_index:
                client_vehicle_index_list = self.get_matching_partner_of_server_vehicle(other_server_vehicle_index)
                for other_client_vehicle_index in client_vehicle_index_list:
                    if other_client_vehicle_index != client_vehicle_index:
                        inter_vehicle_interference += \
                            np.abs(channel_gains_between_client_vehicle_and_server_vehicles[other_client_vehicle_index][server_vehicle_index]) ** 2 * \
                                self._client_vehicles[other_client_vehicle_index].get_transmission_power()
        
        return compute_V2V_SINR(
            white_gaussian_noise=self._white_gaussian_noise,
            channel_gain=channel_gains_between_client_vehicle_and_server_vehicles[client_vehicle_index][server_vehicle_index],
            transmission_power=self._client_vehicles[client_vehicle_index].get_transmission_power(),
            intra_vehicle_interference=intra_vehicle_interference,
            inter_vehicle_interference=inter_vehicle_interference,
        )
        
        
    def get_v2i_SINR(
        self,
        client_vehicle_index : int, 
        edge_node_index : int,
        channel_gains_between_client_vehicle_and_edge_nodes : np.ndarray,
    ) -> float:
        intra_edge_interference = 0
        client_vehicle_index_list = self.get_matching_partner_of_edge_node(edge_node_index)
        for other_client_vehicle_index in client_vehicle_index_list:
            if other_client_vehicle_index != client_vehicle_index:
                if np.abs(channel_gains_between_client_vehicle_and_edge_nodes[other_client_vehicle_index][edge_node_index]) ** 2 < \
                    np.abs(channel_gains_between_client_vehicle_and_edge_nodes[client_vehicle_index][edge_node_index]) ** 2:
                    intra_edge_interference += \
                        np.abs(channel_gains_between_client_vehicle_and_edge_nodes[other_client_vehicle_index][edge_node_index]) ** 2 * \
                            self._client_vehicles[other_client_vehicle_index].get_transmission_power()
        
        inter_edge_interference = 0
        for other_edge_node_index in range(self._edge_node_num):
            if other_edge_node_index != edge_node_index:
                client_vehicle_index_list = self.get_matching_partner_of_edge_node(other_edge_node_index)
                for other_client_vehicle_index in client_vehicle_index_list:
                    if other_client_vehicle_index != client_vehicle_index:
                        inter_edge_interference += \
                            np.abs(channel_gains_between_client_vehicle_and_edge_nodes[other_client_vehicle_index][edge_node_index]) ** 2 * \
                                self._client_vehicles[other_client_vehicle_index].get_transmission_power()
        
        return compute_V2I_SINR(
            white_gaussian_noise=self._white_gaussian_noise,
            channel_gain=channel_gains_between_client_vehicle_and_edge_nodes[client_vehicle_index][edge_node_index],
            transmission_power=self._client_vehicles[client_vehicle_index].get_transmission_power(),
            intra_edge_interference=intra_edge_interference,
            inter_edge_interference=inter_edge_interference,
        )
        