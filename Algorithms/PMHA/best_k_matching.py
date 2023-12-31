from typing import List
import numpy as np
import sys
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")
np.set_printoptions(threshold=np.inf)
from Objects.vehicle_object import vehicle
from Objects.edge_node_object import edge_node
from Algorithms.PMHA.matching_object import matching
from Utilities.distance_and_coverage import calculate_distance
from Utilities.noma import obtain_channel_gains_between_client_vehicle_and_server_vehicles, obtain_channel_gains_between_vehicles_and_edge_nodes

def get_connection_time_of_vehicles_under_V2V_communication_range(
    distance_matrix : np.ndarray,
    vehicles_under_V2V_communication_range: np.ndarray,
    client_vehicles: List[vehicle],
    server_vehicles: List[vehicle],
    now: int
) -> np.ndarray: 
    connection_time = np.zeros(
        (len(client_vehicles), len(server_vehicles)))
    for i in range(len(client_vehicles)):
        for j in range(len(server_vehicles)):
            if i != j:
                if vehicles_under_V2V_communication_range[i][j] == 1:
                    vi_direction = client_vehicles[i].get_mobility(now=now).get_direction()
                    vj_direction = server_vehicles[j].get_mobility(now=now).get_direction()
                    vi_speed = client_vehicles[i].get_mobility(now=now).get_speed()
                    vj_speed = server_vehicles[j].get_mobility(now=now).get_speed()
                    if vi_direction == vj_direction:    # 两车同向
                        if now != 0:
                            distance = calculate_distance(
                                client_vehicles[i].get_mobility(now - 1), 
                                server_vehicles[j].get_mobility(now - 1),
                                type="vehicles"
                            )
                            if distance < distance_matrix[i][j]:
                                connection_time[i][j] = (client_vehicles[i].get_communication_range() - distance_matrix[i][j]) / np.abs(vi_speed - vj_speed)
                            else:
                                connection_time[i][j] = (client_vehicles[i].get_communication_range() + distance_matrix[i][j]) / np.abs(vi_speed - vj_speed)
                        else:
                            distance = calculate_distance(
                                client_vehicles[i].get_mobility(now + 1),
                                server_vehicles[j].get_mobility(now + 1),
                                type="vehicles"
                            )
                            if distance_matrix[i][j] < distance:
                                connection_time[i][j] = (client_vehicles[i].get_communication_range() - distance_matrix[i][j]) / np.abs(vi_speed - vj_speed)
                            else:
                                connection_time[i][j] = (client_vehicles[i].get_communication_range() + distance_matrix[i][j]) / np.abs(vi_speed - vj_speed)
                    else:   # 两车不同向
                        if now != 0:
                            distance = calculate_distance(
                                client_vehicles[i].get_mobility(now - 1),
                                server_vehicles[j].get_mobility(now - 1),
                                type="vehicles"
                            )
                            if distance < distance_matrix[i][j]:
                                connection_time[i][j] = (client_vehicles[i].get_communication_range() - distance_matrix[i][j]) / np.abs(vi_speed + vj_speed)
                            else:
                                connection_time[i][j] = (client_vehicles[i].get_communication_range() + distance_matrix[i][j]) / np.abs(vi_speed + vj_speed)
                        else:
                            distance = calculate_distance(
                                client_vehicles[i].get_mobility(now + 1),
                                server_vehicles[j].get_mobility(now + 1),
                                type="vehicles"
                            )
                            if distance_matrix[i][j] < distance:
                                connection_time[i][j] = (client_vehicles[i].get_communication_range() - distance_matrix[i][j]) / np.abs(vi_speed + vj_speed)
                            else:
                                connection_time[i][j] = (client_vehicles[i].get_communication_range() + distance_matrix[i][j]) / np.abs(vi_speed + vj_speed)
    return connection_time

