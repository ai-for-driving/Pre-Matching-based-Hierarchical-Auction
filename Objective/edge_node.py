from typing import Any, List
import numpy as np
import random
import math
# TODO
# define calculate_distance(location_1: mobility, location_2: mobility) in Objective.mobility
from Objective.mobility import mobility, calculate_distance 
from Objective.vehicle import vehicle

class edge_node(object):
    def __init__(
        self,
        mobility: mobility,        # 因为边缘节点是固定的, 所以它只需要一个mobility表示它的位置
        computing_capability: float,
        storage_capability: float,
        communication_range: float,
        time_slot_num: int,
    ) -> None:
        # self_mobility: mobility = mobility    # 这里写的有点问题
        # 这里赋值的语法是
        # self._mobility: mobility = mobiltiy
        # self 表示当前对象实例
        # ._mobility 表示对象属性值的变量名
        # : mobility 第一个表示这个变量的类型
        # = mobiltiy 第二个表示给这个变量赋值的值
        self._mobility: mobility = mobility 
        self._computing_capability: float = computing_capability
        # 可用资源初始化为同样的值
        self._availiable_computing_capability: List(float) = [self._computing_capability for _ in range(time_slot_num)] 
        self._storage_capability : float = storage_capability
        self._availiable_storage_capability: List(float) = [self._storage_capability for _ in range(time_slot_num)]
        self._communication_range : float = communication_range

    # 这个函数我写着这，是希望你把 edge_node.get_xxx() 这些函数都写一下
    # e.g., get_mobility(), get_computing_capability()
    def __getattribute__(self, __name: str) -> Any:
        pass

    # 函数要指定输入输出, 比如这个函数的输入是self, 输出是 mobility 类型的对象
    # 我们调用时直接使用 edge.get_mobility() 
    def get_mobility(self) -> mobility:  
        return self._mobility

    # 由于边缘节点在处理任务时，任务不一定能在单位时间片内处理完成，其有可能会占有多个时间片
    # 因此, 我们还需要再增加一个变量, 记录可用的computing_capability
    def get_availiable_computing_capability(self, now: int) -> float:
        return self._availiable_computing_capability[now]
    
    # added by near, the edge node should have storage capability
    def get_availiable_storage_capability(self, now) -> float:
        return self._availiable_storage_capability[now]

    # 这个函数是用来更新可用的computing_capability的
    # 从 now 开始, 一共 duration 个时间片, 每个时间片消耗的computing_capability是 consumed_computing_capability
    def set_consumed_computing_capability(self, consumed_computing_capability: float, now: int, duration: int) -> None:
        pass
    
    # 和上面的函数类似
    def set_consumed_storage_capability(self, consumed_storage_capability: float, duration: int) -> None:
        pass

    # def calculate_distance(self, x1, x2, y1, y2, current_time) -> float:
    #     pass
    # 这里的 x, y 是通过车辆轨迹点（经纬度坐标）处理后映射到 所选地图范围内 的平面直角坐标系下的 二维坐标
    # 所以, 2个点的距离运算直接用欧式距离就行
        

def generate_edge_nodes(
    mobilities: List[mobility],
    min_computing_capability: float,
    max_computing_capability: float,
    min_storage_capability: float,
    max_storage_capability: float,
    communication_range : float,
    distribution: str,
) -> List(edge_node):
    edge_nodes = []
    if distribution == "uniform" :
        for mobility in mobilities:
            computing_capability = random.uniform(min_computing_capability,max_computing_capability)
            storage_capability = random.uniform(min_storage_capability,max_storage_capability)
            edge_node_obj = edge_node(mobility, computing_capability, storage_capability, communication_range)
            edge_nodes.append(edge_node_obj)
        return edge_nodes # 返回一个列表, 列表中的每个元素是一个 edge_node 对象
    else:
        pass
        

def get_vehicles_under_coverage_of_edge_nodes(
    vehicles: List[vehicle],
    edge_nodes: List[edge_node],
    now: int,
    V2I_distance: float,
) -> np.ndarray:
    num_vehicles = len(vehicles)
    num_edge_nodes = len(edge_nodes)
    result = np.zeros((num_vehicles, num_edge_nodes))
    for i in range(num_vehicles):
        for j in range(num_edge_nodes):
            vehicle = vehicles[i]
            edge_node = edge_nodes[j]
            distance = calculate_distance(edge_node.mobility.location_x, 
                                          vehicle.mobility.location_x, 
                                          edge_node.mobility.location_y,
                                          vehicle.mobility.location_y,
                                          now)
            if(distance <= V2I_distance):
                result[i,j] = 1

    return result

def generate_edge_nodes_test():
    pass

def get_vehicles_under_coverage_of_edge_nodes_test():
    pass

if __name__ == '__main__':
    generate_edge_nodes_test()
    get_vehicles_under_coverage_of_edge_nodes_test()
    