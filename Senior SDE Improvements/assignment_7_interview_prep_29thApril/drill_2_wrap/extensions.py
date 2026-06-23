"""
Drill 2 — Your work goes here.

Goal: capture super()'s return value, react to it, pass it through.

1. MetricsCache
     - new attributes: hits (int), misses (int)
     - override: get(key) — call super().get, increment hits if not None, else misses
     - override: put(key, value) — call super().put, but DO NOT touch metrics; just pass through
     - the put override must return the bool from super().put unchanged

2. CapacityCache
     - new attribute: capacity (int)
     - override: put(key, value)
        * if key already present, just call super().put (no eviction)
        * if key is NEW and at capacity, evict the OLDEST key first, then super().put
        * use self.keys() (the public API) to find the oldest — do NOT touch _storage
     - "oldest" means the first key in insertion order — Python dicts preserve that

The pattern in both: capture super()'s return, decide based on it, return it.
"""
from cache import Cache


class MetricsCache(Cache):
     def __init__(self):
          super().__init__()
          self.hits = 0
          self.misses = 0
          
     def get(self, key):
          object = super().get(key)
          if object is not None:
               self.hits += 1
          else:
               self.misses += 1
          
          return object
          
     def put(self, key, value):
          return super().put(key, value)


class CapacityCache(Cache):
     def __init__(self, capacity: int):
         super().__init__()
         self.capacity = capacity

     def put(self, key, value):
          if key not in self.keys():          
               if self.size() >= self.capacity:
                    oldest = self.keys()[0]
                    del self._storage[oldest]
          return super().put(key, value) 