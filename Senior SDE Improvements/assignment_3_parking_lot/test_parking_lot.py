"""
Tests for the refactored Parking Lot system.
DO NOT MODIFY THIS FILE.
"""
import pytest


# ============================================================
# PART A — Core OOP Refactoring
# ============================================================

class TestVehicleClasses:
    """Vehicles should be proper classes, not dicts."""

    def test_vehicle_base_class_exists(self):
        from vehicles import Vehicle
        assert Vehicle is not None

    def test_car_is_vehicle(self):
        from vehicles import Vehicle, Car
        car = Car("ABC-123")
        assert isinstance(car, Vehicle)

    def test_motorcycle_is_vehicle(self):
        from vehicles import Vehicle, Motorcycle
        mc = Motorcycle("MOTO-1")
        assert isinstance(mc, Vehicle)

    def test_truck_is_vehicle(self):
        from vehicles import Vehicle, Truck
        truck = Truck("TRUCK-1")
        assert isinstance(truck, Vehicle)

    def test_vehicle_has_license_plate(self):
        from vehicles import Car
        car = Car("XYZ-789")
        assert car.license_plate == "XYZ-789"

    def test_vehicle_knows_allowed_spot_sizes(self):
        """Each vehicle type should know what spot sizes it can fit in."""
        from vehicles import Car, Motorcycle, Truck
        assert "small" in Motorcycle("M1").allowed_spot_sizes
        assert "medium" in Car("C1").allowed_spot_sizes
        assert "large" in Truck("T1").allowed_spot_sizes
        assert "small" not in Car("C2").allowed_spot_sizes
        assert "small" not in Truck("T2").allowed_spot_sizes
        assert "medium" not in Truck("T3").allowed_spot_sizes


class TestSpotClasses:
    """Parking spots should be proper classes with encapsulated state."""

    def test_spot_class_exists(self):
        from spots import ParkingSpot
        assert ParkingSpot is not None

    def test_spot_has_id_and_size(self):
        from spots import ParkingSpot
        spot = ParkingSpot(spot_id=1, size="medium")
        assert spot.spot_id == 1
        assert spot.size == "medium"

    def test_spot_is_available_when_empty(self):
        from spots import ParkingSpot
        spot = ParkingSpot(spot_id=1, size="medium")
        assert spot.is_available() is True

    def test_spot_not_available_when_occupied(self):
        from spots import ParkingSpot
        from vehicles import Car
        spot = ParkingSpot(spot_id=1, size="medium")
        spot.park(Car("ABC-123"))
        assert spot.is_available() is False

    def test_spot_park_and_remove(self):
        from spots import ParkingSpot
        from vehicles import Car
        spot = ParkingSpot(spot_id=1, size="medium")
        car = Car("ABC-123")
        spot.park(car)
        removed = spot.remove()
        assert removed.license_plate == "ABC-123"
        assert spot.is_available() is True

    def test_spot_cannot_double_park(self):
        from spots import ParkingSpot
        from vehicles import Car
        spot = ParkingSpot(spot_id=1, size="medium")
        spot.park(Car("A"))
        with pytest.raises(Exception):
            spot.park(Car("B"))

    def test_spot_cannot_remove_when_empty(self):
        from spots import ParkingSpot
        spot = ParkingSpot(spot_id=1, size="medium")
        with pytest.raises(Exception):
            spot.remove()

    def test_spot_tracks_entry_time(self):
        from spots import ParkingSpot
        from vehicles import Car
        spot = ParkingSpot(spot_id=1, size="medium")
        spot.park(Car("ABC-123"))
        assert spot.entry_time is not None


class TestParkingLotCore:
    """Core parking lot functionality with proper OOP."""

    def test_parking_lot_creation(self):
        from parking_lot import ParkingLot
        lot = ParkingLot(small_spots=2, medium_spots=3, large_spots=1)
        available = lot.get_available_spots()
        assert available["small"] == 2
        assert available["medium"] == 3
        assert available["large"] == 1

    def test_park_car(self):
        from parking_lot import ParkingLot
        from vehicles import Car
        lot = ParkingLot(small_spots=0, medium_spots=2, large_spots=0)
        car = Car("ABC-123")
        spot_id = lot.park_vehicle(car)
        assert spot_id is not None

    def test_park_motorcycle_in_small_spot(self):
        from parking_lot import ParkingLot
        from vehicles import Motorcycle
        lot = ParkingLot(small_spots=1, medium_spots=0, large_spots=0)
        mc = Motorcycle("MOTO-1")
        spot_id = lot.park_vehicle(mc)
        assert spot_id is not None

    def test_truck_needs_large_spot(self):
        from parking_lot import ParkingLot
        from vehicles import Truck
        lot = ParkingLot(small_spots=5, medium_spots=5, large_spots=0)
        truck = Truck("TRUCK-1")
        spot_id = lot.park_vehicle(truck)
        assert spot_id is None  # No large spots

    def test_cannot_park_same_vehicle_twice(self):
        from parking_lot import ParkingLot
        from vehicles import Car
        lot = ParkingLot(small_spots=0, medium_spots=2, large_spots=0)
        car = Car("ABC-123")
        lot.park_vehicle(car)
        result = lot.park_vehicle(car)
        assert result is None

    def test_remove_vehicle(self):
        from parking_lot import ParkingLot
        from vehicles import Car
        lot = ParkingLot(small_spots=0, medium_spots=2, large_spots=0)
        car = Car("ABC-123")
        lot.park_vehicle(car)
        result = lot.remove_vehicle("ABC-123")
        assert result is not None
        assert result["license_plate"] == "ABC-123"

    def test_remove_nonexistent_vehicle(self):
        from parking_lot import ParkingLot
        lot = ParkingLot(small_spots=0, medium_spots=2, large_spots=0)
        result = lot.remove_vehicle("NOPE")
        assert result is None

    def test_spot_freed_after_removal(self):
        from parking_lot import ParkingLot
        from vehicles import Car
        lot = ParkingLot(small_spots=0, medium_spots=1, large_spots=0)
        car = Car("ABC-123")
        lot.park_vehicle(car)
        assert lot.get_available_spots()["medium"] == 0
        lot.remove_vehicle("ABC-123")
        assert lot.get_available_spots()["medium"] == 1

    def test_lot_full(self):
        from parking_lot import ParkingLot
        from vehicles import Car
        lot = ParkingLot(small_spots=0, medium_spots=1, large_spots=0)
        lot.park_vehicle(Car("A"))
        assert lot.is_full() is True

    def test_prefers_smallest_fitting_spot(self):
        """A car should go in a medium spot before a large spot."""
        from parking_lot import ParkingLot
        from vehicles import Car
        lot = ParkingLot(small_spots=0, medium_spots=1, large_spots=1)
        car = Car("ABC-123")
        spot_id = lot.park_vehicle(car)
        # The medium spot should be used first (smaller id = created first)
        info = lot.get_vehicle_info("ABC-123")
        assert info["spot_size"] == "medium"


