import sys
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")

from Objects.cloud_server import cloud_server


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