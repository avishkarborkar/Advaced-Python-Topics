"""
Drill 4 — Your work goes here.

Goal: coordinate multiple wrapped overrides — the AuditedTaskList shape.

1. AuditedDatabase
     - new attribute: audit_log (list of strings)
     - override: insert, update, delete
       * call super() to do the work
       * capture the bool return
       * if True (success), append a log entry like "insert u1" or "update u1"
       * return the bool unchanged
     - find() and all_keys() are NOT overridden — read methods don't log

The Audit pattern — drill it until it's reflexive:
    def insert(self, key, record):
        ok = super().insert(key, record)
        if ok:
            self.audit_log.append(f"insert {key}")
        return ok

The Restricted pattern — pre-check, conditional super:
    def insert(self, key, record):
        if key in self.locked_keys:
            return False
        return super().insert(key, record)
"""
from database import Database


class AuditedDatabase(Database):
    def __init__(self):
        super().__init__()
        self.audit_logs = []

    def insert(self, key, record):
        value = super().insert(key, record)
        if value:
            self.audit_logs.append(f'insert {key}')
        return value

    def update(self, key, record):
        value = super().update(key, record)
        if value:
            self.audit_logs.append(f'update {key}')
        return value
    
    def delete(self, key):
        value = super().delete(key)
        if value:
            self.audit_logs.append(f'delete {key}')
        return value

    def find(self, key: str) -> dict | None:
        return self._records.get(key)

    def all_keys(self) -> list[str]:
        return list(self._records.keys())

class RestrictedDatabase(Database):

    def insert(self, key, record):
        if key in self.locked_keys:
            return False
        return super().insert(key, record)