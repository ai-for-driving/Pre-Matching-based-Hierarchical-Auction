from typing import List
from Objective.mobility import mobility, get_vehicle_trajectories

class vehicle(object):
    '''
    the vehicle is defined by its mobilities, computing capability, avaliable computing capability and transmission power
    args:
        mobilities: a list of mobility
        computing_capability: computing capability
        avaliable_computing_capability: avaliable computing capability
        transmission_power: transmission power
    '''
    def __init__(
        self,
        mobilities: List[mobility],
        computing_capability: float,
        avaliable_computing_capability: float,
        transmission_power: float,
        ) -> None:
        self._mobilities : List[mobility] = mobilities
        self._computing_capability : float = computing_capability
        self._avaliable_computing_capability : float = avaliable_computing_capability
        self._transmission_power : float = transmission_power
        
    def get_mobilities(self) -> List[mobility]:
        return self._mobilities
    
    def get_mobility(self, now: int) -> mobility:
        return self._mobilities[now]
    
    def get_computing_capability(self) -> float:
        return self._computing_capability
    
    def get_avaliable_computing_capability(self) -> float:
        return self._avaliable_computing_capability
    
    def get_transmission_power(self) -> float:
        return self._transmission_power
    
    def __str__(self, now) -> str:
        return "location_x: " + self.get_mobilities(now).get_x() \
            + "\nlocation_y: " + self.get_mobilities(now).get_y() \
            + "\nspeed: " + self.get_mobilities(now).get_speed() \
            + "\ndirection: " + self.get_mobilities(now).get_direction() \
            + "\ncomputing_capability: " + self.get_computing_capability() \
            + "\navaliable_computing_capability: " + self.get_avaliable_computing_capability() \
            + "\ntransmission_power: " + self.get_transmission_power()
            

def generate_vehicle_list(
    vehicle_num: int,
    slot_length: int,
    file_name: str,
    min_computing_capability: float,
    max_computing_capability: float,
    min_transmission_power: float,
    max_transmission_power: float,
) -> List(vehicle):
    mobilities_list : List(List(mobility)) = get_vehicle_trajectories(
        vehicle_num = vehicle_num,
        slot_length = slot_length,
        file_name = file_name,
    )
    pass