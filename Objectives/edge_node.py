from typing import List
import numpy as np
import random
from Objectives.mobility import mobility, calculate_distance 
from Objectives.vehicle import vehicle

class edge_node(object):
    def __init__(
        self,
        mobility: mobility,       
        computing_capability: float,
        storage_capability: float,
        communication_range: float,
        time_slot_num: int,
    ) -> None:
        self._mobility: mobility = mobility 
        self._computing_capability: float = computing_capability
        self._availiable_computing_capability: List[float] = [self._computing_capability for _ in range(time_slot_num)] 
        self._storage_capability : float = storage_capability
        self._availiable_storage_capability: List[float] = [self._storage_capability for _ in range(time_slot_num)]
        self._communication_range : float = communication_range

    def get_mobility(self) -> mobility:
        return self._mobility
    
    def get_computing_capability(self) -> float:
        return self._computing_capability
    
    def get_storage_capability(self) -> float:
        return self._storage_capability
    
    def get_communication_range(self) -> float:
        return self._communication_range
    
    def get_availiable_computing_capability(self, now: int) -> float:
        return self._availiable_computing_capability[now]
    
    def get_availiable_storage_capability(self, now: int) -> float:
        return self._availiable_storage_capability[now]

    def set_consumed_computing_capability(self, consumed_computing_capability: float, now: int, duration: int) -> None:
        for i in range(now, now + duration):
            self._availiable_computing_capability[i] = self._availiable_computing_capability[i] - consumed_computing_capability
        return None    

    def set_consumed_storage_capability(self, consumed_storage_capability: float, now: int, duration: int) -> None:
        for i in range(now, now + duration):
            self._availiable_storage_capability[i] = self._availiable_storage_capability[i] - consumed_storage_capability
        return None
        
def generate_edge_nodes(
    edge_num: int,
    file_name: str,
    min_computing_capability: float,
    max_computing_capability: float,
    min_storage_capability: float,
    max_storage_capability: float,
    communication_range : float,
    distribution: str,
) -> List(edge_node):
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
            mobility_obj = mobility(edge_node_x[_], edge_node_y[_], 0, 0)
            computing_capability = random.uniform(min_computing_capability,max_computing_capability)
            storage_capability = random.uniform(min_storage_capability,max_storage_capability)
            edge_node_obj = edge_node(mobility_obj, computing_capability, storage_capability, communication_range)
            edge_nodes.append(edge_node_obj)
        return edge_nodes 
    else:
        raise Exception("distribution is not supported")
        

def get_vehicles_under_coverage_of_edge_nodes(
    vehicles: List[vehicle],
    edge_nodes: List[edge_node],
    now: int,
) -> np.ndarray:
    num_vehicles = len(vehicles)
    num_edge_nodes = len(edge_nodes)
    result = np.zeros((num_vehicles, num_edge_nodes))
    for i in range(num_vehicles):
        for j in range(num_edge_nodes):
            vehicle = vehicles[i]
            edge_node = edge_nodes[j]
            distance = calculate_distance(vehicle.get_mobility(now), edge_node.get_mobility(now))
            if(distance <= edge_node.get_communication_range()):
                result[i,j] = 1
    return result

def generate_edge_nodes_test():
    pass

def get_vehicles_under_coverage_of_edge_nodes_test():
    pass

if __name__ == '__main__':
    generate_edge_nodes_test()
    get_vehicles_under_coverage_of_edge_nodes_test()