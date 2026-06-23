# Interview Tickets: RideWave — Geo-Aware Dispatch

## Background

This repository contains a working basic dispatch system in the [`dispatch/`](dispatch/) package.
It supports:

- Registering drivers
- Matching the first available driver to a ride request (FIFO)
- A flat fare per ride
- Marking rides as completed

Your task is to extend it into a **geo-aware dispatch system** with surge pricing
and proper ride lifecycle management.

### Read first, code later

1. Read [dispatch/models.py](dispatch/models.py) and [dispatch/dispatcher.py](dispatch/dispatcher.py) end-to-end before doing anything else.
2. Fill out [DESIGN_TEMPLATE.md](DESIGN_TEMPLATE.md) before opening any `.py` file to write code.
3. Only after the design doc is filled in, start implementing.

The design doc is the actual engineering. The code is transcription.

---

## Ticket 1: Add Locations and Distance-Based Matching

**Priority**: High
**Estimated Time**: 25–30 minutes

### Description

Add a notion of geographic location, and change the matching strategy from FIFO
to **nearest available driver** to the pickup location.

### Requirements

1. Introduce a `Location` type with `x` and `y` coordinates and a method to
   compute Euclidean distance to another location.
2. Drivers must have a `location` attribute (current location).
3. A ride request takes a `pickup` and `dropoff`, both Locations.
4. `request_ride` must find the **nearest** available driver to the pickup,
   not the first one registered.
5. If no driver is available, still raise `ValueError("No available drivers")`.

### Acceptance Criteria

- [ ] Locations are first-class — exist outside `Driver` and `Ride`
- [ ] Existing fare and lifecycle behavior is preserved
- [ ] When two drivers are available, the nearer one to the pickup is chosen
- [ ] You can articulate (in the design doc) why `Location` lives where it does

---

## Ticket 2: Replace Boolean Flags with State Machines

**Priority**: High
**Estimated Time**: 25–30 minutes
**Dependencies**: Ticket 1

### Description

The current code uses booleans (`Driver.is_busy`, `Ride.completed`) to track state.
This breaks down once we add cancellation and an explicit "ride started" step.
Replace these with proper state enums.

### Requirements

1. **DriverStatus** enum: `OFFLINE`, `AVAILABLE`, `ON_TRIP`
2. **RideStatus** enum: `REQUESTED`, `ASSIGNED`, `IN_PROGRESS`, `COMPLETED`, `CANCELLED`
3. Drivers start `OFFLINE`. Add `go_online()` and `go_offline()` methods.
4. Only `AVAILABLE` drivers are eligible for matching.
5. New ride lifecycle methods on the dispatcher:
   - `start_ride(ride)` — `ASSIGNED → IN_PROGRESS`
   - `complete_ride(ride)` — `IN_PROGRESS → COMPLETED`, driver returns to `AVAILABLE`
   - `cancel_ride(ride)` — from any active state → `CANCELLED`, driver returns to `AVAILABLE` if assigned
6. Each driver should keep a `ride_history` list of completed rides.

### Acceptance Criteria

- [ ] All boolean flags removed
- [ ] Invalid transitions raise a clear error (e.g. starting a CANCELLED ride)
- [ ] A cancelled ride from IN_PROGRESS still frees the driver
- [ ] A driver can complete a ride and immediately take another

---

## Ticket 3: Distance-Based Fare with Surge Pricing

**Priority**: Medium
**Estimated Time**: 15–20 minutes
**Dependencies**: Ticket 1

### Description

Replace the flat fare with a distance-based fare that supports surge pricing.

### Requirements

1. Dispatcher accepts: `base_fare` (default `2.0`), `rate_per_km` (default `1.0`),
   `surge_multiplier` (default `1.0`).
2. Fare formula: `base_fare + (distance * rate_per_km * surge_multiplier)`,
   where distance is the Euclidean distance from pickup to dropoff.
3. Surge can be updated on the dispatcher at runtime.
4. Fare is locked in at request time — later surge changes do not retro-apply.

### Acceptance Criteria

- [ ] Fare formula matches the spec exactly
- [ ] Surge changes affect new rides, not existing ones
- [ ] The flat-fare dispatcher constructor argument is gone

---

## Ticket 4 (BONUS): Demonstration Script

**Priority**: Low
**Estimated Time**: 10 minutes

Create `demo.py` that exercises the new system end-to-end:
- Register two drivers at different locations, both online
- Request a ride; show that the nearer one is chosen
- Start, complete, and verify the driver's history
- Set a surge, request another ride, show the higher fare
- Cancel an in-progress ride and verify the driver is freed

---

## Evaluation Criteria

1. **You read the existing code before designing.** Reflected in DESIGN_TEMPLATE Section 0.
2. **Reuse vs replace decisions are explicit and defensible.** Reflected in Section 3.
3. **The new abstractions are coordinated** — state machines, locations, fares all fit together cleanly.
4. **The acceptance criteria are met without breaking the original behavior** that should still hold.
5. **Honest class relationships** — no inheritance that doesn't make sense, no leaky state.

---

## Notes

- You may modify any file in `dispatch/`. The existing code is a starting point, not a contract.
- Some ideas you may need to introduce: a state-transition guard, a separate `Matcher` class, an `__init__.py` re-export. Only add what your design calls for.
- If you find yourself coding without having decided ownership in DESIGN_TEMPLATE Section 3, stop and go back.
