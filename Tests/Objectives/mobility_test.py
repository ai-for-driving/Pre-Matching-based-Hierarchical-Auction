import sys
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")
from Objects.mobility_object import mobility

def test_mobility():
    m = mobility(
        x = 1.0,
        y = 2.0,
        speed = 3.0,
        acceleration = 4.0,
        direction = 5.0,
        time = 6.0,
    )
    assert isinstance(m, mobility)
    assert isinstance(m.get_x(), float)
    assert isinstance(m.get_y(), float)
    assert isinstance(m.get_speed(), float)
    assert isinstance(m.get_acceleration(), float)
    assert isinstance(m.get_direction(), float)
    assert isinstance(m.get_time(), float)
    assert m.get_x() == 1.0
    assert m.get_y() == 2.0
    assert m.get_speed() == 3.0
    assert m.get_acceleration() == 4.0
    assert m.get_direction() == 5.0
    assert m.get_time() == 6.0


    
    

    