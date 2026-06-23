# Assignment 3.1 — Library Checkout System

## The Problem

`library.py` is working code but terrible design.
One class does everything: knows item types, manages availability, calculates fees.

Your job: refactor it into 4 files, same pattern as Assignment 3.

---

## What You Need To Build

### 1. `items.py` — LibraryItem Class Hierarchy

- Abstract base class `LibraryItem` with `item_id`, `title`, and `loan_period_days` properties
- `Book(LibraryItem)` — loan period: 14 days
- `Magazine(LibraryItem)` — loan period: 7 days
- `DVD(LibraryItem)` — loan period: 3 days
- Each item type knows its own loan period (encapsulated, not hardcoded elsewhere)

### 2. `copy.py` — ItemCopy

A single physical copy of a library item. Tracks its own state.

- `ItemCopy(copy_id, item)` — holds a `LibraryItem` object
- `is_available()` → bool
- `checkout(member_id)` — raises `ValueError` if already checked out
- `return_item()` — raises `ValueError` if already available
- `due_date` property — `None` when available, set on checkout using `item.loan_period_days`
- `checked_out_by` property — member_id or `None`

### 3. `fee_strategy.py` — LateFeeStrategy

Abstract base + 3 concrete strategies:

- `LateFeeStrategy` — abstract, method: `calculate_fee(days_late, item_type)`
- `FlatDailyFee(rate_per_day)` — `rate * days_late`
- `TieredFee(base_rate, base_days, overflow_rate)` — first N days at base rate, remaining at overflow rate
- `NoFee()` — always returns 0.0

### 4. `library.py` — Library (refactored)

The orchestrator. Uses the above classes. Should have NO `if item_type == "book"` logic.

- `Library(fee_strategy=None)` — defaults to `FlatDailyFee(rate_per_day=0.50)`
- `add_item(item)` — accepts a `LibraryItem` object (not a string type)
- `checkout(member_id, item_id)` → `due_date` or `None`
- `return_item(item_id)` → `late_fee` (float) or `None`
- `get_available_items()` → list of item_ids
- `get_member_checkouts(member_id)` → list of item_ids
- `set_fee_strategy(strategy)` — swap strategy at runtime

---

## The Mapping (same pattern as Assignment 3)

| Assignment 3      | Assignment 3.1     |
|-------------------|--------------------|
| `Vehicle`         | `LibraryItem`      |
| `ParkingSpot`     | `ItemCopy`         |
| `PricingStrategy` | `LateFeeStrategy`  |
| `ParkingLot`      | `Library`          |

---

## Run Tests

```
python -m pytest test_library.py -v
```

Target: 33/33 passing.
