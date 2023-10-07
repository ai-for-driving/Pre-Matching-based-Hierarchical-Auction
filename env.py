from env_profile import env_profile
from Objectives.task import task, generate_task_set
from Objectives.vehicle import vehicle, generate_vehicles
from Objectives.edge_node import edge_node, generate_edge_nodes, get_wired_bandwidth_between_edge_node_and_other_edge_nodes
from Objectives.cloud_server import cloud_server, generate_cloud
from Utilities.vehicle_classification import get_client_and_server_vehicles
from typing import List, Tuple
import time
import pickle
from strategy import action
from Utilities.time_calculation import obtain_computing_time

class env(object):
    
    def __init__(
        self,
        profile: env_profile
    ) -> None:
        self._env_profile = profile
        self._now = 0
        self._end_time = profile.get_slot_length - 1
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
        
        self._resutls_file_name = "results/" \
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
            file_name=profile.get_vehicle_mobility_file_name(),
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
        
        self._client_vehicles : List[vehicle] = []
        self._server_vehicles : List[vehicle] = []
        
        self._client_vehicles, self._server_vehicles = get_client_and_server_vehicles(
            now=self._now,
            vehicles=self._vehicles,
        )
        
        self._client_vehicle_num = len(self._client_vehicles)
        self._server_vehicle_num = len(self._server_vehicles)
        
        self._edge_nodes : List[edge_node] = generate_edge_nodes(
            file_name=profile.get_edge_mobility_file_name(),
            min_computing_capability=profile.get_min_computing_capability_of_edges(),
            max_computing_capability=profile.get_max_computing_capability_of_edges(),
            min_storage_capability=profile.get_min_storage_capability_of_edges(),
            max_storage_capability=profile.get_max_storage_capability_of_edges(),
            communication_range=profile.get_V2V_distance(),
            distribution=profile.get_edge_distribution(),
        )
        
        self._wired_bandwidths_between_edge_node_and_other_edge_nodes = get_wired_bandwidth_between_edge_node_and_other_edge_nodes(
            edge_nodes=self._edge_nodes,
            weight=profile.get_I2I_transmission_weight(),
            transmission_rate=profile.get_I2I_transmission_rate(),
        )
        
        self._cloud : cloud_server = generate_cloud(
            computing_capability=profile.get_cloud_computing_capability(),
            storage_capability=profile.get_cloud_storage_capability(),
            time_slot_num=profile.get_slot_length(),
            min_wired_bandwidth=profile.get_min_I2C_wired_bandwidth(),
            max_wired_bandwidth=profile.get_max_I2C_wired_bandwidth(),
            distribution=profile.get_cloud_distribution(),
        )
        return None
    
    def step(self, now_action : action) -> None:
        if self._now > self._end_time:
            self.save_results()
        else:
            if action.check_validity():
                
                for client_vehicle in self._client_vehicles:
                    tasks : List[Tuple] = client_vehicle.get_tasks_by_time(self._now)
                    task_offloading_decision = now_action.get_offloading_decision_of_client_vehicle(client_vehicle)
                    computing_resource_decision = now_action.get_computing_resource_decision_of_client_vehicle(client_vehicle)
                    if task_offloading_decision == 0:  # processing at local
                        for task_tuple in tasks:
                            self._task_num_at_time[self._now] += 1
                            self._task_processed_at_local_at_time[self._now] += 1
                            
                            task_object : task = task_tuple[1]
                            task_data_size = task_object.get_input_data_size()
                            task_cycles = task_object.get_cqu_cycles()
                            task_deadline = task_object.get_deadline()
                            
                            task_transmission_time = 0
                            task_computing_time = obtain_computing_time(
                                data_size=task_data_size,
                                per_cycle_required=task_cycles,
                                computing_capability=client_vehicle.get_avaliable_computing_capability() * computing_resource_decision,
                            )
                            task_processing_time = task_transmission_time + task_computing_time
                            
                            if task_processing_time <= task_deadline:
                                self._task_successfully_processed_num_at_time[self._now] += 1
                                
                            
                                
                    elif task_offloading_decision >= 1 and task_offloading_decision <= self._server_vehicle_num:  # processing at server vehicle
                        
                        pass
                    elif task_offloading_decision >= self._server_vehicle_num + 1 and \
                        task_offloading_decision <= self._server_vehicle_num + self._env_profile.get_edge_num():  # processing at edge
                        pass
                    elif task_offloading_decision == self._server_vehicle_num + self._env_profile.get_edge_num() + 1:  # processing at the cloud
                        pass
        return None
    
    def update(self) -> None:
        self._now += 1
        self._client_vehicles, self._server_vehicles = get_client_and_server_vehicles(
            now=self._now,
            vehicles=self._vehicles,
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