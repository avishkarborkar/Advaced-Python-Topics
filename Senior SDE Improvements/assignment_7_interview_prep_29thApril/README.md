# `super()` Drill — Night Before the Interview

Four small exercises, each ~10 minutes, designed to make `super()` feel reflexive instead of mysterious.

**Time budget: 45–60 minutes total.** No exception.

---

## What `super()` actually does (read this once, slowly)

`super()` lets a subclass call the parent's version of a method. That's it. Two use cases cover ~95% of what you'll ever do with it:

### Use case 1: Inherit state in `__init__`

```python
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

class Car(Vehicle):
    def __init__(self, brand, doors):
        super().__init__(brand)   # ← runs Vehicle.__init__, sets self.brand
        self.doors = doors        # ← then adds Car-specific state
```

Without `super().__init__(brand)`, `self.brand` would never get set.

### Use case 2: Wrap a method (extend behavior, don't replace it)

```python
class Counter:
    def __init__(self):
        self.count = 0
    def increment(self):
        self.count += 1
        return self.count

class LoggedCounter(Counter):
    def increment(self):
        new_count = super().increment()   # ← parent does the real work
        print(f"counted to {new_count}")  # ← child adds a side effect
        return new_count                  # ← pass the result through
```

Notice the child doesn't reimplement counting. It calls `super()` to do the counting and just *adds* a log.

---

## The mental model

When you override a method on a subclass, ask yourself one question:

> **"Am I replacing this behavior, or adding to it?"**

- **Replacing** → don't call `super()`. Write fresh logic.
- **Adding** → call `super()` to do the original work, then add yours around it.

For most senior interview problems, the answer is **adding**. That's why `super()` shows up everywhere.

---

## The four shapes you'll practice

Each drill teaches one shape of `super()` usage. Do them in order — they build on each other.

| Drill | Shape | Skill |
|-------|-------|-------|
| 1 | `super().__init__()` | Inherit parent state, add new fields |
| 2 | `super().method()` then side-effect | Wrap a method to add behavior after |
| 3 | `result = super().method()` then act on result | Use the parent's return value |
| 4 | `super()` in multiple overridden methods | Coordinate several wrapped methods |

---

## How to work each drill

For each drill folder:

1. Open the **base file** (`vehicle.py`, `counter.py`, etc.) and read it. Don't skim.
2. Open the **test file** and read every test. The tests tell you exactly what your subclass must do.
3. Open the **stub file** (`extensions.py`) and write your code.
4. Run `pytest` in that folder. Iterate until green.
5. Move to the next drill.

If you're stuck for more than 5 minutes on any one drill, peek at `HINTS.md`. It's at the root of this directory.

---

## Rules

- **Do not modify the base file.** Ever. (This is the same rule as the real interview.)
- **Do not modify the test file.**
- **Each subclass must use `super()` at least once.** If you find a way to pass the tests without `super()`, you're missing the point of the drill — go back and use it.
- **Run tests after each drill, not at the end.** Tight feedback loops.

---

## When you're done

You should be able to look at any "extend this base class" problem and immediately answer:

1. Do I need `super().__init__()`? (Almost always yes if the subclass has its own `__init__`.)
2. Which methods am I *replacing* vs *wrapping*?
3. For wrapped methods — do I need the parent's return value?

If those three questions feel automatic, you're ready for the interview.