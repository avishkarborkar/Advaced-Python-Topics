"""
Core models for the basic dispatch system.

Currently supports a single-area, FIFO-matched ride service with flat-rate fares.
"""

from typing import Optional

class Location:
    """
    Holds x, y, coordinates
    """

    def __init__(self, x: float, y: float):
        self.x_coord = x
        self.y_coord = y
    
    def calculate_distance(self, other: Location) -> float:
        """
        returns euclidean distance between 2 points"""
        x1, y1 = self.x_coord, self.y_coord
        x2, y2 = other.x_coord, other.y_coord

        distance = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
        return distance
    

class Driver:
    """
    A driver in the dispatch system.

    Drivers are simple resources — either busy or not. There is no notion
    of location, status enum, or trip lifecycle yet.
    """

    def __init__(self, driver_id: str, name: str, current_location: Location):
        self.driver_id = driver_id
        self.name = name
        self.is_busy = False
        self.current_location = current_location


class Rider:
    """A rider in the dispatch system."""

    def __init__(self, rider_id: str, name: str):
        self.rider_id = rider_id
        self.name = name


class Ride:
    """
    A completed or in-flight ride.

    A ride has a fixed flat fare assigned at creation time.
    There is no concept of distance, surge pricing, or state machine.
    """

    def __init__(self, rider: Rider, driver: Driver, fare: float, pickup: Location, dropoff: Location):
        self.rider = rider
        self.driver = driver
        self.fare = fare
        self.completed = False
        self.pickup = pickup
        self.dropoff = dropoff

