import sys
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")
from Objects.vehicle_object import vehicle
from Objects.mobility_object import mobility

def test_vehicle():
    mobilities = [
        mobility(
            x = 1.0,
            y = 2.0,
            speed = 3.0,
            acceleration = 4.0,
            direction = 5.0,
            time = 6.0,
        ) for _ in range(10)
    ]
    
    v = vehicle(
        mobilities=mobilities,
        computing_capability=1.0,
        storage_capability=2.0,
        transmission_power=3.0,
        communication_range=4.0,
        task_arrival_rate=5.0,
        task_num=6,
        time_slot_num=10,
    )
    assert isinstance(v, vehicle)
    assert isinstance(v.get_mobilities(), list)
    assert isinstance(v.get_mobilities()[0], mobility)
    assert isinstance(v.get_mobilities()[0].get_x(), float)
    assert isinstance(v.get_mobilities()[0].get_y(), float)
    assert isinstance(v.get_mobilities()[0].get_speed(), float)
    assert isinstance(v.get_mobilities()[0].get_acceleration(), float)
    assert isinstance(v.get_mobilities()[0].get_direction(), float)
    assert isinstance(v.get_mobilities()[0].get_time(), float)
    assert isinstance(v.get_computing_capability(), float)
    assert isinstance(v.get_storage_capability(), float)
    assert isinstance(v.get_available_computing_capability(0), float)
    assert isinstance(v.get_available_storage_capability(0), float)
    
    
def test_generate_task():
    mobilities = [
        mobility(
            x = 1.0,
            y = 2.0,
            speed = 3.0,
            acceleration = 4.0,
            direction = 5.0,
            time = 6.0,
        ) for _ in range(10)
    ]
    
    v = vehicle(
        mobilities=mobilities,
        computing_capability=1.0,
        storage_capability=2.0,
        transmission_power=3.0,
        communication_range=4.0,
        task_arrival_rate=5.0,
        task_num=6,
        time_slot_num=10,
    )
    assert isinstance(v.generate_task(), list)
    assert isinstance(v.generate_task()[0], tuple)
    assert isinstance(v.generate_task()[0][0], int)
    assert isinstance(v.generate_task()[0][1], int)
    assert v.generate_task()[0][0] >= 0
    assert v.generate_task()[0][0] <= 9
    assert v.generate_task()[0][1] >= 0
    assert v.generate_task()[0][1] <= 5
    
def test_set_consumed_computing_capability():
    mobilities = [
        mobility(
            x = 1.0,
            y = 2.0,
            speed = 3.0,
            acceleration = 4.0,
            direction = 5.0,
            time = 6.0,
        ) for _ in range(10)
    ]
    
    v = vehicle(
        mobilities=mobilities,
        computing_capability=1.0,
        storage_capability=2.0,
        transmission_power=3.0,
        communication_range=4.0,
        task_arrival_rate=5.0,
        task_num=6,
        time_slot_num=10,
    )
    v.set_consumed_computing_capability(0.5, 0, 2)
    assert v.get_available_computing_capability(0) == 0.5
    assert v.get_available_computing_capability(1) == 0.5
    assert v.get_available_computing_capability(2) == 1.0
    assert v.get_available_computing_capability(3) == 1.0
    assert v.get_available_computing_capability(4) == 1.0
    assert v.get_available_computing_capability(5) == 1.0
    assert v.get_available_computing_capability(6) == 1.0
    assert v.get_available_computing_capability(7) == 1.0
    assert v.get_available_computing_capability(8) == 1.0
    assert v.get_available_computing_capability(9) == 1.0
    
def test_set_consumed_storage_capability():
    mobilities = [
        mobility(
            x = 1.0,
            y = 2.0,
            speed = 3.0,
            acceleration = 4.0,
            direction = 5.0,
            time = 6.0,
        ) for _ in range(10)
    ]
    
    v = vehicle(
        mobilities=mobilities,
        computing_capability=1.0,
        storage_capability=2.0,
        transmission_power=3.0,
        communication_range=4.0,
        task_arrival_rate=5.0,
        task_num=6,
        time_slot_num=10,
    )
    v.set_consumed_storage_capability(0.5, 0, 2)
    assert v.get_available_storage_capability(0) == 1.5
    assert v.get_available_storage_capability(1) == 1.5
    assert v.get_available_storage_capability(2) == 2.0
    assert v.get_available_storage_capability(3) == 2.0
    assert v.get_available_storage_capability(4) == 2.0
    assert v.get_available_storage_capability(5) == 2.0
    assert v.get_available_storage_capability(6) == 2.0
    assert v.get_available_storage_capability(7) == 2.0
    assert v.get_available_storage_capability(8) == 2.0
    assert v.get_available_storage_capability(9) == 2.0