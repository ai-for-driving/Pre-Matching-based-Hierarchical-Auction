from env_profile import env_profile
from Objectives.task import task, generate_task_set
from Objectives.vehicle import vehicle, generate_vehicles
from Objectives.edge_node import edge_node, generate_edge_nodes
from Objectives.cloud_server import cloud_server, generate_cloud
from typing import List
import pickle
from strategy import action

class env(object):
    
    def __init__(
        self,
        profile: env_profile
    ) -> None:
        self._env_profile = profile
        self._now = 0
        self._end_time = profile.get_slot_length - 1
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
        self._edge_nodes : List[edge_node] = generate_edge_nodes(
            file_name=profile.get_edge_mobility_file_name(),
            min_computing_capability=profile.get_min_computing_capability_of_edges(),
            max_computing_capability=profile.get_max_computing_capability_of_edges(),
            min_storage_capability=profile.get_min_storage_capability_of_edges(),
            max_storage_capability=profile.get_max_storage_capability_of_edges(),
            communication_range=profile.get_V2V_distance(),
            distribution=profile.get_edge_distribution(),
        )
        self._cloud : cloud_server = generate_cloud(
            computing_capability=profile.get_cloud_computing_capability(),
            storage_capability=profile.get_cloud_storage_capability(),
            time_slot_num=profile.get_slot_length(),
            min_wired_bandwidth=profile.get_min_wired_bandwidth(),
            max_wired_bandwidth=profile.get_max_wired_bandwidth(),
            distribution=profile.get_cloud_distribution(),
        )
        
    
    def step(self, action : action) -> None:
        if self._now > self._end_time:
            pass
        else:
            if action.check_validity():
                pass
        return None        
    
    def save(self, file_name : str):
        pickle.dump(self, open(file_name, "wb"))
    
    def load(self, file_name : str):
        return pickle.load(open(file_name, "rb"))