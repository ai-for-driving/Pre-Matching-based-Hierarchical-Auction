class env_profile(object):
    def __init__(
        self,
        slot_length: int,
        task_num: int,
        task_distribution: str,
        min_input_data_size_of_tasks: float,
        max_input_data_size_of_tasks: float,
        min_cqu_cycles_of_tasks: float,
        max_cqu_cycles_of_tasks: float,
        min_deadline_of_tasks: float,
        max_deadline_of_tasks: float,
        vehicle_num: int,
        vehicle_mobility_file_name: str,
        min_computing_capability_of_vehicles: float,
        max_computing_capability_of_vehicles: float,
        min_storage_capability_of_vehicles: float,
        max_storage_capability_of_vehicles: float,
        min_transmission_power_of_vehicles: float,
        max_transmission_power_of_vehicles: float,
        V2V_distance: float,
        min_task_arrival_rate_of_vehicles: float,
        max_task_arrival_rate_of_vehicles: float,
        vehicle_distribution: str,
        edge_num: int,
        I2I_transmission_rate: float,
        I2I_transmission_weight: float,
        min_computing_capability_of_edges: float,
        max_computing_capability_of_edges: float,
        min_storage_capability_of_edges: float,
        max_storage_capability_of_edges: float,
        min_communication_range_of_edges: float,
        max_communication_range_of_edges: float,
        edge_mobility_file_name: str,
        edge_distribution: str,
        cloud_computing_capability: float,
        cloud_storage_capability: float,
        min_I2C_wired_bandwidth: float,
        max_I2C_wired_bandwidth: float,
        cloud_distribution: str,
    ) -> None:
        self._slot_length: int = slot_length
        self._task_num: int = task_num
        self._task_distribution: str = task_distribution
        self._min_input_data_size_of_tasks: float = min_input_data_size_of_tasks
        self._max_input_data_size_of_tasks: float = max_input_data_size_of_tasks
        self._min_cqu_cycles_of_tasks: float = min_cqu_cycles_of_tasks
        self._max_cqu_cycles_of_tasks: float = max_cqu_cycles_of_tasks
        self._min_deadline_of_tasks: float = min_deadline_of_tasks
        self._max_deadline_of_tasks: float = max_deadline_of_tasks
        self._vehicle_num: int = vehicle_num
        self._vehicle_mobility_file_name: str = vehicle_mobility_file_name
        self._min_computing_capability_of_vehicles: float = min_computing_capability_of_vehicles
        self._max_computing_capability_of_vehicles: float = max_computing_capability_of_vehicles
        self._min_storage_capability_of_vehicles: float = min_storage_capability_of_vehicles
        self._max_storage_capability_of_vehicles: float = max_storage_capability_of_vehicles
        self._min_transmission_power_of_vehicles: float = min_transmission_power_of_vehicles
        self._max_transmission_power_of_vehicles: float = max_transmission_power_of_vehicles
        self._V2V_distance: float = V2V_distance
        self._min_task_arrival_rate_of_vehicles: float = min_task_arrival_rate_of_vehicles
        self._max_task_arrival_rate_of_vehicles: float = max_task_arrival_rate_of_vehicles
        self._vehicle_distribution: str = vehicle_distribution
        self._edge_num: int = edge_num
        self._min_computing_capability_of_edges: float = min_computing_capability_of_edges
        self._max_computing_capability_of_edges: float = max_computing_capability_of_edges
        self._min_storage_capability_of_edges: float = min_storage_capability_of_edges
        self._max_storage_capability_of_edges: float = max_storage_capability_of_edges
        self._min_communication_range_of_edges: float = min_communication_range_of_edges
        self._max_communication_range_of_edges: float = max_communication_range_of_edges
        self._edge_mobility_file_name: str = edge_mobility_file_name
        self._I2I_transmission_rate: float = I2I_transmission_rate
        self._I2I_transmission_weight: float = I2I_transmission_weight
        self._edge_distribution: str = edge_distribution
        self._cloud_computing_capability: float = cloud_computing_capability
        self._cloud_storage_capability: float = cloud_storage_capability
        self._min_I2C_wired_bandwidth: float = min_I2C_wired_bandwidth
        self._max_I2C_wired_bandwidth: float = max_I2C_wired_bandwidth
        self._cloud_distribution: str = cloud_distribution
        
        
    def get_slot_length(self) -> int:
        return self._slot_length
    
    def get_task_num(self) -> int:  
        return self._task_num
    
    def get_task_distribution(self) -> str:
        return self._task_distribution
    
    def get_min_input_data_size_of_tasks(self) -> float:
        return self._min_input_data_size_of_tasks
    
    def get_max_input_data_size_of_tasks(self) -> float:
        return self._max_input_data_size_of_tasks
    
    def get_min_cqu_cycles_of_tasks(self) -> float:
        return self._min_cqu_cycles_of_tasks
    
    def get_max_cqu_cycles_of_tasks(self) -> float:
        return self._max_cqu_cycles_of_tasks
    
    def get_min_deadline_of_tasks(self) -> float:
        return self._min_deadline_of_tasks
    
    def get_max_deadline_of_tasks(self) -> float:
        return self._max_deadline_of_tasks
    
    def get_vehicle_num(self) -> int:
        return self._vehicle_num
    
    def get_vehicle_mobility_file_name(self) -> str:
        return self._vehicle_mobility_file_name
    
    def get_min_computing_capability_of_vehicles(self) -> float:
        return self._min_computing_capability_of_vehicles
    
    def get_max_computing_capability_of_vehicles(self) -> float:
        return self._max_computing_capability_of_vehicles
    
    def get_min_storage_capability_of_vehicles(self) -> float:
        return self._min_storage_capability_of_vehicles
    
    def get_max_storage_capability_of_vehicles(self) -> float:
        return self._max_storage_capability_of_vehicles
    
    def get_min_transmission_power_of_vehicles(self) -> float:
        return self._min_transmission_power_of_vehicles
    
    def get_max_transmission_power_of_vehicles(self) -> float:
        return self._max_transmission_power_of_vehicles
    
    def get_V2V_distance(self) -> float:
        return self._V2V_distance
    
    def get_min_task_arrival_rate_of_vehicles(self) -> float:
        return self._min_task_arrival_rate_of_vehicles
    
    def get_max_task_arrival_rate_of_vehicles(self) -> float:
        return self._max_task_arrival_rate_of_vehicles
    
    def get_vehicle_distribution(self) -> str:
        return self._vehicle_distribution
    
    def get_edge_num(self) -> int:
        return self._edge_num
    
    def get_min_computing_capability_of_edges(self) -> float:
        return self._min_computing_capability_of_edges
    
    def get_max_computing_capability_of_edges(self) -> float:
        return self._max_computing_capability_of_edges
    
    def get_min_storage_capability_of_edges(self) -> float:
        return self._min_storage_capability_of_edges
    
    def get_max_storage_capability_of_edges(self) -> float:
        return self._max_storage_capability_of_edges
    
    def get_min_communication_range_of_edges(self) -> float:
        return self._min_communication_range_of_edges
    
    def get_max_communication_range_of_edges(self) -> float:
        return self._max_communication_range_of_edges
    
    def get_I2I_transmission_rate(self) -> float:
        return self._I2I_transmission_rate
    
    def get_I2I_transmission_weight(self) -> float:
        return self._I2I_transmission_weight
    
    def get_edge_mobility_file_name(self) -> str:
        return self._edge_mobility_file_name
    
    def get_edge_distribution(self) -> str:
        return self._edge_distribution
    
    def get_cloud_computing_capability(self) -> float:
        return self._cloud_computing_capability
    
    def get_cloud_storage_capability(self) -> float:
        return self._cloud_storage_capability
    
    def get_min_I2C_wired_bandwidth(self) -> float:
        return self._min_I2C_wired_bandwidth
    
    def get_max_I2C_wired_bandwidth(self) -> float:
        return self._max_I2C_wired_bandwidth
    
    def get_cloud_distribution(self) -> str:
        return self._cloud_distribution
    