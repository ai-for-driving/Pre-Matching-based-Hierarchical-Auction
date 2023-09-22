class env(object):
    
    def __init__(
        self,
        slot_length: int) -> None:
        self._now : int = 0
        self._slot_length : int = slot_length
    
        