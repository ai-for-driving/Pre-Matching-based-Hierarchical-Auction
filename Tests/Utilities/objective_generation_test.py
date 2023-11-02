import sys
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")
from Utilities.objective_generation import generate_task_set


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


