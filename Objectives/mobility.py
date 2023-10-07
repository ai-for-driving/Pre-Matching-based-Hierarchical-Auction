from typing import List
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
    
def calculate_distance(mobility1: mobility, mobility2: mobility) -> float:
    return ((mobility1.get_x() - mobility2.get_x()) ** 2 + (mobility1.get_y() - mobility2.get_y()) ** 2) ** 0.5
    
    
def get_vehicle_trajectories(
    vehicle_num: int,
    slot_length: int,
    file_name: str,
) -> List[List[mobility]]:
    pass