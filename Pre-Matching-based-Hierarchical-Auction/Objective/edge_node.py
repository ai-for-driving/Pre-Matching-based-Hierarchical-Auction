from typing import Any, List
import numpy as np
import random
import math
from Objective.mobility import mobility
from Objective.vehicle import vehicle

class edge_node(object):
    def __init__(
        self,
        mobility: mobility,
        computing_capability: float,
        storage_capability: float,
        communication_range: float,
    ) -> None:
        self_mobility: mobility = mobility
        self_computing_capability: float = computing_capability
        self_storage_capability : float = storage_capability
        self_communication_range : float = communication_range

    
    def __getattribute__(self, __name: str) -> Any:
        pass
    
    def get_availiable_computing_capability(self) -> float:
        return self.computing_capability
    
    # added by near, the edge node should have storage capability
    def get_availiable_storage_capability(self) -> float:
        return self.storage_capability
    
    def set_consumed_computing_capability(self, consumed_computing_capability: float, duration: int) -> None:
        pass
    
    def set_consumed_storage_capability(self, consumed_storage_capability: float, duration: int) -> None:
        pass
    
    def calculate_distance(self, x1, x2, y1, y2, current_time) -> float:
        pass
        


def generate_edge_nodes(
    mobilities: List[mobility],
    min_computing_capability: float,
    max_computing_capability: float,
    min_storage_capability: float,
    max_storage_capability: float,
    communication_range : float,
    distribution: str,
) -> List(edge_node):
    edge_nodes = []
    for mobility in mobilities:
        if distribution == "uniform" :
            computing_capability = random.uniform(min_computing_capability,max_computing_capability)
            storage_capability = random.uniform(min_storage_capability,max_storage_capability)
        else:
            pass
        edge_node_obj = edge_node(mobility,computing_capability,storage_capability,communication_range)
        edge_nodes.append(edge_node_obj)

def get_vehicles_under_coverage_of_edge_nodes(
    vehicles: List[vehicle],
    edge_nodes: List[edge_node],
    now: int,
    V2I_distance: float,
) -> np.ndarray:
    num_vehicles = len(vehicles)
    num_edge_nodes = len(edge_nodes)
    result = np.zeros((num_vehicles, num_edge_nodes))
    for i in range(num_vehicles):
        for j in range(num_edge_nodes):
            vehicle = vehicles[i]
            edge_node = edge_nodes[j]
            distance = calculate_distance(edge_node.mobility.location_x, 
                                          vehicle.mobility.location_x, 
                                          edge_node.mobility.location_y,
                                          vehicle.mobility.location_y,
                                          now)
            if(distance <= V2I_distance):
                result[i,j] = 1

    return result

def generate_edge_nodes_test():
    pass

def get_vehicles_under_coverage_of_edge_nodes_test():
    pass

if __name__ == '__main__':
    generate_edge_nodes_test()
    get_vehicles_under_coverage_of_edge_nodes_test()
    