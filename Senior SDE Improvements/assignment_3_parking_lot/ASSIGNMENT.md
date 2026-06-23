# Assignment 3: Parking Lot System (Encapsulation, Composition & Strategy Pattern)

## Difficulty: ★★★☆☆
## Focus: Encapsulation, Composition over Inheritance, Abstract Base Classes, Strategy Pattern

---

## Overview

You're given a working but poorly designed parking lot system. Everything is stuffed into one class using dicts for data. Your job is to **refactor it into proper OOP** and then **add pluggable pricing strategies**.

---

## Files

| File | What To Do |
|------|-----------|
| `parking_lot.py` | Starter code. **Refactor this** — keep the `ParkingLot` class but change its internals. |
| `vehicles.py` | **Create this file.** Vehicle class hierarchy (`Vehicle`, `Car`, `Motorcycle`, `Truck`). |
| `spots.py` | **Create this file.** `ParkingSpot` class with encapsulated state. |
| `pricing.py` | **Create this file.** Abstract `PricingStrategy` + concrete implementations. |
| `test_parking_lot.py` | Test suite. **Do NOT modify.** All tests must pass. |

---

## Part A: OOP Refactoring

### The Problem With the Starter Code
- Vehicles are dicts `{"license_plate": ..., "vehicle_type": ...}` — no behavior, no type safety
- Spots are dicts — state is exposed, no encapsulation
- Vehicle-to-spot-size mapping is hardcoded in `park_vehicle()` — vehicles should know their own sizes
- Everything is in one class — no separation of concerns

### What You Need To Build

**1. `vehicles.py` — Vehicle Class Hierarchy**
- Abstract base class `Vehicle` with `license_plate` and `allowed_spot_sizes` properties
- `Car(Vehicle)` — fits in medium, large
- `Motorcycle(Vehicle)` — fits in small, medium, large
- `Truck(Vehicle)` — fits in large only
- Each vehicle type **knows** what spot sizes it's allowed in (encapsulated, not hardcoded elsewhere)

**2. `spots.py` — ParkingSpot Class**
- `ParkingSpot(spot_id, size)` — encapsulates a single parking spot
- `is_available()` → bool
- `park(vehicle)` — parks a vehicle, records entry time, raises exception if occupied
- `remove()` → returns the vehicle, raises exception if empty
- `entry_time` property — when the vehicle was parked
- Internal state (vehicle, entry time) is managed through methods, not direct access

**3. `parking_lot.py` — Refactored ParkingLot**
- Constructor: `ParkingLot(small_spots, medium_spots, large_spots, pricing_strategy=None)`
- `park_vehicle(vehicle)` → spot_id or None. Takes a Vehicle object, not strings.
- `remove_vehicle(license_plate)` → dict with `license_plate`, `fee`, etc. or None
- `get_available_spots()` → dict of counts by size
- `is_full()` → bool
- `get_vehicle_info(license_plate)` → dict with vehicle details
- Uses `ParkingSpot` objects internally (composition)
- Prefers the smallest fitting spot

---

## Part B: Pricing Strategies (Strategy Pattern)

### The Problem
The starter code has `self.rate_per_hour = 2.0` hardcoded. What if you want daily rates? Tiered rates? EV charging rates? You'd have to keep adding `if/elif` branches.

### What You Need To Build

**`pricing.py` — Pricing Strategy Hierarchy**

- `PricingStrategy` — **abstract base class** (using `abc.ABC`). Cannot be instantiated. Has abstract method `calculate_fee(hours_parked, vehicle_type, spot_size)`.

- `HourlyPricing(rate_per_hour)` — charges `rate * hours`, minimum 1 hour (round up)

- `DailyPricing(rate_per_day)` — charges `rate * days`, minimum 1 day (round up any partial day)

- `TieredPricing(base_rate, base_hours, overflow_rate)` — first `base_hours` at `base_rate/hr`, remaining hours at `overflow_rate/hr`, minimum 1 hour total

**ParkingLot integration:**
- `ParkingLot` accepts an optional `pricing_strategy` in its constructor
- `set_pricing_strategy(strategy)` — swap at runtime
- `remove_vehicle` uses the current strategy to calculate the fee

---

## Design Decisions You Need to Make

- **Where does "vehicle fits in spot" logic live?** In the vehicle? In the spot? In the lot? (Hint: who *owns* that knowledge?)
- **How do you prevent invalid state?** What if someone tries to park in an occupied spot directly?
- **How does ParkingLot compose ParkingSpots?** List? Dict? What's the tradeoff?
- **How does the pricing strategy get the data it needs?** Who passes hours/vehicle_type/spot_size to it?

---

## Run Tests

```bash
cd assignment_3_parking_lot
pytest test_parking_lot.py -v
```

---

## Evaluation Criteria

| Criteria | What I'm Looking For |
|----------|---------------------|
| **Encapsulation** | ParkingSpot protects its state — you can't set `vehicle` directly from outside |
| **Composition** | ParkingLot is built FROM ParkingSpots and Vehicles, not dicts |
| **Inheritance** | Vehicle hierarchy is clean — shared behavior in base, specific in subclasses |
| **Abstraction** | PricingStrategy ABC enforces the contract — you can't accidentally skip `calculate_fee` |
| **Strategy Pattern** | Pricing is pluggable at runtime without touching ParkingLot internals |
| **No God Class** | ParkingLot delegates to its parts, doesn't do everything itself |

---

## Get Started

1. Read `parking_lot.py` — understand the current (bad) design
2. Read `test_parking_lot.py` — understand the expected interfaces
3. Create `vehicles.py` first (simplest)
4. Create `spots.py` next
5. Refactor `parking_lot.py` to use your new classes
6. Create `pricing.py` and wire it into ParkingLot
7. Run tests: `pytest test_parking_lot.py -v`

Good luck.
