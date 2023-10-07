from typing import List
import random

class cloud_server(object):
    def __init__(
        self,
        computing_capability: float,
        storage_capability: float,
        time_slot_num: int,
        wired_bandwidths: List[float],
        ) -> None:
        self._computing_capability : float = computing_capability
        self._storage_capability : float = storage_capability
        self._avaliable_computing_capability : List[float] = [computing_capability for _ in range(time_slot_num)]
        self._avaliable_storage_capability : List[float] = [storage_capability for _ in range(time_slot_num)]   
        self._wired_bandwidth : List[float] = wired_bandwidths
        
    def get_computing_capability(self) -> float:
        return self._computing_capability
    
    def get_storage_capability(self) -> float:
        return self._storage_capability
    
    def get_availiable_computing_capability(self, now: int) -> float:
        return self._avaliable_computing_capability[now]
    
    def get_availiable_storage_capability(self, now: int) -> float:
        return self._avaliable_storage_capability[now]
    
    def get_wired_bandwidth(self, edge_node_index: int) -> float:
        return self._wired_bandwidth[edge_node_index]
    
    def set_consumed_computing_capability(self, consumed_computing_capability: float, now: int, duration: int) -> None:
        for i in range(now, now + duration):
            self._avaliable_computing_capability[i] = self._avaliable_computing_capability[i] - consumed_computing_capability
        return None
    
    def set_consumed_storage_capability(self, consumed_storage_capability: float, now: int, duration: int) -> None:
        for i in range(now, now + duration):
            self._avaliable_storage_capability[i] = self._avaliable_storage_capability[i] - consumed_storage_capability
        return None
    
def generate_cloud(
    computing_capability: float,
    storage_capability: float,
    time_slot_num: int,
    min_wired_bandwidth: float,
    max_wired_bandwidth: float,
    distribution: str,
) -> cloud_server:
    if distribution == "uniform":
        wired_bandwidths = [random.uniform(min_wired_bandwidth, max_wired_bandwidth) for _ in range(time_slot_num)]
        return cloud_server(computing_capability, storage_capability, time_slot_num, wired_bandwidths)
    else:
        raise Exception("No such distribution: " + distribution + " for cloud")