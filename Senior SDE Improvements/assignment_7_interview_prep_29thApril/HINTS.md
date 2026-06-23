# Hints

Only peek when stuck for 5+ minutes on a single test. Each hint is **progressive** — try the first hint, run tests again, escalate only if needed.

---

## Drill 1 — `super().__init__()`

**Hint 1:** The base signature is `__init__(self, name: str, *, max_size=100, readonly=False)`. The `*` means everything after it is keyword-only. When you call `super().__init__(...)`, you must pass `max_size` and `readonly` *by name*, not positionally.

**Hint 2:** Your subclass `__init__` should accept all the parent's args plus its own. The cleanest pattern is to just take them all explicitly:

```python
def __init__(self, name, *, max_size=100, readonly=False, version=1):
    super().__init__(name, max_size=max_size, readonly=readonly)
    self.version = version
```

**Hint 3:** For `VersionedRepository.add`, the test `test_add_uses_super` checks that `r._index` gets populated. Only the base's `add()` populates `_index`. So your override must call `super().add(key, value)` — don't reimplement.

**Hint 4:** For `NamespacedRepository`, both `add` and `get` need to prefix the key with `f"{self.namespace}:{key}"` *before* calling super.

---

## Drill 2 — Wrap and use the return value

**Hint 1:** For `MetricsCache.get`, you need to call `super().get(key)`, capture the return, and look at it. If it's `None`, increment misses; otherwise, increment hits. Don't forget to return the value.

```python
def get(self, key):
    value = super().get(key)
    if value is None:
        self.misses += 1
    else:
        self.hits += 1
    return value
```

**Hint 2:** For `CapacityCache.put`, the order matters: check capacity *before* calling super, but ONLY if it's a new key. Use `key in self.keys()` (the public API) to check.

```python
def put(self, key, value):
    if key not in self.keys() and self.size() >= self.capacity:
        oldest = self.keys()[0]
        super().__delitem__(...)  # ← but Cache has no delete method...
```

**Hint 3 (continued):** Cache has no public delete. You'll need to access the storage indirectly. The test allows you to use the public API, but if you must touch `_storage` for the eviction, that's a real interview discussion point ("the base doesn't expose deletion — I'd advocate adding a `remove()` method"). For this drill, accessing `self._storage` to remove the oldest is acceptable — but call it out as a code-smell to a real interviewer.

---

## Drill 3 — Conditional super

**Hint 1:** For `EmailValidator`, call super first, return its failure if any, then check for `@` and `.`:

```python
def validate(self, value):
    ok, reason = super().validate(value)
    if not ok:
        return ok, reason
    if "@" not in value:
        return False, "must contain '@'"
    if "." not in value:
        return False, "must contain '.'"
    return True, None
```

**Hint 2:** For `SkippableValidator`, check for the prefix BEFORE calling super:

```python
def validate(self, value):
    if isinstance(value, str) and value.startswith("trusted:"):
        return True, None
    return super().validate(value)
```

**Hint 3:** For `CompositeValidator`, the unsafe check must run first. If safe, fall through to super. The order is important — running super first would let `<script>` strings pass if they happened to be the right length.

---

## Drill 4 — Coordinate multiple overrides

**Hint 1:** For `AuditedDatabase`, the pattern repeats three times. Resist the urge to abstract it. Just write it out:

```python
class AuditedDatabase(Database):
    def __init__(self):
        super().__init__()
        self.audit_log = []

    def insert(self, key, record):
        ok = super().insert(key, record)
        if ok:
            self.audit_log.append(f"insert {key}")
        return ok

    # ...same for update and delete
```

**Hint 2:** For `RestrictedDatabase`, `locked_keys` is a kwarg. Default it to an empty set:

```python
def __init__(self, locked_keys=None):
    super().__init__()
    self.locked_keys = locked_keys or set()
```

**Hint 3:** The pre-check pattern for restricted keys:

```python
def insert(self, key, record):
    if key in self.locked_keys:
        return False
    return super().insert(key, record)
```

---

## After all drills

If you finished all four with green tests, go back to **Assignment 7's `AuditedTaskList`** and rewrite it from scratch using the Drill 4 pattern. It should take you 3 minutes now.

That's the proof you've internalized this. If `AuditedTaskList` still feels hard after these drills, redo Drill 4.
