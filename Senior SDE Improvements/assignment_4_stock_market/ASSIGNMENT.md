# Assignment 4: Stock Market Event System

## Problem Statement

You have a **tightly coupled** stock market system where a `Stock` class directly calls methods on traders, analysts, and loggers whenever the price changes. Adding a new observer type requires modifying the `Stock` class.

Your job is to **refactor it using the Observer Pattern** to achieve loose coupling and extensibility.

---

## What You'll Learn

✅ **Observer Pattern** — Objects subscribe to events without tight coupling  
✅ **Event-Driven Architecture** — Publishers and subscribers interact through events  
✅ **Abstraction & Polymorphism** — Handle different observer types uniformly  
✅ **Dependency Inversion** — Depend on interfaces, not concrete classes  
✅ **Open/Closed Principle** — Add new observers/events without modifying existing code  
✅ **Separation of Concerns** — Each class has one reason to change  

---

## What You Need to Build

### 1. **events.py** — Event Hierarchy
Abstract base class `Event` with concrete subclasses:
- `Event` (abstract)
  - `PriceUpdateEvent(stock_symbol, old_price, new_price, timestamp)`
  - `VolumeThresholdEvent(stock_symbol, volume, threshold, timestamp)`
  - `TradingHaltEvent(stock_symbol, reason, timestamp)`

Each event knows what happened and when. Events are **immutable** (passed around, not modified).

---

### 2. **observers.py** — Observer Hierarchy
Abstract base class `EventObserver` with concrete subclasses:
- `EventObserver` (abstract)
  - `TraderObserver(name)` — executes trades based on price changes
  - `AnalystObserver(name)` — analyzes trends
  - `LoggerObserver()` — logs all events
  - `AlertObserver(email)` — sends alerts

Each observer **receives events** and decides what to do with them.

---

### 3. **event_bus.py** — The Broker
`EventBus` class that:
- `subscribe(event_type, observer)` — register observer for event type
- `unsubscribe(event_type, observer)` — unregister
- `publish(event)` — notify all subscribed observers

The **event bus is the middleman** — Stock doesn't know traders exist, traders don't know about Stock.

---

### 4. **stocks.py** — Observable Entities
`Stock` class that:
- `update_price(new_price)` — publishes a `PriceUpdateEvent`
- `update_volume(new_volume)` — publishes a `VolumeThresholdEvent` if threshold exceeded
- `halt_trading(reason)` — publishes a `TradingHaltEvent`

Stock **doesn't call observers directly** — it publishes events to the EventBus.

---

### 5. **stock_market.py** — The Orchestrator
`StockMarket` class that:
- `add_stock(stock_symbol)` — creates and registers a stock
- `add_observer(observer)` — subscribes observer to relevant events
- `update_price(stock_symbol, new_price)` — updates a stock's price
- `remove_observer(observer)` — cleans up subscriptions

The market **wires everything together** but remains loosely coupled.

---

## Key Design Principles

| Principle | What It Means | Example |
|-----------|---------------|---------|
| **Single Responsibility** | Each class has ONE reason to change | Stock changes price, TraderObserver reacts — two separate reasons |
| **Open/Closed** | Open for extension, closed for modification | Add new observer type without touching Stock or EventBus |
| **Dependency Inversion** | Depend on abstractions, not concrete classes | Stock publishes to EventBus (abstraction), not to Trader (concrete) |
| **Loose Coupling** | Objects communicate through interfaces | Stock and Trader know nothing about each other |
| **Composition Over Inheritance** | Use objects instead of deep hierarchies | Observers are composed into EventBus, not inherited |

---

## How It Should Work

```python
# Set up the market
market = StockMarket(event_bus=EventBus())

# Create stocks
apple = Stock(symbol="AAPL", initial_price=150.0)
market.add_stock(apple)

# Create observers
trader = TraderObserver(name="Alice")
analyst = AnalystObserver(name="Bob")
logger = LoggerObserver()

# Subscribe them — market wires everything
market.add_observer(trader)
market.add_observer(analyst)
market.add_observer(logger)

# Update price — triggers a cascade of events
market.update_price("AAPL", 152.50)
# ↓ Stock publishes PriceUpdateEvent
# ↓ EventBus notifies all subscribed observers
# ↓ Trader executes trade, Analyst analyzes, Logger records
```

---

## What Tests Expect

- ✅ `PriceUpdateEvent`, `VolumeThresholdEvent`, `TradingHaltEvent` exist
- ✅ `TraderObserver`, `AnalystObserver`, `LoggerObserver` exist
- ✅ `EventBus.subscribe()` and `publish()` work
- ✅ Observers receive the correct event type
- ✅ `Stock.update_price()` publishes to EventBus, not directly to observers
- ✅ No observer knows about Stock directly (loose coupling)
- ✅ New observer types can be added without modifying existing code

---

## Focus Areas

**These are the exact things coding interviews test:**

1. **Understanding coupling and cohesion** — Can you design systems where objects don't depend on each other?
2. **Pattern recognition** — When should you use Observer? Strategy? Factory?
3. **SOLID principles** — Do you write code that's easy to extend?
4. **Polymorphism** — Can you handle many observer types with one interface?
5. **Event-driven thinking** — Real systems work this way (message queues, event buses, pub/sub)

---

## Hints

- `Event` should be abstract — you never instantiate it directly
- `EventBus` should store subscriptions as `dict[event_type] → list[observers]`
- Observers should have an `on_event(event)` method that the bus calls
- Stock should have a reference to EventBus but NOT to individual observers
- Use `isinstance()` checks inside `on_event()` to handle specific event types

---

## Bonus Challenges

Once tests pass:
1. Add **event filtering** — subscribe to events with conditions (`PriceUpdateEvent where price > 200`)
2. Add **event priority** — some observers run first
3. Add **async handlers** — observers run in parallel (thread pool)
4. Add **event replay** — persist and re-publish events

But focus on passing tests first.