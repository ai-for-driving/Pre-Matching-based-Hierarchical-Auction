from typing import List
import math
class mobility(object):
    '''the mobility of a vehicle is defined by its position, speed and direction'''
    def __init__(
        self,
        x: float,
        y: float,
        speed: float,
        direction: float,
    ) -> None:
        self._x : float = x
        self._y : float = y
        self._speed : float = speed
        self._direction : float = direction
        
    def get_x(self) -> float:
        return self._x
    
    def get_y(self) -> float:
        return self._y
    
    def get_speed(self) -> float:
        return self._speed
    
    def get_direction(self) -> float:
        return self._direction
    
def calculate_distance(location_1 : mobility, location_2 : mobility) -> float:
    x1 = location_1.get_x()
    x2 = location_2.get_x()
    y1 = location_1.get_y()
    y2 = location_2.get_y()

    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    
def get_vehicle_trajectories(
    vehicle_num: int,
    slot_length: int,
    file_name: str,
) -> List(List(mobility)):
    pass