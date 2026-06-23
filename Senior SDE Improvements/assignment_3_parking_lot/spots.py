import time
from vehicles import Vehicle

# Before this class - The original Parkinglot used raw dictionaries.\
# example - self.spots[spot_id] = {"size": "small", "vehicle": None, "entry_time": None}

# before — lot does everything
# spot["vehicle"] = {...}
# spot["entry_time"] = time.time()

# Now as we implemented encamsulation we ca simply: spot.park(vehicle)


class ParkingSpot:
    def __init__(self, spot_id: int, size: str):
        self.spot_id = spot_id
        self.size = size
        self._vehicle = None
        self._entry_time = None

    @property
    def entry_time(self):
        return self._entry_time
    
    def is_available(self):
        return self._vehicle is None
    
    def park(self, vehicle: Vehicle):
        if self._vehicle:
            raise ValueError('Already Occupied')
        
        self._vehicle = vehicle
        self._entry_time = time.time()

    def remove(self):
        if self._vehicle is None:
            raise ValueError('Already Empty')
    
        vehicle_in_spot = self._vehicle
        self._vehicle = None
        self._entry_time = None
        return vehicle_in_spot
        
    


