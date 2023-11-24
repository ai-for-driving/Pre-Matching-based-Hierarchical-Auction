import numpy as np
import sys
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")
from Strategy.strategy import action

class RA_agent(object):
    
    def __init__(
        self,
    ) -> None:
        pass
        
    def generate_action(
        self,
        client_vehicle_number : int,
        server_vehicle_number : int,
        edge_node_number : int,
        cloud_node_number : int,
    ) -> action:
        offloading_decision = np.zeros((client_vehicle_number, server_vehicle_number + edge_node_number + cloud_node_number + 1), dtype = np.int64)
        computing_resource_decision = np.zeros((client_vehicle_number, server_vehicle_number + edge_node_number + cloud_node_number + 1), dtype = np.float64)
        for _ in range(client_vehicle_number):
            offloading_node = np.random.randint(0, server_vehicle_number + edge_node_number + cloud_node_number + 1)
            offloading_decision[_, offloading_node] = 1
            computing_resource_decision[_, offloading_node] = np.random.uniform(0, 1)
        action_obj = action(client_vehicle_number, server_vehicle_number, edge_node_number, cloud_node_number)
        action_obj.set_offloading_decision(offloading_decision)
        action_obj.set_computing_resource_decision(computing_resource_decision)
        for i in range(server_vehicle_number + edge_node_number + cloud_node_number + 1):
            if i != 0 and np.sum(action_obj.get_computing_resource_decision()[:, i]) > 1:
                # print("i ", i)
                # print("\norigin: ", action_obj.get_computing_resource_decision()[:, i])
                
                soft_max = np.exp(action_obj.get_computing_resource_decision()[:, i]) / np.sum(np.exp(action_obj.get_computing_resource_decision()[:, i]))
                action_obj.set_computing_resource_decision_of_offloaded_node(i, soft_max)
                # print("\nsoftmax: ", soft_max)
                # print("\nction_object: ", action_obj.get_computing_resource_decision()[:, i])
        if not action_obj.check_validity():
            # print("\naction_objct_offloading:", action_obj.get_offloading_decision())
            # print("\naction_object: ", action_obj.get_computing_resource_decision())
            raise Exception("Invalid action")
        return action_obj


