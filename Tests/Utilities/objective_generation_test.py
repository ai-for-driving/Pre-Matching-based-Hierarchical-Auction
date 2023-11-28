import sys
import random
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")
from Utilities.object_generation import generate_task_set


def generate_task_set_test():
    tasks = generate_task_set(
        task_num = 10,
        distribution = "uniform",
        min_input_data_size = 1,
        max_input_data_size = 100,
        min_cqu_cycles = 1,
        max_cqu_cycles = 100,
        min_deadline = 1,
        max_deadline = 100,
    )
    for t in tasks:
        print(t)
        print("\n")


if __name__ == '__main__':
    # min_map_x = -10
    # max_map_x = 10.5
    # min_map_y = 0
    # max_map_y = 500
    # edge_num = 9
    # random_xs = [random.uniform(min_map_x, max_map_x) for _ in range(edge_num)]
    # random_ys = [random.uniform(min_map_y, max_map_y) for _ in range(edge_num)]
    
    # print(random_xs)
    # print(random_ys)
    
    min_task_arrival_rate = 0.05
    max_task_arrival_rate = 1
    print(random.uniform(min_task_arrival_rate, max_task_arrival_rate))

