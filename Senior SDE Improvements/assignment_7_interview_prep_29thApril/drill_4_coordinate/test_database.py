"""
Tests for Drill 4. DO NOT MODIFY.
Run with: pytest test_database.py -v

This is the AuditedTaskList shape. Coordinate three overrides, each wrapping
super() with a side effect gated by super()'s return value.
"""
import pytest
from database import Database


# ─────────────────────────────────────────────
# 1. AuditedDatabase
# ─────────────────────────────────────────────
# Override insert/update/delete. Each:
#   - calls super() to do the real work
#   - captures the bool return
#   - logs the action ONLY on success
#   - returns the bool unchanged
#
# Read methods (find, all_keys) are NOT logged.
# Failed mutations are NOT logged.

class TestAuditedDatabase:

    def test_inherits_from_database(self):
        from extensions import AuditedDatabase
        assert issubclass(AuditedDatabase, Database)

    def test_audit_log_starts_empty(self):
        from extensions import AuditedDatabase
        d = AuditedDatabase()
        assert d.audit_log == []

    def test_successful_insert_logs(self):
        from extensions import AuditedDatabase
        d = AuditedDatabase()
        ok = d.insert("u1", {"name": "alice"})
        assert ok is True
        assert len(d.audit_log) == 1
        assert "insert" in d.audit_log[0].lower()
        assert "u1" in d.audit_log[0]

    def test_failed_insert_does_not_log(self):
        from extensions import AuditedDatabase
        d = AuditedDatabase()
        d.insert("u1", {"name": "alice"})
        d.audit_log.clear()
        ok = d.insert("u1", {"name": "bob"})  # already exists
        assert ok is False
        assert len(d.audit_log) == 0

    def test_successful_update_logs(self):
        from extensions import AuditedDatabase
        d = AuditedDatabase()
        d.insert("u1", {"name": "alice"})
        d.audit_log.clear()
        d.update("u1", {"name": "alice2"})
        assert len(d.audit_log) == 1
        assert "update" in d.audit_log[0].lower()

    def test_failed_update_does_not_log(self):
        from extensions import AuditedDatabase
        d = AuditedDatabase()
        ok = d.update("missing", {})
        assert ok is False
        assert len(d.audit_log) == 0

    def test_successful_delete_logs(self):
        from extensions import AuditedDatabase
        d = AuditedDatabase()
        d.insert("u1", {})
        d.audit_log.clear()
        d.delete("u1")
        assert len(d.audit_log) == 1
        assert "delete" in d.audit_log[0].lower()

    def test_failed_delete_does_not_log(self):
        from extensions import AuditedDatabase
        d = AuditedDatabase()
        ok = d.delete("missing")
        assert ok is False
        assert len(d.audit_log) == 0

    def test_find_does_not_log(self):
        from extensions import AuditedDatabase
        d = AuditedDatabase()
        d.insert("u1", {"x": 1})
        d.audit_log.clear()
        d.find("u1")
        d.find("missing")
        assert len(d.audit_log) == 0

    def test_returns_super_value_unchanged(self):
        """Your overrides must pass through super()'s bool — don't swallow or invert."""
        from extensions import AuditedDatabase
        d = AuditedDatabase()
        assert d.insert("a", {}) is True
        assert d.insert("a", {}) is False  # duplicate
        assert d.update("a", {}) is True
        assert d.update("missing", {}) is False
        assert d.delete("a") is True
        assert d.delete("a") is False  # already deleted

    def test_log_order_matches_call_order(self):
        from extensions import AuditedDatabase
        d = AuditedDatabase()
        d.insert("u1", {})
        d.insert("u2", {})
        d.update("u1", {"v": 1})
        d.delete("u2")
        actions = [entry.split()[0].lower() for entry in d.audit_log]
        assert actions == ["insert", "insert", "update", "delete"]


# ─────────────────────────────────────────────
# 2. RestrictedDatabase
# ─────────────────────────────────────────────
# Override insert/update/delete. Each:
#   - if the key is in self.locked_keys, return False WITHOUT calling super()
#   - otherwise, defer to super()
# This combines drills 3 + 4: pre-check, then super (or skip super entirely).

class TestRestrictedDatabase:

    def test_inherits_from_database(self):
        from extensions import RestrictedDatabase
        assert issubclass(RestrictedDatabase, Database)

    def test_locked_keys_init(self):
        from extensions import RestrictedDatabase
        d = RestrictedDatabase(locked_keys={"system"})
        assert "system" in d.locked_keys

    def test_locked_key_insert_blocked(self):
        from extensions import RestrictedDatabase
        d = RestrictedDatabase(locked_keys={"system"})
        ok = d.insert("system", {"x": 1})
        assert ok is False
        assert d.find("system") is None  # super() never ran

    def test_unlocked_key_insert_works(self):
        from extensions import RestrictedDatabase
        d = RestrictedDatabase(locked_keys={"system"})
        ok = d.insert("user", {"x": 1})
        assert ok is True
        assert d.find("user") == {"x": 1}

    def test_locked_key_update_blocked(self):
        from extensions import RestrictedDatabase
        d = RestrictedDatabase(locked_keys={"system"})
        ok = d.update("system", {"x": 1})
        assert ok is False

    def test_locked_key_delete_blocked(self):
        from extensions import RestrictedDatabase
        d = RestrictedDatabase(locked_keys={"system"})
        ok = d.delete("system")
        assert ok is False

    def test_find_not_restricted(self):
        """find() is read-only — no restriction."""
        from extensions import RestrictedDatabase
        d = RestrictedDatabase(locked_keys={"system"})
        # locked or not, find should pass through
        assert d.find("system") is None

    def test_default_locked_keys_empty(self):
        """If no locked_keys provided, behave like Database."""
        from extensions import RestrictedDatabase
        d = RestrictedDatabase()
        assert d.insert("anything", {}) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
