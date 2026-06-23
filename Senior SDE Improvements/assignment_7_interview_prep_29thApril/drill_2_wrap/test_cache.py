"""
Tests for Drill 2. DO NOT MODIFY.
Run with: pytest test_cache.py -v

The skill: capture super()'s return value. React to it. Pass it through.
This is the pattern that broke you on AuditedTaskList — drill it here.
"""
import pytest
from cache import Cache


# ─────────────────────────────────────────────
# 1. MetricsCache
# ─────────────────────────────────────────────
# get() must increment self.hits if value found, self.misses if None.
# put() must NOT touch metrics — only get() is metered.
# Both methods must use super() and pass through its return value unchanged.

class TestMetricsCache:

    def test_inherits_from_cache(self):
        from extensions import MetricsCache
        assert issubclass(MetricsCache, Cache)

    def test_starts_with_zero_metrics(self):
        from extensions import MetricsCache
        c = MetricsCache()
        assert c.hits == 0
        assert c.misses == 0

    def test_miss_increments_misses(self):
        from extensions import MetricsCache
        c = MetricsCache()
        result = c.get("nope")
        assert result is None
        assert c.misses == 1
        assert c.hits == 0

    def test_hit_increments_hits(self):
        from extensions import MetricsCache
        c = MetricsCache()
        c.put("k", 1)
        result = c.get("k")
        assert result == 1
        assert c.hits == 1
        assert c.misses == 0

    def test_put_does_not_change_metrics(self):
        from extensions import MetricsCache
        c = MetricsCache()
        c.put("a", 1)
        c.put("b", 2)
        c.put("a", 3)  # overwrite
        assert c.hits == 0
        assert c.misses == 0

    def test_mixed_access(self):
        from extensions import MetricsCache
        c = MetricsCache()
        c.put("k", 1)
        c.get("k")
        c.get("k")
        c.get("missing")
        c.get("also_missing")
        assert c.hits == 2
        assert c.misses == 2

    def test_put_return_passed_through(self):
        """put() must still return its bool — your wrapper can't swallow it."""
        from extensions import MetricsCache
        c = MetricsCache()
        assert c.put("new", 1) is True       # new entry
        assert c.put("new", 2) is False      # overwrite


# ─────────────────────────────────────────────
# 2. CapacityCache
# ─────────────────────────────────────────────
# Bounded cache. When full, evict the OLDEST key on a NEW put().
# Overwriting an existing key does NOT evict.
# Must use super().put() to do the actual storage work.
# Must use the public API (keys()) to find what to evict — no _storage access.

class TestCapacityCache:

    def test_inherits_from_cache(self):
        from extensions import CapacityCache
        assert issubclass(CapacityCache, Cache)

    def test_capacity_stored(self):
        from extensions import CapacityCache
        c = CapacityCache(capacity=3)
        assert c.capacity == 3

    def test_under_capacity_no_eviction(self):
        from extensions import CapacityCache
        c = CapacityCache(capacity=3)
        c.put("a", 1)
        c.put("b", 2)
        assert c.size() == 2
        assert c.get("a") == 1

    def test_at_capacity_evicts_oldest(self):
        from extensions import CapacityCache
        c = CapacityCache(capacity=3)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        c.put("d", 4)  # triggers eviction of "a"
        assert c.size() == 3
        assert c.get("a") is None
        assert c.get("b") == 2
        assert c.get("c") == 3
        assert c.get("d") == 4

    def test_overwrite_does_not_evict(self):
        """Overwriting an existing key shouldn't trigger eviction."""
        from extensions import CapacityCache
        c = CapacityCache(capacity=2)
        c.put("a", 1)
        c.put("b", 2)
        c.put("a", 99)  # overwrite, NOT a new entry
        assert c.size() == 2
        assert c.get("a") == 99
        assert c.get("b") == 2  # b still there

    def test_capacity_one_evicts_each_new(self):
        from extensions import CapacityCache
        c = CapacityCache(capacity=1)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        assert c.size() == 1
        assert c.get("c") == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])