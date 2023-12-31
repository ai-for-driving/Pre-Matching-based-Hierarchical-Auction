import random
from typing import List
from Objects.task_object import task
from Objects.mobility_object import mobility
from Objects.vehicle_object import vehicle
from Objects.edge_node_object import edge_node
from Objects.cloud_server_object import cloud_server
from Utilities.vehicular_trajectories_processing import TrajectoriesProcessing
from Utilities.wired_bandwidth import get_wired_bandwidth_between_edge_nodes_and_the_cloud

def generate_task_set(
    task_num: int,
    distribution: str,
    min_input_data_size: float,     # in MB
    max_input_data_size: float,     # in MB
    min_cqu_cycles: float,          # cycles/bit
    max_cqu_cycles: float,          # cycles/bit
    min_deadline: float,            # seconds
    max_deadline: float,            # seconds
):
    '''
    Generate a task set with given parameters
    Args:
        task_num: number of tasks
        distribution: distribution of the task parameters
        min_input_data_size: minimum input data size
        max_input_data_size: maximum input data size
        min_cqu_cycles: minimum cqu cycles
        max_cqu_cycles: maximum cqu cycles
        min_deadline: minimum deadline
        max_deadline: maximum deadline
    Returns:
        tasks: a list of tasks
    '''
    tasks = list()
    if distribution == "uniform":
        for _ in range(task_num):
            t = task(
                input_data_size = random.uniform(min_input_data_size, max_input_data_size),
                cqu_cycles = random.uniform(min_cqu_cycles, max_cqu_cycles),
                deadline = random.uniform(min_deadline, max_deadline),
            )
            tasks.append(t)
        return tasks
    elif distribution == "normal":
        for _ in range(task_num):
            t = task(
                input_data_size = random.normalvariate((min_input_data_size + max_input_data_size)/2, (max_input_data_size - min_input_data_size)/6),
                cqu_cycles = random.normalvariate((min_cqu_cycles + max_cqu_cycles)/2, (max_cqu_cycles - min_cqu_cycles)/6),
                deadline = random.normalvariate((min_deadline + max_deadline)/2, (max_deadline - min_deadline)/6),
            )
            tasks.append(t)
        return tasks
    else:
        raise ValueError("Distribution not supported")
    
    
def generate_vehicles(
    vehicle_num: int,
    slot_length: int,
    file_name_key: str,
    slection_way: str,
    filling_way: str,
    chunk_size: int,
    start_time: str,
    min_computing_capability: float,        # GHz
    max_computing_capability: float,        # GHz
    min_storage_capability: float,          # MB
    max_storage_capability: float,          # MB
    min_transmission_power: float,          # mW
    max_transmission_power: float,          # mW
    communication_range: float,             # meters
    min_task_arrival_rate: float,           # tasks/s
    max_task_arrival_rate: float,           # tasks/s
    task_num: int,
    distribution: str,
) -> tuple[float, float, float, float, List[vehicle]]:

    trajectoriesProcessing = TrajectoriesProcessing(
        file_name_key=file_name_key,
        vehicle_number=vehicle_num,
        start_time=start_time,
        slot_length=slot_length,
        slection_way=slection_way,
        filling_way=filling_way,
        chunk_size=chunk_size,
    )
    min_map_x, max_map_x, min_map_y, max_map_y = trajectoriesProcessing.processing()
    
    mobilities_list : List[List[mobility]] = trajectoriesProcessing.get_vehicle_mobilities()
    
    vehicles = []
    if distribution == "uniform":
        for _ in range(vehicle_num):
            vehicles.append(
                vehicle(
                    mobilities=mobilities_list[_],
                    computing_capability=random.uniform(min_computing_capability, max_computing_capability),
                    storage_capability=random.uniform(min_storage_capability, max_storage_capability),
                    transmission_power=random.uniform(min_transmission_power, max_transmission_power),
                    time_slot_num=slot_length,
                    communication_range=communication_range,
                    task_arrival_rate=random.uniform(min_task_arrival_rate, max_task_arrival_rate),
                    task_num=task_num,
                )
            )
        return min_map_x, max_map_x, min_map_y, max_map_y, vehicles
    else:
        raise Exception("distribution not supported")
    
    
def generate_edge_nodes(
    edge_num: int,
    min_map_x: float,
    max_map_x: float,
    min_map_y: float,
    max_map_y: float,
    min_computing_capability: float,        # GHz   
    max_computing_capability: float,        # GHz
    min_storage_capability: float,          # MB
    max_storage_capability: float,          # MB
    communication_range : float,            # meters
    time_slot_num: int,
    distribution: str,
) -> List[edge_node]:
    edge_nodes = []
    edge_node_x = [random.uniform(min_map_x, max_map_x) for _ in range(edge_num)]
    edge_node_y = [random.uniform(min_map_y, max_map_y) for _ in range(edge_num)]
    if distribution == "uniform" :
        for _ in range(edge_num):
            mobility_obj = mobility(
                x = edge_node_x[_], 
                y = edge_node_y[_], 
                speed = 0, 
                acceleration = 0,
                direction = 0,
                time = 0
            )
            computing_capability = random.uniform(min_computing_capability,max_computing_capability)
            storage_capability = random.uniform(min_storage_capability,max_storage_capability)
            edge_node_obj = edge_node(
                edge_node_mobility = mobility_obj, 
                computing_capability = computing_capability, 
                storage_capability = storage_capability,
                communication_range = communication_range,
                time_slot_num = time_slot_num)
            edge_nodes.append(edge_node_obj)
        return edge_nodes 
    else:
        raise Exception("distribution is not supported")
        
        
def generate_cloud(
    computing_capability: float,        # GHz
    storage_capability: float,          # MB
    edge_node_num: int,
    time_slot_num: int,
    min_wired_bandwidth: float,         # Mbps
    max_wired_bandwidth: float,         # Mbps
    distribution: str,
) -> cloud_server:
    if distribution == "uniform":
        wired_bandwidths = get_wired_bandwidth_between_edge_nodes_and_the_cloud(
            min_wired_bandwidth=min_wired_bandwidth,
            max_wired_bandwidth=max_wired_bandwidth,
            edge_node_num=edge_node_num,
        )
        return cloud_server(computing_capability, storage_capability, time_slot_num, wired_bandwidths)
    else:
        raise Exception("No such distribution: " + distribution + " for cloud")