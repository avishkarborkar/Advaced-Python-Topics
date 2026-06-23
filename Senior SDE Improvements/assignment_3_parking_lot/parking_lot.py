"""
Parking Lot System — Starter Code

This is a WORKING but poorly designed parking lot.
Everything is crammed into one class. Your job is to refactor it
and extend it with new features.

Current features:
- Park vehicles (car, motorcycle, truck)
- Different spot sizes (small, medium, large)
- Entry/exit tracking
"""

# Things missing: 
# 1. All Vehicles are in one Dict and so layer of abstraction bw them.

import time
from spots import ParkingSpot
from pricing import PricingStrategy, HourlyPricing
from vehicles import Vehicle, Motorcycle, Truck, Car
from typing import Optional
class ParkingLot:
    """
    A parking lot that handles everything in one class.
    Works, but adding new features will be painful.
    """

    def __init__(self, small_spots, medium_spots, large_spots, pricing_strategy: Optional[PricingStrategy] = None):
        self.spots = {}
        spot_id = 1
        self.vehicle_spot_map = {}

        for _ in range(small_spots):
            self.spots[spot_id] = ParkingSpot(spot_id=spot_id, size='small')
            spot_id += 1

        for _ in range(medium_spots):
            self.spots[spot_id] = ParkingSpot(spot_id=spot_id, size='medium')
            spot_id += 1

        for _ in range(large_spots):
            self.spots[spot_id] = ParkingSpot(spot_id=spot_id, size='large')
            spot_id += 1

        self.pricing_strategy = pricing_strategy or HourlyPricing(rate_per_hour=2.0)

    def set_pricing_strategy(self, pricing_strategy):
        self.pricing_strategy = pricing_strategy


    def park_vehicle(self, vehicle: Vehicle):
        """
        Park a vehicle. Returns spot_id if successful, None if lot is full.
        """

        if vehicle.license_plate in self.vehicle_spot_map:
            return None
        
        for spot_id, spot in self.spots.items():
            if spot.is_available() and spot.size in vehicle.allowed_spot_sizes:
                spot.park(vehicle)
                self.vehicle_spot_map[vehicle.license_plate] = spot_id
                return spot_id
            
        return None

    def remove_vehicle(self, license_plate: Vehicle):
        """
        Remove a vehicle and calculate the fee.
        Returns (spot_id, fee) or None if vehicle not found.
        """

        if license_plate not in self.vehicle_spot_map:
            return None
        
        spot_id = self.vehicle_spot_map[license_plate]
        spot = self.spots[spot_id]
        hours = (time.time() - spot.entry_time) / 3600
        hours = max(1, round(hours))  # Minimum 1 hour
        spot.remove()
        del self.vehicle_spot_map[license_plate]
        fee = self.pricing_strategy.calculate_fee(hours_parked=hours)

        return {"license_plate": license_plate, "spot_id": spot_id, "fee": fee}


    def get_available_spots(self):
        """Returns count of available spots by size."""
        counts = {"small": 0, "medium": 0, "large": 0}
        for spot in self.spots.values():
            if spot.is_available():
                counts[spot.size] += 1
        return counts

    def is_full(self):
        """Check if all spots are occupied."""
        return all(not spot.is_available() for spot in self.spots.values())

    def get_vehicle_info(self, license_plate):
        """Get info about a parked vehicle."""
        if license_plate not in self.vehicle_spot_map:
            return None
        
        spot_id = self.vehicle_spot_map[license_plate]
        spot = self.spots[spot_id]
        
        return {
            "license_plate": license_plate,
            "vehicle_type": spot._vehicle.__class__.__name__.lower(),
            "spot_id": spot_id,
            "spot_size": spot.size,
            "entry_time": spot.entry_time,
        }


# Bad Design I found
# 1. There are 4 things the base class is doing: park_vehicle, remove_vehicle, get_available_spots, get_available_spots, get_vehicle_info, is_full.

# Solution I did
# 1. We did not make subclasses for the class methods but instead extracted from Vehicle, ParkingSpot, PRicingStrategy
# You didn't make subclasses of ParkingLot. What you actually did:

# Extracted Vehicle hierarchy — vehicles know their own rules
# Extracted ParkingSpot — spots manage their own state
# Extracted PricingStrategy — pricing is swappable, not hardcoded