def get_connection_time_of_vehicle_under_V2I_communication_range(
    vehicles_under_V2I_communication_range: np.ndarray,
    client_vehicles: List[vehicle],
    edge_nodes: List[edge_node],
    now: int
) -> np.ndarray: 
    connection_time = np.zeros(
        (len(client_vehicles), len(edge_nodes)))
    for i in range(len(client_vehicles)):
        for j in range(len(edge_nodes)):
            if vehicles_under_V2I_communication_range[i][j] == 1:
                for time_index in range(now + 1, client_vehicles[i].get_time_slot_num()):
                    distance = calculate_distance(
                        client_vehicles[i].get_mobility(now=time_index), 
                        edge_nodes[j].get_mobility(),
                        type="edge_nodes"
                    )
                    if distance <= edge_nodes[j].get_communication_range():
                        connection_time[i][j] += 1
    return connection_time

def init_preference_list(
    client_vehicles: List[vehicle],
    server_vehicles: List[vehicle],
    edge_nodes: List[edge_node],
    vehicles_under_V2V_communication_range: np.ndarray,
    vehicles_under_V2I_communication_range: np.ndarray,
    connection_time_of_vehicles_under_V2V_communication_range: np.ndarray,
    connection_time_of_vehicles_under_V2I_communication_range: np.ndarray,
    now: int,
) -> List[List[dict]]:
    client_vehicle_num = len(client_vehicles)
    server_vehicle_num = len(server_vehicles)
    edge_node_num = len(edge_nodes)
    
    preference_list = list()
    
    for client_vehicle_index in range(client_vehicle_num):
        client_vehicle_preference_list = list()
        for server_vehicle_index in range(server_vehicle_num):
            if vehicles_under_V2V_communication_range[client_vehicle_index][server_vehicle_index] == 1:
                client_vehicle_preference_list.append(
                    {
                        "type": "server_vehicle", 
                        "id": server_vehicle_index, 
                        "connection_time": connection_time_of_vehicles_under_V2V_communication_range[client_vehicle_index][server_vehicle_index], 
                        "computing_capability": server_vehicles[server_vehicle_index].get_available_computing_capability(now=now), 
                        "storage_capability": server_vehicles[server_vehicle_index].get_available_storage_capability(now=now),
                    })
        for edge_node_index in range(edge_node_num):
            if vehicles_under_V2I_communication_range[client_vehicle_index][edge_node_index] == 1:
                client_vehicle_preference_list.append(
                    {
                        "type": "edge_node", 
                        "id": edge_node_index, 
                        "connection_time": connection_time_of_vehicles_under_V2I_communication_range[client_vehicle_index][edge_node_index], 
                        "computing_capability": edge_nodes[edge_node_index].get_available_computing_capability(now=now),
                        "storage_capability": edge_nodes[edge_node_index].get_available_storage_capability(now=now),
                    })
        # sort the preference list by connection time, computing capability and storage capability
        client_vehicle_preference_list = sorted(
            client_vehicle_preference_list, 
            key=lambda x: (x["connection_time"], x["computing_capability"], x["storage_capability"]), 
            reverse=True
        )
        preference_list.append(client_vehicle_preference_list)
    return preference_list


