import random

class task(object):
    '''
    A task is defined by its input data size, cqu cycles and deadline
    '''
    def __init__(
        self,
        input_data_size: float,
        cqu_cycles: float,
        deadline: float,
        ) -> None:
        self._input_data_size : float = input_data_size
        self._cqu_cycles : float = cqu_cycles
        self._deadline : float = deadline
    
    def get_input_data_size(self) -> float:
        return self._input_data_size
    
    def get_cqu_cycles(self) -> float:
        return self._cqu_cycles
    
    def get_deadline(self) -> float:
        return self._deadline
    
    def __str__(self) -> str:
        return "Input data size: " + str(self._input_data_size) + "\nCqu cycles: " + str(self._cqu_cycles) + "\nDeadline: " + str(self._deadline)
        

def generate_task_set(
    task_num: int,
    distribution: str,
    min_input_data_size: float,
    max_input_data_size: float,
    min_cqu_cycles: float,
    max_cqu_cycles: float,
    min_deadline: float,
    max_deadline: float,
):
    '''
    Generate a task set with given parameters
    Args:
        task_num: number of tasks
        distribution: distribution of the task parameters
        min_input_data_size: minimum input data size
        max_input_data_size: maximum input data size
        min_cqu_cycles: minimum cqu cycles
        max_cqu_cycles: maximum cqu cycles
        min_deadline: minimum deadline
        max_deadline: maximum deadline
    Returns:
        tasks: a list of tasks
    '''
    tasks = list()
    if distribution == "uniform":
        for _ in range(task_num):
            t = task(
                input_data_size = random.uniform(min_input_data_size, max_input_data_size),
                cqu_cycles = random.uniform(min_cqu_cycles, max_cqu_cycles),
                deadline = random.uniform(min_deadline, max_deadline),
            )
            tasks.append(t)
        return tasks
    elif distribution == "normal":
        for _ in range(task_num):
            t = task(
                input_data_size = random.normalvariate((min_input_data_size + max_input_data_size)/2, (max_input_data_size - min_input_data_size)/6),
                cqu_cycles = random.normalvariate((min_cqu_cycles + max_cqu_cycles)/2, (max_cqu_cycles - min_cqu_cycles)/6),
                deadline = random.normalvariate((min_deadline + max_deadline)/2, (max_deadline - min_deadline)/6),
            )
            tasks.append(t)
        return tasks
    else:
        raise ValueError("Distribution not supported")
    
    
def generate_task_set_test():
    tasks = generate_task_set(
        task_num = 10,
        distribution = "normal",
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
        
if __name__ == "__main__":
    generate_task_set_test()