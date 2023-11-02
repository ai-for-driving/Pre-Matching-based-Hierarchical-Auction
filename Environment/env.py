from Utilities.noma import obtain_channel_gains_between_client_vehicle_and_server_vehicles, obtain_channel_gains_between_vehicles_and_edge_nodes
from Utilities.wired_bandwidth import get_wired_bandwidth_between_edge_node_and_other_edge_nodes
from Environment.env_profile import env_profile
from Objectives.task import task
from Objectives.vehicle import vehicle
from Objectives.edge_node import edge_node
from Objectives.cloud_server import cloud_server
from Utilities.objective_generation import generate_task_set, generate_vehicles, generate_edge_nodes, generate_cloud
from Utilities.vehicle_classification import get_client_and_server_vehicles
from Utilities.distance_and_coverage import get_distance_matrix_between_client_vehicles_and_server_vehicles, get_distance_matrix_between_vehicles_and_edge_nodes, get_distance_matrix_between_edge_nodes  
from Utilities.distance_and_coverage import get_vehicles_under_V2I_communication_range, get_vehicles_under_V2V_communication_range
from typing import List, Tuple
import numpy as np
import time
import pickle
from Strategy.strategy import action
from Utilities.time_calculation import obtain_computing_time, obtain_transmission_time, obtain_wired_transmission_time
from Utilities.time_calculation import compute_transmission_rate, compute_V2V_SINR, compute_V2I_SINR

