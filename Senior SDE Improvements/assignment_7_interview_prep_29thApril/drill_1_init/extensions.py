"""
Drill 1 — Your work goes here.

Goal: master super().__init__() with keyword-only args and forwarding.

Two subclasses to write:

1. VersionedRepository
     - new attribute: version (int, default 1)
     - new method: bump() — increments version
     - override: add() — increments version on every successful add
     - must forward ALL base kwargs (max_size, readonly) to super()
     - must use super().add() to do the actual work

2. NamespacedRepository
     - new attribute: namespace (str, REQUIRED — no default)
     - override: add(key, value) auto-prefixes "{namespace}:" before super().add
     - override: get(key) auto-prefixes "{namespace}:" before super().get
     - must forward ALL base kwargs (max_size, readonly) to super()

Read test_repository.py before writing. The tests are your spec.

Hint: the base signature is:
    def __init__(self, name: str, *, max_size: int = 100, readonly: bool = False)
The * means max_size and readonly are KEYWORD-ONLY. You can't pass them
positionally — they must be `max_size=...` in the call.
"""
from repository import Repository


class VersionedRepository(Repository):
    def __init__(self, name, *, max_size = 100, readonly = False, version = 1):
        super().__init__(name, max_size=max_size, readonly=readonly)
        self.version = version

    def bump(self):
        self.version += 1

    def add(self, key, value):
        super().add(key, value)
        self.version += 1


class NamespacedRepository(Repository):
    
    def __init__(self, name, namespace: str, *, max_size = 100, readonly = False):
        super().__init__(name, max_size=max_size, readonly=readonly)
        self.namespace = namespace

    def add(self, key, value):
        key = f"{self.namespace}:{key}"
        super().add(key, value)
        
    def get(self, key):
        key = f"{self.namespace}:{key}"
        super().get(key)

