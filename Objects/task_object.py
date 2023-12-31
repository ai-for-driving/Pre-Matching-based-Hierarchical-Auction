from Utilities.conversion import cover_MB_to_bit, cover_Hz_to_GHz

class task(object):
    '''
    A task is defined by its input data size, cqu cycles and deadline
    '''
    def __init__(
        self,
        input_data_size: float,     # MB
        cqu_cycles: float,          # cycles/bit
        deadline: float,            # seconds
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
    
    def get_requested_computing_resources(self) -> float:
        return self._cqu_cycles * cover_MB_to_bit(self._input_data_size) / self._deadline
    
    def __str__(self) -> str:
        return "Input data size: " + str(self._input_data_size) + "\nCqu cycles: " + str(self._cqu_cycles) + "\nDeadline: " + str(self._deadline) + "\nRequested computing resources: " + str(cover_Hz_to_GHz(self.get_requested_computing_resources())) + "\n"
        