class env(object):
    
    def __init__(
        self,
        profile: env_profile
    ) -> None:
        self._env_profile = profile
        self._now = 0
        self._end_time = profile.get_slot_length() - 1
        self._task_num_at_time = [0 for _ in range(profile.get_slot_length())]
        self._average_processing_time_at_time = [0 for _ in range(profile.get_slot_length())]
        self._average_transmission_time_at_time = [0 for _ in range(profile.get_slot_length())]
        self._average_computing_time_at_time = [0 for _ in range(profile.get_slot_length())]
        self._average_computing_capability_at_time = [0 for _ in range(profile.get_slot_length())]
        self._average_storage_capability_at_time = [0 for _ in range(profile.get_slot_length())]
        self._task_processed_at_local_at_time = [0 for _ in range(profile.get_slot_length())]
        self._task_processed_at_vehicle_at_time = [0 for _ in range(profile.get_slot_length())]
        self._task_processed_at_edge_at_time = [0 for _ in range(profile.get_slot_length())]
        self._task_processed_at_local_edge_at_time = [0 for _ in range(profile.get_slot_length())]
        self._task_processed_at_other_edge_at_time = [0 for _ in range(profile.get_slot_length())]
        self._task_processed_at_cloud_at_time = [0 for _ in range(profile.get_slot_length())]
        self._task_successfully_processed_num_at_time = [0 for _ in range(profile.get_slot_length())]
        
        
        self._resutls_file_name = "/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/Results/" \
            + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ".txt"
        
        self._tasks : List[task] = generate_task_set(
            task_num=profile.get_task_num(),
            distribution=profile.get_task_distribution(),
            min_input_data_size=profile.get_min_input_data_size_of_tasks(),
            max_input_data_size=profile.get_max_input_data_size_of_tasks(),
            min_cqu_cycles=profile.get_min_cqu_cycles_of_tasks(),
            max_cqu_cycles=profile.get_max_cqu_cycles_of_tasks(),
            min_deadline=profile.get_min_deadline_of_tasks(),
            max_deadline=profile.get_max_deadline_of_tasks(),
        )
        
        self._vehicles : List[vehicle] = generate_vehicles(
            vehicle_num=profile.get_vehicle_num(),
            slot_length=profile.get_slot_length(),
            file_name_key=profile.get_vehicle_mobility_file_name_key(),
            slection_way=profile.get_vehicular_trajectories_processing_selection_way(),
            filling_way=profile.get_vehicular_trajectories_processing_filling_way(),
            chunk_size=profile.get_vehicular_trajectories_processing_chunk_size(),
            start_time=profile.get_vehicular_trajectories_processing_start_time(),
            min_computing_capability=profile.get_min_computing_capability_of_vehicles(),
            max_computing_capability=profile.get_max_computing_capability_of_vehicles(),
            min_storage_capability=profile.get_min_storage_capability_of_vehicles(),
            max_storage_capability=profile.get_max_storage_capability_of_vehicles(),
            min_transmission_power=profile.get_min_transmission_power_of_vehicles(),
            max_transmission_power=profile.get_max_transmission_power_of_vehicles(),
            min_task_arrival_rate=profile.get_min_task_arrival_rate_of_vehicles(),
            max_task_arrival_rate=profile.get_max_task_arrival_rate_of_vehicles(),
            communication_range=profile.get_V2V_distance(),
            task_num=profile.get_task_num(),
            distribution=profile.get_vehicle_distribution(),
        )
        
        self._edge_nodes : List[edge_node] = generate_edge_nodes(
            edge_num=profile.get_edge_num(),
            file_name=profile.get_edge_mobility_file_name(),
            min_computing_capability=profile.get_min_computing_capability_of_edges(),
            max_computing_capability=profile.get_max_computing_capability_of_edges(),
            min_storage_capability=profile.get_min_storage_capability_of_edges(),
            max_storage_capability=profile.get_max_storage_capability_of_edges(),
            communication_range=profile.get_V2V_distance(),
            distribution=profile.get_edge_distribution(),
            time_slot_num=profile.get_slot_length(),
        )
        
        self._distance_matrix_between_edge_nodes = get_distance_matrix_between_edge_nodes(
            edge_nodes=self._edge_nodes,
        )
        self._wired_bandwidths_between_edge_node_and_other_edge_nodes = get_wired_bandwidth_between_edge_node_and_other_edge_nodes(
            edge_nodes=self._edge_nodes,
            weight=profile.get_I2I_transmission_weight(),
            transmission_rate=profile.get_I2I_transmission_rate(),
            distance_matrix=self._distance_matrix_between_edge_nodes,
        )
        
        self._cloud : cloud_server = generate_cloud(
            computing_capability=profile.get_cloud_computing_capability(),
            storage_capability=profile.get_cloud_storage_capability(),
            edge_node_num=profile.get_edge_num(),
            time_slot_num=profile.get_slot_length(),
            min_wired_bandwidth=profile.get_min_I2C_wired_bandwidth(),
            max_wired_bandwidth=profile.get_max_I2C_wired_bandwidth(),
            distribution=profile.get_cloud_distribution(),
        )
        
        self._client_vehicles : List[vehicle] = []
        self._server_vehicles : List[vehicle] = []
        
        self._client_vehicles, self._server_vehicles = get_client_and_server_vehicles(
            now=self._now,
            vehicles=self._vehicles,
        )
        
        self._client_vehicle_num = len(self._client_vehicles)
        self._server_vehicle_num = len(self._server_vehicles)

        self._distance_matrix_between_client_vehicles_and_server_vehicles : np.ndarray = get_distance_matrix_between_client_vehicles_and_server_vehicles(
            client_vehicles=self._client_vehicles,
            server_vehicles=self._server_vehicles,
            now=self._now,
        )
        self._distance_matrix_between_client_vehicles_and_edge_nodes : np.ndarray = get_distance_matrix_between_vehicles_and_edge_nodes(
            client_vehicles=self._client_vehicles,
            edge_nodes=self._edge_nodes,
            now=self._now,
        )
        self._vehicles_under_V2V_communication_range : np.ndarray = get_vehicles_under_V2V_communication_range(
            distance_matrix=self._distance_matrix_between_client_vehicles_and_server_vehicles,
            client_vehicles=self._client_vehicles,
            server_vehicles=self._server_vehicles,
        )
        self._vehicles_under_V2I_communication_range : np.ndarray = get_vehicles_under_V2I_communication_range(
            client_vehicles=self._client_vehicles,
            edge_nodes=self._edge_nodes,
            now=self._now,
        )
        
        self._channel_gains_between_client_vehicle_and_server_vehicles = obtain_channel_gains_between_client_vehicle_and_server_vehicles(
            distance_matrix=self._distance_matrix_between_client_vehicles_and_server_vehicles,
            client_vehicles=self._client_vehicles,
            server_vehicles=self._server_vehicles,
            path_loss_exponent=self._env_profile.get_path_loss_exponent(),
        )
        
        self._channel_gains_between_client_vehicle_and_edge_nodes = obtain_channel_gains_between_vehicles_and_edge_nodes(
            distance_matrix=self._distance_matrix_between_client_vehicles_and_edge_nodes,
            client_vehicles=self._client_vehicles,
            edge_nodes=self._edge_nodes,
            path_loss_exponent=self._env_profile.get_path_loss_exponent(),
        )
        
        return None
    
    def get_client_vehicle_num(self) -> int:
        return self._client_vehicle_num
    
    def get_server_vehicle_num(self) -> int:
        return self._server_vehicle_num
    
    def step(self, now_action : action) -> None:
        if self._now > self._end_time:
            self.save_results()
        else:
            
            client_vehicle_available_computing_capability = [client_vehicle.get_available_computing_capability(self._now) for client_vehicle in self._client_vehicles]
            server_vehicle_available_computing_capability = [server_vehicle.get_available_computing_capability(self._now) for server_vehicle in self._server_vehicles]
            edge_node_available_computing_capability = [edge_node.get_available_computing_capability(self._now) for edge_node in self._edge_nodes]
            cloud_available_computing_capability = self._cloud.get_available_computing_capability(self._now)
            
            if now_action.check_validity():
                
                for client_vehicle_index in range(self._client_vehicle_num):
                    client_vehicle : vehicle = self._client_vehicles[client_vehicle_index]
                    tasks : List[Tuple] = client_vehicle.get_tasks_by_time(self._now)
                    task_offloading_decision = now_action.get_offloading_decision_of_client_vehicle(client_vehicle_index=client_vehicle_index)
                    computing_resource_decision = now_action.get_computing_resource_decision_of_client_vehicle(client_vehicle_index=client_vehicle_index)
                    for task_tuple in tasks:
                        
                        self._task_num_at_time[self._now] += 1
                        
                        task_object : task = self._tasks[task_tuple[1]]
                        task_data_size = task_object.get_input_data_size()
                        task_cycles = task_object.get_cqu_cycles()
                        task_deadline = task_object.get_deadline()
                        
                        task_transmission_time = 0
                        task_computing_time = 0
                        task_processing_time = 0
                        task_during_time = 0
                        
                        if task_offloading_decision == 0:  # processing at local                       
                            self._task_processed_at_local_at_time[self._now] += 1
                            
                            allocated_computing_capability = \
                                client_vehicle_available_computing_capability[client_vehicle_index] * computing_resource_decision
                            task_computing_time = obtain_computing_time(
                                data_size=task_data_size,
                                per_cycle_required=task_cycles,
                                computing_capability=allocated_computing_capability
                            )
                            task_processing_time = task_transmission_time + task_computing_time
                            
                            if task_processing_time <= task_deadline:
                                self._task_successfully_processed_num_at_time[self._now] += 1
                            
                            task_during_time = np.floor(task_computing_time).astype('int')
                            self._client_vehicles[client_vehicle_index].set_consumed_computing_capability(
                                consumed_computing_capability=allocated_computing_capability,
                                now=self._now,
                                duration=task_during_time,
                            )
                            self._client_vehicles[client_vehicle_index].set_consumed_storage_capability(
                                consumed_storage_capability=task_data_size,
                                now=self._now,
                                duration=task_during_time,
                            )
                                
                        elif task_offloading_decision >= 1 and \
                            task_offloading_decision <= self._server_vehicle_num:  # processing at server vehicle
                            self._task_processed_at_vehicle_at_time[self._now] += 1
                            server_vehicle_index = task_offloading_decision - 1
                            if self._vehicles_under_V2V_communication_range[client_vehicle_index][server_vehicle_index] == 1:
                                
                                task_transmission_time = self.obtain_V2V_transmission_time(
                                    now_action=now_action,
                                    client_vehicle_index=client_vehicle_index,
                                    server_vehicle_index=server_vehicle_index,
                                    task_data_size=task_data_size,
                                )
                                
                                allocated_computing_capability = \
                                    server_vehicle_available_computing_capability[server_vehicle_index] * computing_resource_decision
                                task_computing_time = obtain_computing_time(
                                    data_size=task_data_size,
                                    per_cycle_required=task_cycles,
                                    computing_capability=allocated_computing_capability
                                )
                                task_processing_time = task_transmission_time + task_computing_time
                                
                                if task_processing_time <= task_deadline:
                                    self._task_successfully_processed_num_at_time[self._now] += 1
                                
                                task_computing_start_time = self._now + np.ceil(task_transmission_time)
                                task_during_time = np.floor(task_computing_time).astype('int')
                                self._server_vehicles[server_vehicle_index] : vehicle .set_consumed_computing_capability(
                                    consumed_computing_capability=allocated_computing_capability,
                                    now=task_computing_start_time,
                                    duration=task_during_time,
                                )
                                self._server_vehicles[server_vehicle_index] : vehicle .set_consumed_storage_capability(
                                    consumed_storage_capability=task_data_size,
                                    now=task_computing_start_time,
                                    duration=task_during_time,
                                )
                                
                            else:
                                pass
                                # print("V2V communication range error")
                                # print("\nclient_vehicle_index", client_vehicle_index)
                                # print("\nserver_vehicle_index", server_vehicle_index)
                                # print("\nself._vehicles_under_V2V_communication_range", self._vehicles_under_V2V_communication_range)
                                # print("\nself._vehicles_under_V2V_communication_range[client_vehicle_index][server_vehicle_index]", self._vehicles_under_V2V_communication_range[client_vehicle_index][server_vehicle_index])
                                # raise Exception("V2V communication range error")
                        elif task_offloading_decision >= self._server_vehicle_num + 1 and \
                            task_offloading_decision <= self._server_vehicle_num + self._env_profile.get_edge_num():  # processing at edge
                            self._task_processed_at_edge_at_time[self._now] += 1
                            
                            edge_node_index = task_offloading_decision - self._server_vehicle_num - 1
                            if self._vehicles_under_V2I_communication_range[client_vehicle_index][edge_node_index] == 1: # the client vehicle is under the communication range of the edge node
                                self._task_processed_at_local_edge_at_time[self._now] += 1
                                
                                task_transmission_time = self.obtain_V2I_transmission_time(
                                    now_action=now_action,
                                    client_vehicle_index=client_vehicle_index,
                                    edge_node_index=edge_node_index,
                                    task_data_size=task_data_size,
                                )
                                
                                allocated_computing_capability = \
                                    edge_node_available_computing_capability[edge_node_index] * computing_resource_decision
                                task_computing_time = obtain_computing_time(
                                    data_size=task_data_size,
                                    per_cycle_required=task_cycles,
                                    computing_capability=allocated_computing_capability
                                )
                                
                                task_processing_time = task_transmission_time + task_computing_time
                                
                                if task_processing_time <= task_deadline:
                                    self._task_successfully_processed_num_at_time[self._now] += 1
                                    
                                task_computing_start_time = self._now + np.ceil(task_transmission_time)
                                task_during_time = np.floor(task_computing_time)
                                self._edge_nodes[edge_node_index] : edge_node .set_consumed_computing_capability(
                                    consumed_computing_capability=allocated_computing_capability,
                                    now=task_computing_start_time,
                                    duration=task_during_time,
                                )
                                self._edge_nodes[edge_node_index] : edge_node .set_consumed_storage_capability(
                                    consumed_storage_capability=task_data_size,
                                    now=task_computing_start_time,
                                    duration=task_during_time,
                                )
                                
                            else:  # the client vehicle is not under the communication range of the edge node
                                self._task_processed_at_other_edge_at_time[self._now] += 1
                                
                                task_v2i_transmission_time = 0
                                task_i2i_transmission_time = 0
                                
                                for other_edge_node_index in range(self._env_profile.get_edge_num()):
                                    if other_edge_node_index != edge_node_index:
                                        if self._vehicles_under_V2I_communication_range[client_vehicle_index][other_edge_node_index] == 1:
                                            task_v2i_transmission_time = self.obtain_V2I_transmission_time(
                                                now_action=now_action,
                                                client_vehicle_index=client_vehicle_index,
                                                edge_node_index=other_edge_node_index,
                                                task_data_size=task_data_size,
                                            )
                                            task_i2i_transmission_time = obtain_wired_transmission_time(
                                                transmission_rate=self._wired_bandwidths_between_edge_node_and_other_edge_nodes[edge_node_index][other_edge_node_index],
                                                data_size=task_data_size,
                                            )
                                            break
                                
                                task_transmission_time = task_v2i_transmission_time + task_i2i_transmission_time
                                
                                allocated_computing_capability = \
                                    edge_node_available_computing_capability[edge_node_index] * computing_resource_decision
                                
                                task_computing_time = obtain_computing_time(
                                    data_size=task_data_size,
                                    per_cycle_required=task_cycles,
                                    computing_capability=allocated_computing_capability
                                )
                                
                                task_processing_time = task_transmission_time + task_computing_time
                                
                                if task_processing_time <= task_deadline:
                                    self._task_successfully_processed_num_at_time[self._now] += 1
                                    
                                task_computing_start_time = self._now + np.ceil(task_transmission_time)
                                task_during_time = np.floor(task_computing_time)
                                self._edge_nodes[edge_node_index] : edge_node .set_consumed_computing_capability(
                                    consumed_computing_capability=allocated_computing_capability,
                                    now=task_computing_start_time,
                                    duration=task_during_time,
                                )
                                self._edge_nodes[edge_node_index] : edge_node .set_consumed_storage_capability(
                                    consumed_storage_capability=task_data_size,
                                    now=task_computing_start_time,
                                    duration=task_during_time,
                                )
                                
                        elif task_offloading_decision == self._server_vehicle_num + self._env_profile.get_edge_num() + 1:  # processing at the cloud
                            
                            self._task_processed_at_cloud_at_time[self._now] += 1
                            
                            task_v2i_transmission_time = 0
                            task_i2c_transmission_time = 0
                            
                            for edge_node_index in range(self._env_profile.get_edge_num()):
                                if self._vehicles_under_V2I_communication_range[client_vehicle_index][edge_node_index] == 1:
                                    task_v2i_transmission_time = self.obtain_V2I_transmission_time(
                                        now_action=now_action,
                                        client_vehicle_index=client_vehicle_index,
                                        edge_node_index=edge_node_index,
                                        task_data_size=task_data_size,
                                    )
                                    task_i2c_transmission_time = obtain_wired_transmission_time(
                                        transmission_rate=self._cloud.get_wired_bandwidth_between_edge_node_and_cloud(edge_node_index=edge_node_index),
                                        data_size=task_data_size,
                                    )
                                    break
                                
                            task_transmission_time = task_v2i_transmission_time + task_i2c_transmission_time
                            
                            allocated_computing_capability = \
                                cloud_available_computing_capability * computing_resource_decision
                            
                            task_computing_time = obtain_computing_time(
                                data_size=task_data_size,
                                per_cycle_required=task_cycles,
                                computing_capability=allocated_computing_capability
                            )
                            
                            task_processing_time = task_transmission_time + task_computing_time
                            if task_processing_time <= task_deadline:
                                self._task_successfully_processed_num_at_time[self._now] += 1
                                
                            task_computing_start_time = self._now + np.ceil(task_transmission_time)
                            task_during_time = np.floor(task_computing_time)
                            self._cloud : cloud_server .set_consumed_computing_capability(
                                consumed_computing_capability=allocated_computing_capability,
                                now=task_computing_start_time,
                                duration=task_during_time,
                            )
                            
                            self._cloud : cloud_server .set_consumed_storage_capability(
                                consumed_storage_capability=task_data_size,
                                now=task_computing_start_time,
                                duration=task_during_time,
                            )
            
            self.update()
                            
        return None
    
    def obtain_V2V_transmission_time(
        self, 
        now_action : action, 
        client_vehicle_index : int, 
        server_vehicle_index : int, 
        task_data_size : float,
    ) -> float:
        
        intra_vehicle_interference = 0
        client_vehicle_index_list = now_action.get_offloading_decision_at_server_vehicle(server_vehicle_index)
        for other_client_vehicle_index in client_vehicle_index_list:
            if other_client_vehicle_index != client_vehicle_index:
                if np.abs(self._channel_gains_between_client_vehicle_and_server_vehicles[other_client_vehicle_index][server_vehicle_index]) ** 2 < \
                    np.abs(self._channel_gains_between_client_vehicle_and_server_vehicles[client_vehicle_index][server_vehicle_index]) ** 2:
                    intra_vehicle_interference += \
                        np.abs(self._channel_gains_between_client_vehicle_and_server_vehicles[other_client_vehicle_index][server_vehicle_index]) ** 2 * \
                            self._client_vehicles[other_client_vehicle_index].get_transmission_power()
                            
        inter_vehicle_interference = 0
        for other_server_vehicle_index in range(self._server_vehicle_num):
            if other_server_vehicle_index != server_vehicle_index:
                client_vehicle_index_list = now_action.get_offloading_decision_at_server_vehicle(other_server_vehicle_index)
                for other_client_vehicle_index in client_vehicle_index_list:
                    if other_client_vehicle_index != client_vehicle_index:
                        inter_vehicle_interference += \
                            np.abs(self._channel_gains_between_client_vehicle_and_server_vehicles[other_client_vehicle_index][server_vehicle_index]) ** 2 * \
                                self._client_vehicles[other_client_vehicle_index].get_transmission_power()
        
        sinr = compute_V2V_SINR(
            white_gaussian_noise=self._env_profile.get_white_gaussian_noise(),
            channel_gain=self._channel_gains_between_client_vehicle_and_server_vehicles[client_vehicle_index][server_vehicle_index],
            transmission_power=self._client_vehicles[client_vehicle_index].get_transmission_power(),
            intra_vehicle_interference=intra_vehicle_interference,
            inter_vehicle_interference=inter_vehicle_interference,
        )
        
        transmission_rate = compute_transmission_rate(
            SINR=sinr,
            bandwidth=self._env_profile.get_V2V_bandwidth(),
        )
        
        task_transmission_time = obtain_transmission_time(
            transmission_rate=transmission_rate,
            data_size=task_data_size,
        )
        
        return task_transmission_time
    
    def obtain_V2I_transmission_time(
        self, 
        now_action : action, 
        client_vehicle_index : int, 
        edge_node_index : int, 
        task_data_size : float
    ) -> float:
        
        intra_edge_interference = 0
        client_vehicle_index_list = now_action.get_offloading_decision_at_edge_node(edge_node_index)
        for other_client_vehicle_index in client_vehicle_index_list:
            if other_client_vehicle_index != client_vehicle_index:
                if np.abs(self._channel_gains_between_client_vehicle_and_edge_nodes[other_client_vehicle_index][edge_node_index]) ** 2 < \
                    np.abs(self._channel_gains_between_client_vehicle_and_edge_nodes[client_vehicle_index][edge_node_index]) ** 2:
                    intra_edge_interference += \
                        np.abs(self._channel_gains_between_client_vehicle_and_edge_nodes[other_client_vehicle_index][edge_node_index]) ** 2 * \
                            self._client_vehicles[other_client_vehicle_index].get_transmission_power()
        
        inter_edge_interference = 0
        for other_edge_node_index in range(self._env_profile.get_edge_num()):
            if other_edge_node_index != edge_node_index:
                client_vehicle_index_list = now_action.get_offloading_decision_at_edge_node(other_edge_node_index)
                for other_client_vehicle_index in client_vehicle_index_list:
                    if other_client_vehicle_index != client_vehicle_index:
                        inter_edge_interference += \
                            np.abs(self._channel_gains_between_client_vehicle_and_edge_nodes[other_client_vehicle_index][edge_node_index]) ** 2 * \
                                self._client_vehicles[other_client_vehicle_index].get_transmission_power()
        
        sinr = compute_V2I_SINR(
            white_gaussian_noise=self._env_profile.get_white_gaussian_noise(),
            channel_gain=self._channel_gains_between_client_vehicle_and_edge_nodes[client_vehicle_index][edge_node_index],
            transmission_power=self._client_vehicles[client_vehicle_index].get_transmission_power(),
            intra_edge_interference=intra_edge_interference,
            inter_edge_interference=inter_edge_interference,
        )
        
        transmission_rate = compute_transmission_rate(
            SINR=sinr,
            bandwidth=self._env_profile.get_V2I_bandwidth(),
        )
        
        task_transmission_time = obtain_transmission_time(
            transmission_rate=transmission_rate,
            data_size=task_data_size,
        )
        
        return task_transmission_time
    
    def update(self) -> None:
        
        self._now += 1
        
        self._client_vehicles, self._server_vehicles = get_client_and_server_vehicles(
            now=self._now,
            vehicles=self._vehicles,
        )
        
        self._client_vehicle_num = len(self._client_vehicles)
        self._server_vehicle_num = len(self._server_vehicles)

        self._distance_matrix_between_client_vehicles_and_server_vehicles : np.ndarray = get_distance_matrix_between_client_vehicles_and_server_vehicles(
            client_vehicles=self._client_vehicles,
            server_vehicles=self._server_vehicles,
            now=self._now,
        )
        self._distance_matrix_between_client_vehicles_and_edge_nodes : np.ndarray = get_distance_matrix_between_vehicles_and_edge_nodes(
            client_vehicles=self._client_vehicles,
            edge_nodes=self._edge_nodes,
            now=self._now,
        )
        self._vehicles_under_V2V_communication_range : np.ndarray = get_vehicles_under_V2V_communication_range(
            distance_matrix=self._distance_matrix_between_client_vehicles_and_server_vehicles,
            client_vehicles=self._client_vehicles,
            server_vehicles=self._server_vehicles,
        )
        self._vehicles_under_V2I_communication_range : np.ndarray = get_vehicles_under_V2I_communication_range(
            client_vehicles=self._client_vehicles,
            edge_nodes=self._edge_nodes,
            now=self._now,
        )
        
        self._channel_gains_between_client_vehicle_and_server_vehicles = obtain_channel_gains_between_client_vehicle_and_server_vehicles(
            distance_matrix=self._distance_matrix_between_client_vehicles_and_server_vehicles,
            client_vehicles=self._client_vehicles,
            server_vehicles=self._server_vehicles,
            path_loss_exponent=self._env_profile.get_path_loss_exponent(),
        )
        
        self._channel_gains_between_client_vehicle_and_edge_nodes = obtain_channel_gains_between_vehicles_and_edge_nodes(
            distance_matrix=self._distance_matrix_between_client_vehicles_and_edge_nodes,
            client_vehicles=self._client_vehicles,
            edge_nodes=self._edge_nodes,
            path_loss_exponent=self._env_profile.get_path_loss_exponent(),
        )
        return None
    
    def save(self, file_name : str):
        pickle.dump(self, open(file_name, "wb"))
    
    def load(self, file_name : str):
        return pickle.load(open(file_name, "rb"))
    
    def save_results(self):
        
        """add results to the file"""
        try:
            with open(self._resutls_file_name, "a+") as f:
                f.write("task_num_at_time: " + str(self._task_num_at_time) + "\n" \
                    + "average_processing_time_at_time: " + str(self._average_processing_time_at_time) + "\n" \
                    + "average_transmission_time_at_time: " + str(self._average_transmission_time_at_time) + "\n" \
                    + "average_computing_time_at_time: " + str(self._average_computing_time_at_time) + "\n" \
                    + "average_computing_capability_at_time: " + str(self._average_computing_capability_at_time) + "\n" \
                    + "average_storage_capability_at_time: " + str(self._average_storage_capability_at_time) + "\n" \
                    + "task_processed_at_local_at_time: " + str(self._task_processed_at_local_at_time) + "\n" \
                    + "task_processed_at_vehicle_at_time: " + str(self._task_processed_at_vehicle_at_time) + "\n" \
                    + "task_processed_at_edge_at_time: " + str(self._task_processed_at_edge_at_time) + "\n" \
                    + "task_processed_at_local_edge_at_time: " + str(self._task_processed_at_local_edge_at_time) + "\n" \
                    + "task_processed_at_other_edge_at_time: " + str(self._task_processed_at_other_edge_at_time) + "\n" \
                    + "task_processed_at_cloud_at_time: " + str(self._task_processed_at_cloud_at_time) + "\n" \
                    + "task_successfully_processed_num_at_time: " + str(self._task_successfully_processed_num_at_time) + "\n" )
        except:
            raise Exception("No such file: " + self._resutls_file_name)
        return None