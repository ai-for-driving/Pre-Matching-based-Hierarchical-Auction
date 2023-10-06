from typing import Any, List
from Objective.edge_node import edge_node, get_vehicles_under_coverage_of_edge_nodes

class cloud(object):
    '''
    A cloud is defined by its computing capability, transmission speed
    '''
    def __init__(
            self,
            edge_nodes: List[edge_node],  # 边节点列表
            transmission_speed: float,  # 传输速率
            computing_capability: float,  # 计算能力
            available_computing_capability: float  # 可用计算能力
    ) -> None:
        self._edge_nodes: List[edge_node] = edge_nodes
        self._transmission_speed: float = transmission_speed
        self._computing_capability: float = computing_capability
        self._available_computing_capability: float = available_computing_capability
    def get_edge_nodes(self) -> List[edge_node]:
        return self._edge_nodes

    def get_edge_node(self, now: int) -> edge_node:
        '''获取边缘节点'''
        return self.edge_nodes[now]

    def get_transmission_speed(self) -> float:
        '''获取边节点与云服务器的传输速率'''
        return self._transmission_speed

    def get_computing_capability(self) -> float:
        '''获取云的计算能力'''
        return self._computing_capability

    def get_available_computing_capability(self) -> float:
        '''获取云的可用计算能力'''
        return self._available_computing_capability

    def __str__(self, now) -> str:
        return "边缘节点: " + str(self.get_edge_node(now)) \
               + "\n计算能力: " + str(self.get_computing_capability()) \
               + "\n可用计算能力: " + str(self.get_available_computing_capability()) \
               + "\n传输速率: " + str(self.get_transmission_speed())

def time_offloading_cloud():
    pass

def generate_cloud_list(
        edge_nodes: List[edge_node],  # 边缘节点列表
        min_computing_capability: float,  # 最小计算能力
        max_computing_capability: float,  # 最大计算能力
        min_transmission_speed: float,  # 最小传输速率
        max_transmission_speed: float,  # 最大传输速率
        min_available_computing_capability: float,  # 最小可用计算能力
        max_available_computing_capability: float,  # 最大可用计算能力
) -> List[cloud]:
    edge_nodes_list: List[List[edge_node]] = get_vehicles_under_coverage_of_edge_nodes(

    )
    # 定义内部功能函数
    pass

def get_edge_nodes_under_coverage_of_Clouds(
        edge_nodes: List[edge_node],  # 边缘节点列表
        Clouds: List[cloud],  # 云服务器列表
        now: int,  # 当前时间
        I2C_distance: float,  # 边缘节点到云服务器的距离
) -> Any:
    num_EdgeNodes = len(edge_nodes)
    num_Clouds = len(Clouds)

def generate_cloud_test():
    cloud_list_test = generate_cloud_list(
        edge_nodes=[],  # 边缘节点列表
        min_computing_capability=1,  # 最小计算能力
        max_computing_capability=100,  # 最大计算能力
        min_transmission_speed=1,  # 最小传输速率
        max_transmission_speed=100,  # 最大传输速率
        min_available_computing_capability=1,  # 最小可用计算能力
        max_available_computing_capability100=100,  # 最大可用计算能力
    )
    pass

def get_edge_nodes_under_coverage_of_Clouds(
) -> Any:
    pass

if __name__ == "__main__":
    generate_cloud_test()