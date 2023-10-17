import sys
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")

from Objectives.cloud_server import cloud_server


# class cloud_server(object):
#     def __init__(
#         self,
#         computing_capability: float,
#         storage_capability: float,
#         time_slot_num: int,
#         wired_bandwidths: List[float],
#         ) -> None:
#         self._computing_capability : float = computing_capability
#         self._storage_capability : float = storage_capability
#         self._available_computing_capability : List[float] = [computing_capability for _ in range(time_slot_num)]
#         self._available_storage_capability : List[float] = [storage_capability for _ in range(time_slot_num)]   
#         self._wired_bandwidth : List[float] = wired_bandwidths
        
#     def get_computing_capability(self) -> float:
#         return self._computing_capability
    
#     def get_storage_capability(self) -> float:
#         return self._storage_capability
    
#     def get_available_computing_capability(self, now: int) -> float:
#         return self._available_computing_capability[now]
    
#     def get_available_storage_capability(self, now: int) -> float:
#         return self._available_storage_capability[now]
    
#     def get_wired_bandwidth_between_edge_node_and_cloud(self, edge_node_index: int) -> float:
#         return self._wired_bandwidth[edge_node_index]
    
#     def set_consumed_computing_capability(self, consumed_computing_capability: float, now: int, duration: int) -> None:
#         for i in range(now, now + duration):
#             self._available_computing_capability[i] = self._available_computing_capability[i] - consumed_computing_capability
#         return None
    
#     def set_consumed_storage_capability(self, consumed_storage_capability: float, now: int, duration: int) -> None:
#         for i in range(now, now + duration):
#             self._available_storage_capability[i] = self._available_storage_capability[i] - consumed_storage_capability
#         return None
    


def test_cloud_server():
    c = cloud_server(
        computing_capability=1.0,
        storage_capability=2.0,
        time_slot_num=10,
        wired_bandwidths=[1.0, 2.0, 3.0],
    )
    assert isinstance(c, cloud_server)
    assert isinstance(c.get_computing_capability(), float)
    assert isinstance(c.get_storage_capability(), float)
    assert isinstance(c.get_available_computing_capability(0), float)
    assert isinstance(c.get_available_storage_capability(0), float)
    assert isinstance(c.get_wired_bandwidth_between_edge_node_and_cloud(0), float)
    

def test_set_consumed_computing_capability():
    start_time = 0
    duration = 5
    c = cloud_server(
        computing_capability=1.0,
        storage_capability=2.0,
        time_slot_num=10,
        wired_bandwidths=[1.0, 2.0, 3.0],
    )
    assert c.get_available_computing_capability(0) == 1.0
    c.set_consumed_computing_capability(0.5, start_time, duration)
    assert c.get_available_computing_capability(0) == 0.5
    assert c.get_available_computing_capability(1) == 0.5
    assert c.get_available_computing_capability(2) == 0.5
    assert c.get_available_computing_capability(3) == 0.5
    assert c.get_available_computing_capability(4) == 0.5
    assert c.get_available_computing_capability(5) == 1.0
    assert c.get_available_computing_capability(6) == 1.0
    
    
def test_set_consumed_storage_capability():
    start_time = 0
    duration = 5
    c = cloud_server(
        computing_capability=1.0,
        storage_capability=2.0,
        time_slot_num=10,
        wired_bandwidths=[1.0, 2.0, 3.0],
    )
    assert c.get_available_storage_capability(0) == 2.0
    c.set_consumed_storage_capability(0.5, start_time, duration)
    assert c.get_available_storage_capability(0) == 1.5
    assert c.get_available_storage_capability(1) == 1.5
    assert c.get_available_storage_capability(2) == 1.5
    assert c.get_available_storage_capability(3) == 1.5
    assert c.get_available_storage_capability(4) == 1.5
    assert c.get_available_storage_capability(5) == 2.0
    assert c.get_available_storage_capability(6) == 2.0