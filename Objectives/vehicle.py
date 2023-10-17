from typing import List, Tuple
import random
import numpy as np
from Objectives.mobility import mobility

class vehicle(object):
    '''
    the vehicle is defined by its mobilities, computing capability, available computing capability and transmission power
    args:
        mobilities: a list of mobility
        computing_capability: computing capability
        available_computing_capability: available computing capability
        transmission_power: transmission power
    '''
    def __init__(
        self,
        mobilities: List[mobility],
        computing_capability: float,
        storage_capability: float,
        time_slot_num: int,
        transmission_power: float,
        communication_range: float,
        task_arrival_rate: float,
        task_num: int,
    ) -> None:
        self._mobilities : List[mobility] = mobilities
        self._computing_capability : float = computing_capability
        self._storage_capability : float = storage_capability
        self._time_slot_num : int = time_slot_num
        self._available_computing_capability : List[float] = [computing_capability for _ in range(time_slot_num)]
        self._available_storage_capability : List[float] = [storage_capability for _ in range(time_slot_num)]
        self._transmission_power : float = transmission_power
        self._communication_range : float = communication_range
        self._task_arrival_rate : float = task_arrival_rate
        self._task_num : int = task_num
        self._tasks : List[Tuple] = self.generate_task()
        
    def get_mobilities(self) -> List[mobility]:
        return self._mobilities
    
    def get_mobility(self, now: int) -> mobility:
        return self._mobilities[now]
    
    def get_computing_capability(self) -> float:
        return self._computing_capability
    
    def get_storage_capability(self) -> float:
        return self._storage_capability
    
    def get_available_computing_capability(self, now: int) -> float:
        return self._available_computing_capability[now]
    
    def get_available_storage_capability(self, now: int) -> float:
        return self._available_storage_capability[now]
    
    def get_transmission_power(self) -> float:
        return self._transmission_power
    
    def get_communication_range(self) -> float:
        return self._communication_range
    
    def get_task_arrival_rate(self) -> float:
        return self._task_arrival_rate
    
    def get_tasks(self) -> List[Tuple]:
        return self._tasks
    
    def get_tasks_by_time(self, now : int) -> List[Tuple]:
        return [task for task in self._tasks if task[0] == now]
    
    def set_consumed_computing_capability(self, consumed_computing_capability: float, now: int, duration: int) -> None:
        for i in range(now, now + duration):
            self._available_computing_capability[i] = self._available_computing_capability[i] - consumed_computing_capability
        return None
    
    def set_consumed_storage_capability(self, consumed_storage_capability: float, now: int, duration: int) -> None:
        for i in range(now, now + duration):
            self._available_storage_capability[i] = self._available_storage_capability[i] - consumed_storage_capability
        return None
    
    def generate_task(self) -> List[Tuple]:
        '''each vehicle generate tasks according to a Poission distribution with arrival rate'''
        tasks : List[Tuple] = []
        task_arrival_times = np.random.poisson(self._task_arrival_rate, self._time_slot_num)
        for i in range(self._time_slot_num):
            if task_arrival_times[i] > 0:
                for _ in range(task_arrival_times[i]):
                    tasks.append((i, random.choices(range(self._task_num), k=1)[0]))
        return tasks
    
    def __str__(self, now) -> str:
        return "location_x: " + self.get_mobilities(now).get_x() \
            + "\nlocation_y: " + self.get_mobilities(now).get_y() \
            + "\nspeed: " + self.get_mobilities(now).get_speed() \
            + "\ndirection: " + self.get_mobilities(now).get_direction() \
            + "\ncomputing_capability: " + self.get_computing_capability() \
            + "\nstorage_capability: " + self.get_storage_capability() \
            + "\navailable_computing_capability: " + self.get_available_computing_capability(now) \
            + "\navailable_storage_capability: " + self.get_available_storage_capability(now) \
            + "\ntransmission_power: " + self.get_transmission_power() \
            + "\ncommunication_range: " + self.get_communication_range() \
            + "\ntask_arrival_rate: " + self.get_task_arrival_rate()
