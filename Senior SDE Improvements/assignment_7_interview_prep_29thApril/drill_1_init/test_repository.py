"""
Tests for Drill 1. DO NOT MODIFY.
Run with: pytest test_repository.py -v

This drill is harder than it looks. The base has keyword-only args, lazy
state, and methods that depend on __init__ having run. Skip super().__init__
and you get half-initialized objects with confusing failures.
"""
import pytest
from repository import Repository


class TestBaseStillWorks:
    def test_base_init(self):
        r = Repository("main", max_size=10, readonly=False)
        assert r.name == "main"
        assert r.max_size == 10
        assert r.readonly is False
        assert r.size() == 0


# ─────────────────────────────────────────────
# 1. VersionedRepository
# ─────────────────────────────────────────────
# Adds: a `version` int (default 1).
# Adds: a `bump()` method that increments version.
# Forwards: ALL base kwargs (max_size, readonly).
# Overrides: add() — increments version on every successful add.

class TestVersionedRepository:

    def test_inherits_from_repository(self):
        from extensions import VersionedRepository
        assert issubclass(VersionedRepository, Repository)

    def test_default_version_is_1(self):
        from extensions import VersionedRepository
        r = VersionedRepository("v")
        assert r.version == 1

    def test_explicit_version(self):
        from extensions import VersionedRepository
        r = VersionedRepository("v", version=5)
        assert r.version == 5

    def test_forwards_keyword_only_args(self):
        """If you forget to forward max_size, this test fails."""
        from extensions import VersionedRepository
        r = VersionedRepository("v", max_size=3, readonly=False)
        assert r.max_size == 3
        r.add("a", 1)
        r.add("b", 2)
        r.add("c", 3)
        with pytest.raises(RuntimeError):
            r.add("d", 4)

    def test_forwards_readonly(self):
        from extensions import VersionedRepository
        r = VersionedRepository("v", readonly=True)
        with pytest.raises(RuntimeError):
            r.add("x", 1)

    def test_add_bumps_version(self):
        from extensions import VersionedRepository
        r = VersionedRepository("v")
        assert r.version == 1
        r.add("a", 1)
        assert r.version == 2
        r.add("b", 2)
        assert r.version == 3

    def test_add_uses_super(self):
        """If you reimplemented add() instead of using super().add(),
        the base's _index dict won't be populated."""
        from extensions import VersionedRepository
        r = VersionedRepository("v")
        r.add("apple", 1)
        r.add("ant", 2)
        assert "a" in r._index

    def test_bump_method(self):
        from extensions import VersionedRepository
        r = VersionedRepository("v")
        r.bump()
        r.bump()
        assert r.version == 3


# ─────────────────────────────────────────────
# 2. NamespacedRepository
# ─────────────────────────────────────────────
# Adds: a `namespace` str (REQUIRED — no default).
# Behavior: keys are auto-prefixed with "{namespace}:" on add() and get().
# Forwards: ALL base kwargs.

class TestNamespacedRepository:

    def test_inherits_from_repository(self):
        from extensions import NamespacedRepository
        assert issubclass(NamespacedRepository, Repository)

    def test_namespace_required(self):
        from extensions import NamespacedRepository
        with pytest.raises(TypeError):
            NamespacedRepository("r")

    def test_namespace_stored(self):
        from extensions import NamespacedRepository
        r = NamespacedRepository("r", namespace="users")
        assert r.namespace == "users"

    def test_add_prefixes_key(self):
        from extensions import NamespacedRepository
        r = NamespacedRepository("r", namespace="users")
        r.add("alice", {"role": "admin"})
        assert r.get("users:alice") == {"role": "admin"}

    def test_get_prefixes_key(self):
        from extensions import NamespacedRepository
        r = NamespacedRepository("r", namespace="users")
        r.add("alice", 1)
        assert r.get("alice") == 1

    def test_forwards_max_size(self):
        from extensions import NamespacedRepository
        r = NamespacedRepository("r", namespace="ns", max_size=2)
        r.add("a", 1)
        r.add("b", 2)
        with pytest.raises(RuntimeError):
            r.add("c", 3)

    def test_two_namespaces_isolated(self):
        from extensions import NamespacedRepository
        users = NamespacedRepository("u", namespace="users")
        accts = NamespacedRepository("a", namespace="accounts")
        users.add("alice", "user_data")
        accts.add("alice", "acct_data")
        assert users.get("alice") == "user_data"
        assert accts.get("alice") == "acct_data"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
