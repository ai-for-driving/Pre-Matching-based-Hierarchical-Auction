from typing import Any, List
import numpy as np
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
        pass
    
    def __getattribute__(self, __name: str) -> Any:
        pass
    
    def get_availiable_computing_capability(self) -> float:
        pass
    
    # added by near, the edge node should have storage capability
    def get_availiable_storage_capability(self) -> float:
        pass
    
    def set_consumed_computing_capability(self, consumed_computing_capability: float, duration: int) -> None:
        pass
    
    def set_consumed_storage_capability(self, consumed_storage_capability: float, duration: int) -> None:
        pass
    

def generate_edge_nodes(
    mobilities: List[mobility],
    min_computing_capability: float,
    max_computing_capability: float,
    min_storage_capability: float,
    max_storage_capability: float,
    distribution: str,
) -> List(edge_node):
    pass

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
            pass
    return result

def generate_edge_nodes_test():
    pass

def get_vehicles_under_coverage_of_edge_nodes_test():
    pass

if __name__ == '__main__':
    generate_edge_nodes_test()
    get_vehicles_under_coverage_of_edge_nodes_test()
    