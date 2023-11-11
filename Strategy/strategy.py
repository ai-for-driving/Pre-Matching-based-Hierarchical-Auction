from typing import List
import numpy as np

class action(object):
    def __init__(
        self, 
        client_vehicle_number : int,
        server_vehicle_number : int,
        edge_node_number : int,
        cloud_node_number : int
    ) -> None:
        self._client_vehicle_number = client_vehicle_number
        self._server_vehicle_number = server_vehicle_number
        self._edge_node_number = edge_node_number
        self._cloud_node_number = cloud_node_number
        self._offloading_decision = np.zeros(
            (client_vehicle_number, 1 + server_vehicle_number + edge_node_number + cloud_node_number),
            dtype = np.int64       # 0: not offloading, 1: offloading 
        )
        self._computing_resource_decision = np.zeros(
            (client_vehicle_number, 1 + server_vehicle_number + edge_node_number + cloud_node_number),
            dtype = np.float64      # 0 ~ 1: computing resource decision
        )
        
    def get_offloading_decision(self) -> np.ndarray:
        return self._offloading_decision
    
    def get_computing_resource_decision(self) -> np.ndarray:
        return self._computing_resource_decision
    
    def set_offloading_decision(self, offloading_decision: np.ndarray) -> None:
        # print("offloading_dicision: ", offloading_decision)
        # print("\n offloading_dicision shape: ", offloading_decision.shape)
        # print("\n self._offloading_decision: ", self._offloading_decision)
        # print("\n self._offloading_decision shape: ", self._offloading_decision.shape)
        if offloading_decision.shape[0] != self._offloading_decision.shape[0] or offloading_decision.shape[1] != self._offloading_decision.shape[1]:
            raise Exception("Invalid offloading decision")
        self._offloading_decision = offloading_decision
        return None
    
    def set_computing_resource_decision(self, computing_resource_decision: np.ndarray) -> None:
        if computing_resource_decision.shape[0] != self._computing_resource_decision.shape[0] or computing_resource_decision.shape[1] != self._computing_resource_decision.shape[1]:
            raise Exception("Invalid computing resource decision")
        self._computing_resource_decision = computing_resource_decision
        return None
    
    def get_offloading_decision_of_client_vehicle(self, client_vehicle_index: int) -> int:
        self.check_client_vehicle_index(client_vehicle_index)
        for i in range(self._offloading_decision.shape[1]):
            if self._offloading_decision[client_vehicle_index][i] != 0:
                return i
        raise Exception("No offloading decision of vehicle " + str(client_vehicle_index))
    
    def get_computing_resource_decision_of_client_vehicle(self, client_vehicle_index: int) -> float:
        self.check_client_vehicle_index(client_vehicle_index)
        for i in range(self._computing_resource_decision.shape[1]):
            if self._computing_resource_decision[client_vehicle_index][i] != 0:
                return self._computing_resource_decision[client_vehicle_index][i]
        raise Exception("No computing resource decision of vehicle " + str(client_vehicle_index))
    
    def get_offloading_decison_at_local(self) -> np.ndarray:
        return self._offloading_decision[:, 0]
    
    def get_computing_resource_decision_at_local(self) -> np.ndarray:
        return self._computing_resource_decision[:, 0]
    
    def get_offloading_decision_at_server_vehicle(self, server_vehicle_index: int) -> List[int]:
        new_server_vehicle_index = self.get_new_server_vehicle_index(server_vehicle_index)
        client_vehicle_index_list = []
        for i in range(self._client_vehicle_number):
            if self._offloading_decision[i][new_server_vehicle_index] != 0:
                client_vehicle_index_list.append(i)
        return client_vehicle_index_list
    
    def get_computing_resource_decision_at_server_vehicle(self, server_vehicle_index: int) -> np.ndarray:
        new_server_vehicle_index = self.get_new_server_vehicle_index(server_vehicle_index)
        return self._computing_resource_decision[:, new_server_vehicle_index]
    
    def get_offloading_decision_at_edge_node(self, edge_node_index: int) -> List[int]:
        new_edge_node_index = self.get_new_edge_node_index(edge_node_index)
        client_vehicle_index_list = []
        for i in range(self._client_vehicle_number):
            if self._offloading_decision[i][new_edge_node_index] != 0:
                client_vehicle_index_list.append(i)
        return client_vehicle_index_list
    
    def get_computing_resource_decision_at_edge_node(self, edge_node_index: int) -> np.ndarray:
        new_edge_node_index = self.get_new_edge_node_index(edge_node_index)
        return self._computing_resource_decision[:, new_edge_node_index]
    
    def get_offloading_decision_at_cloud_node(self) -> List[int]:
        client_vehicle_index_list = []
        for i in range(self._client_vehicle_number):
            if self._offloading_decision[i][-1] != 0:
                client_vehicle_index_list.append(i)
        return client_vehicle_index_list
    
    def get_computing_resource_decision_at_cloud_node(self) -> np.ndarray:
        return self._computing_resource_decision[:, -1]
    
    def get_offloading_decision_of_client_vehicle_to_server_vehicle(self, client_vehicle_index: int, server_vehicle_index: int) -> int:
        self.check_client_vehicle_index(client_vehicle_index)
        new_server_vehicle_index = self.get_new_server_vehicle_index(server_vehicle_index)
        return self._offloading_decision[client_vehicle_index][new_server_vehicle_index]

    def get_computing_resource_decision_of_client_vehicle_to_server_vehicle(self, client_vehicle_index: int, server_vehicle_index: int) -> float:
        self.check_client_vehicle_index(client_vehicle_index)
        new_server_vehicle_index = self.get_new_server_vehicle_index(server_vehicle_index)
        return self._computing_resource_decision[client_vehicle_index][new_server_vehicle_index]
    
    def get_offloading_decision_of_vehicle_to_edge_node(self, client_vehicle_index: int, edge_node_index: int) -> int:
        self.check_client_vehicle_index(client_vehicle_index)
        new_edge_node_index = self.get_new_edge_node_index(edge_node_index)
        return self._offloading_decision[client_vehicle_index][new_edge_node_index]
    
    def get_computing_resource_decision_of_vehicle_to_edge_node(self, client_vehicle_index: int, edge_node_index: int) -> float:
        self.check_client_vehicle_index(client_vehicle_index)
        new_edge_node_index = self.get_new_edge_node_index(edge_node_index)
        return self._computing_resource_decision[client_vehicle_index][new_edge_node_index]
    
    def get_offloading_decision_of_vehicle_to_cloud_node(self, client_vehicle_index: int) -> int:
        self.check_client_vehicle_index(client_vehicle_index)
        return self._offloading_decision[client_vehicle_index][-1]
    
    def get_computing_resource_decision_of_vehicle_to_cloud_node(self, client_vehicle_index: int) -> float:
        self.check_client_vehicle_index(client_vehicle_index)
        return self._computing_resource_decision[client_vehicle_index][-1]
    
    def set_offloading_decision_of_vehicle(self, client_vehicle_index: int, offloading_decision: np.ndarray) -> None:
        self.check_client_vehicle_index(client_vehicle_index)
        if offloading_decision.shape[0] != self._offloading_decision.shape[1]:
            raise Exception("Invalid offloading decision")
        self._offloading_decision[client_vehicle_index] = offloading_decision
        return None
    
    def set_computing_resource_decision_of_vehicle(self, client_vehicle_index: int, computing_resource_decision: np.ndarray) -> None:
        self.check_client_vehicle_index(client_vehicle_index)
        if computing_resource_decision.shape[0] != self._computing_resource_decision.shape[1]:
            raise Exception("Invalid computing resource decision")
        self._computing_resource_decision[client_vehicle_index] = computing_resource_decision
        return None
    
    def set_offloading_decision_of_offloaded_node(self, offloading_node_index: int, offloading_decision: np.ndarray) -> None:
        if offloading_node_index > (self._edge_node_number + self._server_vehicle_number + 1)  or offloading_node_index < 1:
            raise Exception("Invalid offloading node index")
        if offloading_decision.shape[0] != self._offloading_decision.shape[0]:
            raise Exception("Invalid offloading decision")
        self._offloading_decision[:, offloading_node_index] = offloading_decision
        return None
    
    def set_computing_resource_decision_of_offloaded_node(self, offloading_node_index: int, computing_resource_decision: np.ndarray) -> None:
        if offloading_node_index > (self._edge_node_number + self._server_vehicle_number + 1)  or offloading_node_index < 1:
            raise Exception("Invalid offloading node index")
        if computing_resource_decision.shape[0] != self._computing_resource_decision.shape[0]:
            raise Exception("Invalid computing resource decision")
        self._computing_resource_decision[:, offloading_node_index] = computing_resource_decision
        return None
    
    def set_offloading_decision_at_local(self, client_vehicle_index, offloading_decision: int) -> None:
        self.check_client_vehicle_index(client_vehicle_index)
        if offloading_decision > 1 or offloading_decision < 0:
            raise Exception("Invalid offloading decision")
        self._offloading_decision[client_vehicle_index][0] = offloading_decision
        return None
    
    def set_computing_resource_decision_at_local(self, client_vehicle_index: int, computing_resource_decision: float) -> None:
        self.check_client_vehicle_index(client_vehicle_index)
        self._computing_resource_decision[client_vehicle_index][0] = computing_resource_decision
        return None
    
    def set_offloading_decision_of_vehicle_to_vehicle(self, client_vehicle_index: int, server_vehicle_index: int, offloading_decision: int) -> None:
        self.check_client_vehicle_index(client_vehicle_index)
        new_server_vehicle_index = self.get_new_server_vehicle_index(server_vehicle_index)
        if offloading_decision > 1 or offloading_decision < 0:
            raise Exception("Invalid offloading decision")
        self._offloading_decision[client_vehicle_index][new_server_vehicle_index] = offloading_decision
        return None
    
    def set_computing_resource_decision_of_vehicle_to_vehicle(self, client_vehicle_index: int, server_vehicle_index: int, computing_resource_decision: float) -> None:
        self.check_client_vehicle_index(client_vehicle_index)
        new_server_vehicle_index = self.get_new_server_vehicle_index(server_vehicle_index)
        self._computing_resource_decision[client_vehicle_index][new_server_vehicle_index] = computing_resource_decision
        return None
    
    def set_offloading_decision_of_vehicle_to_edge_node(self, client_vehicle_index: int, edge_node_index: int, offloading_decision: int) -> None:
        self.check_client_vehicle_index(client_vehicle_index)
        new_edge_node_index = self.get_new_edge_node_index(edge_node_index)
        if offloading_decision > 1 or offloading_decision < 0:
            raise Exception("Invalid offloading decision")
        self._offloading_decision[client_vehicle_index][new_edge_node_index] = offloading_decision
        return None
    
    def set_computing_resource_decision_of_vehicle_to_edge_node(self, client_vehicle_index: int, edge_node_index: int, computing_resource_decision: float) -> None:
        self.check_client_vehicle_index(client_vehicle_index)
        new_edge_node_index = self.get_new_edge_node_index(edge_node_index)
        self._computing_resource_decision[client_vehicle_index][new_edge_node_index] = computing_resource_decision
        return None
    
    def set_offloading_decision_of_vehicle_to_cloud_node(self, client_vehicle_index: int, offloading_decision: int) -> None:
        self.check_client_vehicle_index(client_vehicle_index)
        if offloading_decision > 1 or offloading_decision < 0:
            raise Exception("Invalid offloading decision")
        self._offloading_decision[client_vehicle_index][-1] = offloading_decision
        return None
    
    def set_computing_resource_decision_of_vehicle_to_cloud_node(self, client_vehicle_index: int, computing_resource_decision: float) -> None:
        self.check_client_vehicle_index(client_vehicle_index)
        self._computing_resource_decision[client_vehicle_index][-1] = computing_resource_decision
        return None
    
    def __str__(self) -> str:
        return "offloading_decision: " + str(self._offloading_decision) + "\n" + "computing_resource_decision: " + str(self._computing_resource_decision) + "\n"
    
    def check_client_vehicle_index(self, client_vehicle_index: int) -> None:
        if client_vehicle_index > self._client_vehicle_number or client_vehicle_index < 0:
            raise Exception("Invalid client vehicle index")
    
    def get_new_server_vehicle_index(self, server_vehicle_index: int) -> int:
        if server_vehicle_index > self._server_vehicle_number or server_vehicle_index < 0:
            raise Exception("Invalid server vehicle index, server_vehicle_index: " + str(server_vehicle_index) + ", self._server_vehicle_number: " + str(self._server_vehicle_number))
        return server_vehicle_index + 1
    
    def get_new_edge_node_index(self, edge_node_index: int) -> int:
        if edge_node_index > self._edge_node_number or edge_node_index < 0:
            raise Exception("Invalid edge node index")
        return edge_node_index + self._server_vehicle_number + 1
    
    def check_validity(self) -> bool:
        for i in range(self._client_vehicle_number):
            if np.abs(np.sum(self._offloading_decision[i]) - 1) > 1e-5:
                print("np.sum(self._offloading_decision[i]) != 1:\n")
                print("i: ", i)
                print("self._offloading_decision[i]: ", self._offloading_decision[i])
                print("sum: ", np.sum(self._offloading_decision[i]))
                print("self._offloading_decision: ", self._offloading_decision)
                return False
        for i in range(2 + self._server_vehicle_number + self._edge_node_number):
            if i == 0:  # local
                for j in range(self._client_vehicle_number):
                    if self._computing_resource_decision[j][i] > 1 + 1e-5:
                        print("self._computing_resource_decision[j][i] > 1: \n")
                        print("j: ", j)
                        print("i: ", i)
                        print("self._computing_resource_decision[j][i]: ", self._computing_resource_decision[j][i])
                        print("self._computing_resource_decision: ", self._computing_resource_decision)
                        return False
            else:    # server vehicles, edge nodes, and the cloud
                if np.sum(self._computing_resource_decision[:, i]) > 1 + 1e-5:
                    print("np.sum(self._computing_resource_decision[:, i]) > 1: \n")
                    print("i: ", i)
                    print("self._computing_resource_decision[:, i]: ", self._computing_resource_decision[:, i])
                    print("sum: ", np.sum(self._computing_resource_decision[:, i]))
                    print("self._computing_resource_decision: ", self._computing_resource_decision)
                    return False
        return True


