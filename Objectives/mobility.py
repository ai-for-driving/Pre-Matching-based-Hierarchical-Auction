from typing import List
class mobility(object):
    '''the mobility of a vehicle is defined by its position, speed and direction'''
    def __init__(
        self,
        x: float,
        y: float,
        speed: float,
        acceleration: float,
        direction: float,
        time : float,
    ) -> None:
        self._x : float = x
        self._y : float = y
        self._speed : float = speed
        self._acceleration : float = acceleration
        self._direction : float = direction
        self._time = time
        
    def get_x(self) -> float:
        return self._x
    
    def get_y(self) -> float:
        return self._y
    
    def get_speed(self) -> float:
        return self._speed
    
    def get_acceleration(self) -> float:
        return self._acceleration
    
    def get_direction(self) -> float:
        return self._direction
    
    def get_time(self) -> float:
        return self._time

    
def get_vehicle_trajectories(
    vehicle_num: int,
    slot_length: int,
    file_name: str,
) -> List[List[mobility]]:
    pass