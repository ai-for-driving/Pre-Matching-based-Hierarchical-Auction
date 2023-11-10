class buyer(object):
    
    def __init__(
        self,
        buyer_type: str,     #  e.g., "vehicle", "edge node"
        index: int,    #  the index of vehicle or edge node
        vehicle_indexs: list,    #  the indexs of vehicles
        time_slot_index: int,
        requested_computing_resources: float,
        requested_storage_resources: float,
        bid: float,
        payment: float,
    ) -> None:
        self._type = buyer_type
        self._index = index
        self._vehicle_indexs = vehicle_indexs
        self._time_slot_index = time_slot_index
        self._requested_computing_resources = requested_computing_resources
        self._requested_storage_resources = requested_storage_resources
        self._bid = bid
        self._payment = payment
    
    def get_type(self) -> str:
        return self._type
    
    def get_index(self) -> int:
        return self._index
    
    def get_time_slot_index(self) -> int:
        return self._time_slot_index
    
    def get_requested_computing_resources(self) -> float:
        return self._requested_computing_resources
    
    def get_requested_storage_resources(self) -> float:
        return self._requested_storage_resources
    
    def get_bid(self) -> float:
        return self._bid
    
    def get_payment(self) -> float:
        return self._payment
    
    def get_vehicle_indexs(self) -> list:
        return self._vehicle_indexs
    
    def set_type(self, buyer_type: str) -> None:
        self._type = buyer_type
        
    def set_index(self, index: int) -> None:
        self._index = index
        
    def set_time_slot_index(self, time_slot_index: int) -> None:
        self._time_slot_index = time_slot_index
        
    def set_requested_computing_resources(self, requested_computing_resources: float) -> None:
        self._requested_computing_resources = requested_computing_resources
        
    def set_requested_storage_resources(self, requested_storage_resources: float) -> None:
        self._requested_storage_resources = requested_storage_resources
    
    def set_bid(self, bid: float) -> None:
        self._bid = bid
        
    def set_payment(self, payment: float) -> None:
        self._payment = payment
        
    def set_vehicle_indexs(self, vehicle_indexs: list) -> None:
        self._vehicle_indexs = vehicle_indexs
        
    def __str__(self) -> str:
        return "Buyer type: {}, index: {}, vehicle_index: {}, time slot index: {}, requested computing resources: {}, requested storage resources: {}, bid: {}, payment: {}".format(
            self._type,
            self._index,
            self._vehicle_indexs,
            self._time_slot_index,
            self._requested_computing_resources,
            self._requested_storage_resources,
            self._bid,
            self._payment,
        )


class seller(object):
    
    def __init__(
        self,
        seller_type: str,    #  e.g., "vehicle", "edge node", "cloud"
        index: int,    #  the index of vehicle or edge node
        time_slot_index: int,
        offered_computing_resources: float,
        offered_storage_resources: float,
        ask: float,
        payment: float,
    ) -> None:
        self._type = seller_type
        self._index = index
        self._time_slot_index = time_slot_index
        self._offered_computing_resources = offered_computing_resources
        self._offered_storage_resources = offered_storage_resources
        self._ask = ask
        self._payment = payment
        
    def get_type(self) -> str:
        return self._type
    
    def get_index(self) -> int:
        return self._index
    
    def get_time_slot_index(self) -> int:
        return self._time_slot_index
    
    def get_offered_computing_resources(self) -> float:
        return self._offered_computing_resources
    
    def get_offered_storage_resources(self) -> float:
        return self._offered_storage_resources
    
    def get_ask(self) -> float:
        return self._ask
    
    def get_payment(self) -> float:
        return self._payment
    
    def set_type(self, seller_type: str) -> None:
        self._type = seller_type
        
    def set_index(self, index: int) -> None:
        self._index = index
    
    def set_time_slot_index(self, time_slot_index: int) -> None:
        self._time_slot_index = time_slot_index
    
    def set_offered_computing_resources(self, offered_computing_resources: float) -> None:
        self._offered_computing_resources = offered_computing_resources
        
    def set_offered_storage_resources(self, offered_storage_resources: float) -> None:
        self._offered_storage_resources = offered_storage_resources
        
    def set_ask(self, ask: float) -> None:
        self._ask = ask
    
    def set_payment(self, payment: float) -> None:
        self._payment = payment
    
    def __str__(self) -> str:
        return "Seller type: {}, index: {}, time slot index: {}, offered computing resources: {}, offered storage resources: {}, ask: {}, payment: {}".format(
            self._type,
            self._index,
            self._time_slot_index,
            self._offered_computing_resources,
            self._offered_storage_resources,
            self._ask,
            self._payment,
        )