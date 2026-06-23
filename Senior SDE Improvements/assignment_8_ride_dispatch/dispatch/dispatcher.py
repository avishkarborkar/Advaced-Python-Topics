"""
Basic Dispatcher.

Manages drivers and matches incoming ride requests to the first
available driver (FIFO). Charges a flat fare per ride.
"""

from typing import Dict, List, Optional
from .models import Driver, Rider, Ride, Location

class Dispatcher:
    """
    Basic ride dispatcher.

    - Registers drivers
    - Matches the first non-busy driver to a ride request (FIFO)
    - Charges a flat fare configured at construction
    """

    def __init__(self, flat_fare: float = 10.0):
        self._drivers: Dict[str, Driver] = {}
        self._rides: List[Ride] = []
        self.flat_fare = flat_fare

    def register_driver(self, driver: Driver) -> None:
        """Add a driver to the system."""
        self._drivers[driver.driver_id] = driver

    def get_driver(self, driver_id: str) -> Optional[Driver]:
        """Look up a driver by ID."""
        return self._drivers.get(driver_id)

    def request_ride(self, rider: Rider, pickup: Location, dropoff: Location) -> Ride:
        """
        Match the first available driver to a ride request.

        Raises ValueError if no driver is available.
        """
        distances : Dict[Driver, float] = {}
        available_drivers = []

        #All available drivers
        for id, driver in self._drivers.items():
            if not driver.is_busy:
                available_drivers.append(driver)

        #Compute distance
        for driver in available_drivers:
            distances[driver] = driver.current_location.calculate_distance(pickup)

        if not distances:
            raise ValueError("No available drivers")
        
        sorted_drivers = sorted(distances, key=distances.get)
        ride = Ride(rider=rider, driver=sorted_drivers[0], fare=self.flat_fare, pickup=pickup, dropoff=dropoff)
        chosen_driver = sorted_drivers[0]
        chosen_driver.is_busy = True
        self._rides.append(ride)
        return ride

    def complete_ride(self, ride: Ride) -> None:
        """Mark the ride as completed and free up the driver."""
        ride.completed = True
        ride.driver.is_busy = False

    def all_rides(self) -> List[Ride]:
        """Return all rides ever issued."""
        return list(self._rides)