def best_k_offloading_node_matching(
    client_vehicles: List[vehicle],
    server_vehicles: List[vehicle],
    edge_nodes: List[edge_node],
    k_offloading_node_num: int,
    distance_matrix_between_client_vehicles_and_server_vehicles: np.ndarray,
    distance_matrix_between_client_vehicles_and_edge_nodes: np.ndarray,
    preference_list: List[List[dict]],
    random_change_matching_probability: float,
    path_loss_exponent: int,
    white_gaussian_noise: int,
) -> np.ndarray:
    # Initialization
    client_vehicle_num = len(client_vehicles)
    server_vehicle_num = len(server_vehicles)
    edge_node_num = len(edge_nodes)

    init_matching = matching(
        client_vehicles=client_vehicles,
        client_vehicle_num=client_vehicle_num,
        server_vehicle_num=server_vehicle_num,
        edge_node_num=edge_node_num,
        white_gaussian_noise=white_gaussian_noise,
        preference_list=preference_list,
    )
    
    best_k_nodes = np.zeros((client_vehicle_num, server_vehicle_num + edge_node_num))
    
    now_matching = matching(
        client_vehicles=client_vehicles,
        client_vehicle_num=client_vehicle_num,
        server_vehicle_num=server_vehicle_num,
        edge_node_num=edge_node_num,
        white_gaussian_noise=white_gaussian_noise,
        preference_list=preference_list,
    )
    
    now_matching = init_matching
    
    channel_gains_between_client_vehicle_and_server_vehicles = obtain_channel_gains_between_client_vehicle_and_server_vehicles(
        distance_matrix=distance_matrix_between_client_vehicles_and_server_vehicles,
        client_vehicles=client_vehicles,
        server_vehicles=server_vehicles,
        path_loss_exponent=path_loss_exponent,
    )
    channel_gains_between_client_vehicle_and_edge_nodes = obtain_channel_gains_between_vehicles_and_edge_nodes(
        distance_matrix=distance_matrix_between_client_vehicles_and_edge_nodes,
        client_vehicles=client_vehicles,
        edge_nodes=edge_nodes,
        path_loss_exponent=path_loss_exponent,
    )
    
    for _ in range(client_vehicle_num * k_offloading_node_num):
        while True:
            if now_matching.is_stable():
                break

            blocking_pairs = now_matching.search_blocking_pairs()
            for blocking_pair in blocking_pairs:
                partner_of_v1 = now_matching.get_matching_partner_of_client_vehicle(blocking_pair[0])
                partner_of_v2 = now_matching.get_matching_partner_of_client_vehicle(blocking_pair[1])
                
                now_v1_sinr = 0
                now_v2_sinr = 0
                
                if partner_of_v1["type"] == "server_vehicle":
                    now_v1_sinr = now_matching.get_v2v_SINR(
                        client_vehicle_index=blocking_pair[0],
                        server_vehicle_index=partner_of_v1["id"],
                        channel_gains_between_client_vehicle_and_server_vehicles=channel_gains_between_client_vehicle_and_server_vehicles,
                    )
                elif partner_of_v1["type"] == "edge_node":
                    now_v1_sinr = now_matching.get_v2i_SINR(
                        client_vehicle_index=blocking_pair[0],
                        edge_node_index=partner_of_v1["id"],
                        channel_gains_between_client_vehicle_and_edge_nodes=channel_gains_between_client_vehicle_and_edge_nodes,
                    )
                else:
                    raise ValueError("The type of partner of v1 is wrong.")
                
                if partner_of_v2["type"] == "server_vehicle":
                    now_v2_sinr = now_matching.get_v2v_SINR(
                        client_vehicle_index=blocking_pair[1],
                        server_vehicle_index=partner_of_v2["id"],
                        channel_gains_between_client_vehicle_and_server_vehicles=channel_gains_between_client_vehicle_and_server_vehicles,
                    )
                elif partner_of_v2["type"] == "edge_node":
                    now_v2_sinr = now_matching.get_v2i_SINR(
                        client_vehicle_index=blocking_pair[1],
                        edge_node_index=partner_of_v2["id"],
                        channel_gains_between_client_vehicle_and_edge_nodes=channel_gains_between_client_vehicle_and_edge_nodes,
                    )
                else:
                    raise ValueError("The type of partner of v2 is wrong.")
                
                updated_matching = matching(
                    client_vehicles=client_vehicles,
                    client_vehicle_num=client_vehicle_num,
                    server_vehicle_num=server_vehicle_num,
                    edge_node_num=edge_node_num,
                    white_gaussian_noise=white_gaussian_noise,
                    preference_list=preference_list,
                )
                
                updated_matching = now_matching
                
                updated_matching.delete_matching_of_client_vehicle(blocking_pair[0])
                updated_matching.delete_matching_of_client_vehicle(blocking_pair[1])
                
                new_partner_of_v1 = dict()
                new_partner_of_v2 = dict()
                for preference in now_matching.get_preference_list()[blocking_pair[0]]:
                    if preference["id"] == partner_of_v2["id"] and preference["type"] == partner_of_v2["type"]:
                        new_partner_of_v1 = preference
                        break
                for preference in preference_list[blocking_pair[1]]:
                    if preference["id"] == partner_of_v1["id"] and preference["type"] == partner_of_v1["type"]:
                        new_partner_of_v2 = preference
                        break
                if new_partner_of_v1 == dict() or new_partner_of_v2 == dict():
                    raise ValueError("The new partner of v1 or v2 is wrong.")
                updated_matching.insert_matching((blocking_pair[0], new_partner_of_v1))
                updated_matching.insert_matching((blocking_pair[1], new_partner_of_v2))
                
                updated_v1_sinr = 0
                updated_v2_sinr = 0
                
                if partner_of_v1["type"] == "server_vehicle":
                    updated_v1_sinr = updated_matching.get_v2v_SINR(
                        client_vehicle_index=blocking_pair[0],
                        server_vehicle_index=partner_of_v1["id"],
                        channel_gains_between_client_vehicle_and_server_vehicles=channel_gains_between_client_vehicle_and_server_vehicles,
                    )
                elif partner_of_v1["type"] == "edge_node":
                    updated_v1_sinr = updated_matching.get_v2i_SINR(
                        client_vehicle_index=blocking_pair[0],
                        edge_node_index=partner_of_v1["id"],
                        channel_gains_between_client_vehicle_and_edge_nodes=channel_gains_between_client_vehicle_and_edge_nodes,
                    )
                else:
                    raise ValueError("The type of partner of v1 is wrong.")
                
                if partner_of_v2["type"] == "server_vehicle":
                    updated_v2_sinr = updated_matching.get_v2v_SINR(
                        client_vehicle_index=blocking_pair[1],
                        server_vehicle_index=partner_of_v2["id"],
                        channel_gains_between_client_vehicle_and_server_vehicles=channel_gains_between_client_vehicle_and_server_vehicles,
                    )
                elif partner_of_v2["type"] == "edge_node":
                    updated_v2_sinr = updated_matching.get_v2i_SINR(
                        client_vehicle_index=blocking_pair[1],
                        edge_node_index=partner_of_v2["id"],
                        channel_gains_between_client_vehicle_and_edge_nodes=channel_gains_between_client_vehicle_and_edge_nodes,
                    )
                else:
                    raise ValueError("The type of partner of v2 is wrong.")
                
                if updated_v1_sinr > now_v1_sinr and updated_v2_sinr > now_v2_sinr:
                    
                    now_matching = updated_matching
            break
            
        for client_vehicle_index in range(client_vehicle_num):
            matching_partner = now_matching.get_matching_partner_of_client_vehicle(client_vehicle_index)
            if matching_partner is None:
                continue
            if matching_partner["type"] == "server_vehicle":
                best_k_nodes[client_vehicle_index][matching_partner["id"]] = 1
            elif matching_partner["type"] == "edge_node":
                best_k_nodes[client_vehicle_index][server_vehicle_num + matching_partner["id"]] = 1
            else:
                raise ValueError("The type of matching partner is wrong.")
            
        now_matching = init_matching
        for client_vehicle_index in range(client_vehicle_num):
            random_number = np.random.rand()
            if random_number < random_change_matching_probability:
                now_matching.delete_matching_of_client_vehicle(client_vehicle_index)
                preference_list_number = len(preference_list[client_vehicle_index])
                if preference_list_number == 0:
                    continue
                random_number = np.random.randint(0, preference_list_number)
                now_matching.insert_matching((client_vehicle_index, preference_list[client_vehicle_index][random_number]))
        
        # print("round:", _)
        # print("\nbest_k_nodes")
        # print(best_k_nodes)
    
    return best_k_nodes