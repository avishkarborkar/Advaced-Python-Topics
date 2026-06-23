"""
Drill 2 — base class. DO NOT MODIFY.

Cache is a dict-backed key-value store with two methods that return
meaningful values:
    get(key) -> value or None  (None means miss)
    put(key, value) -> bool    (False means overwrite, True means new entry)

Your subclasses must wrap these methods, *capture* the return values,
and react to them — without reimplementing the storage logic.
"""


class Cache:
    def __init__(self):
        self._storage: dict = {}

    def get(self, key):
        return self._storage.get(key)

    def put(self, key, value) -> bool:
        is_new = key not in self._storage
        self._storage[key] = value
        return is_new

    def keys(self):
        return list(self._storage.keys())

    def size(self) -> int:
        return len(self._storage)