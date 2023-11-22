import sys
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")
from Objects.mobility import mobility
from Objects.edge_node import edge_node

def test_edge_node():
    m = mobility(
        x = 1.0,
        y = 2.0,
        speed = 3.0,
        acceleration = 4.0,
        direction = 5.0,
        time = 6.0,
    )
    e = edge_node(
        mobility=m,
        computing_capability=1.0,
        storage_capability=2.0,
        communication_range=3.0,
        time_slot_num=10,
    )
    assert isinstance(e, edge_node)
    assert isinstance(e.get_mobility(), mobility)
    assert isinstance(e.get_mobility().get_x(), float)
    assert isinstance(e.get_mobility().get_y(), float)
    assert isinstance(e.get_mobility().get_speed(), float)
    assert isinstance(e.get_mobility().get_acceleration(), float)
    assert isinstance(e.get_mobility().get_direction(), float)
    assert isinstance(e.get_mobility().get_time(), float)
    assert isinstance(e.get_computing_capability(), float)
    assert isinstance(e.get_storage_capability(), float)
    assert isinstance(e.get_communication_range(), float)
    assert isinstance(e.get_available_computing_capability(0), float)
    assert isinstance(e.get_available_storage_capability(0), float)
    
def test_set_consumed_computing_capability():
    start_time = 0
    duration = 5
    m = mobility(
        x = 1.0,
        y = 2.0,
        speed = 3.0,
        acceleration = 4.0,
        direction = 5.0,
        time = 6.0,
    )
    e = edge_node(
        mobility=m,
        computing_capability=1.0,
        storage_capability=2.0,
        communication_range=3.0,
        time_slot_num=10,
    )
    assert e.get_available_computing_capability(0) == 1.0
    e.set_consumed_computing_capability(0.5, start_time, duration)
    assert e.get_available_computing_capability(0) == 0.5
    assert e.get_available_computing_capability(1) == 0.5
    assert e.get_available_computing_capability(2) == 0.5
    assert e.get_available_computing_capability(3) == 0.5
    assert e.get_available_computing_capability(4) == 0.5
    assert e.get_available_computing_capability(5) == 1.0
    assert e.get_available_computing_capability(6) == 1.0
    assert e.get_available_computing_capability(7) == 1.0
    assert e.get_available_computing_capability(8) == 1.0
    assert e.get_available_computing_capability(9) == 1.0


def test_set_consumed_storage_capability():
    start_time = 0
    duration = 5
    m = mobility(
        x = 1.0,
        y = 2.0,
        speed = 3.0,
        acceleration = 4.0,
        direction = 5.0,
        time = 6.0,
    )
    e = edge_node(
        mobility=m,
        computing_capability=1.0,
        storage_capability=2.0,
        communication_range=3.0,
        time_slot_num=10,
    )
    assert e.get_available_storage_capability(0) == 2.0
    e.set_consumed_storage_capability(0.5, start_time, duration)
    assert e.get_available_storage_capability(0) == 1.5
    assert e.get_available_storage_capability(1) == 1.5
    assert e.get_available_storage_capability(2) == 1.5
    assert e.get_available_storage_capability(3) == 1.5
    assert e.get_available_storage_capability(4) == 1.5
    assert e.get_available_storage_capability(5) == 2.0
    assert e.get_available_storage_capability(6) == 2.0
    assert e.get_available_storage_capability(7) == 2.0
    assert e.get_available_storage_capability(8) == 2.0
    assert e.get_available_storage_capability(9) == 2.0