# ============================================================
# PART B — Pricing Strategies (Strategy Pattern)
# ============================================================

class TestPricingStrategies:
    """Pricing should be pluggable via strategy pattern, not hardcoded."""

    def test_hourly_pricing(self):
        from pricing import HourlyPricing
        strategy = HourlyPricing(rate_per_hour=5.0)
        # 2 hours parked
        fee = strategy.calculate_fee(hours_parked=2, vehicle_type="car", spot_size="medium")
        assert fee == 10.0

    def test_hourly_pricing_minimum_one_hour(self):
        from pricing import HourlyPricing
        strategy = HourlyPricing(rate_per_hour=5.0)
        fee = strategy.calculate_fee(hours_parked=0.25, vehicle_type="car", spot_size="medium")
        assert fee == 5.0  # Minimum 1 hour

    def test_daily_pricing(self):
        from pricing import DailyPricing
        strategy = DailyPricing(rate_per_day=20.0)
        # 25 hours = 2 days
        fee = strategy.calculate_fee(hours_parked=25, vehicle_type="car", spot_size="medium")
        assert fee == 40.0

    def test_daily_pricing_minimum_one_day(self):
        from pricing import DailyPricing
        strategy = DailyPricing(rate_per_day=20.0)
        fee = strategy.calculate_fee(hours_parked=3, vehicle_type="car", spot_size="medium")
        assert fee == 20.0

    def test_tiered_pricing(self):
        """First 2 hours at base rate, then higher rate after."""
        from pricing import TieredPricing
        strategy = TieredPricing(base_rate=3.0, base_hours=2, overflow_rate=5.0)
        # 5 hours: 2 hours * $3 + 3 hours * $5 = $6 + $15 = $21
        fee = strategy.calculate_fee(hours_parked=5, vehicle_type="car", spot_size="medium")
        assert fee == 21.0

    def test_tiered_pricing_within_base(self):
        from pricing import TieredPricing
        strategy = TieredPricing(base_rate=3.0, base_hours=2, overflow_rate=5.0)
        fee = strategy.calculate_fee(hours_parked=1, vehicle_type="car", spot_size="medium")
        assert fee == 3.0

    def test_pricing_strategy_is_abstract(self):
        """PricingStrategy should be an abstract base class."""
        from pricing import PricingStrategy
        with pytest.raises(TypeError):
            PricingStrategy()

    def test_parking_lot_uses_pricing_strategy(self):
        """ParkingLot should accept a pricing strategy."""
        from parking_lot import ParkingLot
        from pricing import HourlyPricing
        from vehicles import Car
        lot = ParkingLot(
            small_spots=0, medium_spots=2, large_spots=0,
            pricing_strategy=HourlyPricing(rate_per_hour=10.0)
        )
        car = Car("ABC-123")
        lot.park_vehicle(car)
        result = lot.remove_vehicle("ABC-123")
        # Should use the hourly strategy, minimum 1 hour = $10
        assert result["fee"] >= 10.0

    def test_swap_pricing_strategy(self):
        """Should be able to change pricing strategy at runtime."""
        from parking_lot import ParkingLot
        from pricing import HourlyPricing, DailyPricing
        lot = ParkingLot(
            small_spots=0, medium_spots=2, large_spots=0,
            pricing_strategy=HourlyPricing(rate_per_hour=5.0)
        )
        lot.set_pricing_strategy(DailyPricing(rate_per_day=20.0))
        # Just verify it doesn't crash — the strategy was swapped
        from vehicles import Car
        lot.park_vehicle(Car("ABC-123"))
        result = lot.remove_vehicle("ABC-123")
        assert result["fee"] >= 20.0  # Daily minimum


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
