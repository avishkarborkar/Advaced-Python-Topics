"""
Drill 4 — base class. DO NOT MODIFY.

Database has three mutation methods (insert/update/delete) and one
read method (find). Mutations return bool — True if it worked,
False if not (e.g., update or delete on a missing key).

This is the EXACT pattern that broke you on AuditedTaskList. Drill it
here in isolation: override multiple methods, each wrapping super(),
each with side effects gated by super()'s return value.
"""


class Database:
    def __init__(self):
        self._records: dict[str, dict] = {}

    def insert(self, key: str, record: dict) -> bool:
        if key in self._records:
            return False
        self._records[key] = record
        return True

    def update(self, key: str, record: dict) -> bool:
        if key not in self._records:
            return False
        self._records[key] = record
        return True

    def delete(self, key: str) -> bool:
        if key not in self._records:
            return False
        del self._records[key]
        return True

    def find(self, key: str) -> dict | None:
        return self._records.get(key)

    def all_keys(self) -> list[str]:
        return list(self._records.keys())
