import numpy as np
from strategy import action

def random_action(
    client_vehicle_number : int,
    server_vehicle_number : int,
    edge_node_number : int,
    cloud_node_number : int,
) -> action:
    offloading_decision = np.zeros((client_vehicle_number, server_vehicle_number + edge_node_number + cloud_node_number), dtype = np.int)
    computing_resource_decision = np.zeros((client_vehicle_number, server_vehicle_number + edge_node_number + cloud_node_number), dtype = np.float)
    for _ in range(client_vehicle_number):
        offloading_node = np.random.randint(0, server_vehicle_number + edge_node_number + cloud_node_number)
        offloading_decision[_, offloading_node] = 1
        computing_resource_decision[_, offloading_node] = np.random.uniform(0, 1)
    action_obj = action(client_vehicle_number, server_vehicle_number, edge_node_number, cloud_node_number)
    action_obj.set_offloading_decision(offloading_decision)
    action_obj.set_computing_resource_decision(computing_resource_decision)
    for i in range(2 + server_vehicle_number + edge_node_number):
        if np.sum(action_obj.get_computing_resource_decision()[:][i]) > 1:
            soft_max = np.exp(action_obj.get_computing_resource_decision()[:][i]) / np.sum(np.exp(action_obj.get_computing_resource_decision()[:][i]))
            action_obj.set_computing_resource_decision_of_offloaded_node(i, soft_max)
    if not action_obj.check_validity():
        raise Exception("Invalid action")
    return action_obj