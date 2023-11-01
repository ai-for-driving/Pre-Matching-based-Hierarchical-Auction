import random
from typing import List
from Objectives.task import task
from Objectives.mobility import mobility
from Objectives.vehicle import vehicle
from Objectives.edge_node import edge_node
from Objectives.cloud_server import cloud_server
from Utilities.vehicular_trajectories_processing import TrajectoriesProcessing
from Utilities.wired_bandwidth import get_wired_bandwidth_between_edge_nodes_and_the_cloud

def generate_task_set(
    task_num: int,
    distribution: str,
    min_input_data_size: float,
    max_input_data_size: float,
    min_cqu_cycles: float,
    max_cqu_cycles: float,
    min_deadline: float,
    max_deadline: float,
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
    min_computing_capability: float,
    max_computing_capability: float,
    min_storage_capability: float,
    max_storage_capability: float,
    min_transmission_power: float,
    max_transmission_power: float,
    communication_range: float,
    min_task_arrival_rate: float,
    max_task_arrival_rate: float,
    task_num: int,
    distribution: str,
) -> List[vehicle]:

    trajectoriesProcessing = TrajectoriesProcessing(
        file_name_key=file_name_key,
        vehicle_number=vehicle_num,
        start_time=start_time,
        slot_length=slot_length,
        slection_way=slection_way,
        filling_way=filling_way,
        chunk_size=chunk_size,
    )
    trajectoriesProcessing.processing()
    
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
        return vehicles
    else:
        raise Exception("distribution not supported")
    
    
def generate_edge_nodes(
    edge_num: int,
    file_name: str,
    min_computing_capability: float,
    max_computing_capability: float,
    min_storage_capability: float,
    max_storage_capability: float,
    communication_range : float,
    time_slot_num: int,
    distribution: str,
) -> List[edge_node]:
    edge_nodes = []
    edge_node_x = []
    edge_node_y = []
    try:
        with open(file_name, 'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                line = line.split(',')
                edge_node_x.append(float(line[0]))
                edge_node_y.append(float(line[1]))
    except:
        raise Exception("No such file: " + file_name)
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
                mobility = mobility_obj, 
                computing_capability = computing_capability, 
                storage_capability = storage_capability,
                communication_range = communication_range,
                time_slot_num = time_slot_num)
            edge_nodes.append(edge_node_obj)
        return edge_nodes 
    else:
        raise Exception("distribution is not supported")
        
        
def generate_cloud(
    computing_capability: float,
    storage_capability: float,
    edge_node_num: int,
    time_slot_num: int,
    min_wired_bandwidth: float,
    max_wired_bandwidth: float,
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