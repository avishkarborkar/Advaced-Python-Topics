"""
Tests for YOUR subclasses.

DO NOT MODIFY THIS FILE.
Run with: pytest test_extensions.py -v

These tests are your contract. Your job is to make them pass without
modifying task_list.py or test_task_list.py.

Read every test before writing code. Each one tells you exactly what
behavior the subclass must implement and what it must NOT change from the base.
"""
import pytest


# ─────────────────────────────────────────────
# 1. PrioritizedTaskList
# ─────────────────────────────────────────────
# Goal: tasks have a priority. list_tasks() returns them sorted highest first.
# All other behavior matches the base.

class TestPrioritizedTaskList:

    def test_inherits_from_task_list(self):
        from extensions import PrioritizedTaskList
        from task_list import TaskList
        assert issubclass(PrioritizedTaskList, TaskList)

    def test_add_accepts_priority(self):
        from extensions import PrioritizedTaskList
        t = PrioritizedTaskList()
        task = t.add("Important", priority=5)
        assert task.title == "Important"
        # priority lives on extra (per base contract) OR on the task directly
        # — your call, but the test just asserts you didn't lose it
        assert task.extra.get("priority") == 5 or getattr(task, "priority", None) == 5

    def test_list_tasks_sorted_by_priority_desc(self):
        from extensions import PrioritizedTaskList
        t = PrioritizedTaskList()
        t.add("Low", priority=1)
        t.add("High", priority=10)
        t.add("Medium", priority=5)
        titles = [task.title for task in t.list_tasks()]
        assert titles == ["High", "Medium", "Low"]

    def test_default_priority_is_zero(self):
        """Tasks added without an explicit priority get priority 0."""
        from extensions import PrioritizedTaskList
        t = PrioritizedTaskList()
        t.add("With")
        t.add("Higher", priority=3)
        titles = [task.title for task in t.list_tasks()]
        assert titles == ["Higher", "With"]

    def test_complete_unchanged(self):
        """complete() should behave exactly like the base."""
        from extensions import PrioritizedTaskList
        t = PrioritizedTaskList()
        task = t.add("Anything", priority=7)
        assert t.complete(task.task_id) is True
        assert task.completed is True

    def test_remove_unchanged(self):
        from extensions import PrioritizedTaskList
        t = PrioritizedTaskList()
        task = t.add("Gone", priority=2)
        assert t.remove(task.task_id) is True
        assert t.count() == 0

    def test_count_unchanged(self):
        from extensions import PrioritizedTaskList
        t = PrioritizedTaskList()
        t.add("A", priority=1)
        t.add("B", priority=2)
        assert t.count() == 2

    def test_get_unchanged(self):
        from extensions import PrioritizedTaskList
        t = PrioritizedTaskList()
        added = t.add("X", priority=4)
        assert t.get(added.task_id) is added


# ─────────────────────────────────────────────
# 2. DeadlineTaskList
# ─────────────────────────────────────────────
# Goal: tasks can have a deadline (unix timestamp). New method overdue(now)
# returns all NOT-yet-completed tasks whose deadline < now.

class TestDeadlineTaskList:

    def test_inherits_from_task_list(self):
        from extensions import DeadlineTaskList
        from task_list import TaskList
        assert issubclass(DeadlineTaskList, TaskList)

    def test_add_accepts_deadline(self):
        from extensions import DeadlineTaskList
        t = DeadlineTaskList()
        task = t.add("Deliver", deadline=2000)
        assert task.title == "Deliver"
        assert task.extra.get("deadline") == 2000 or getattr(task, "deadline", None) == 2000

    def test_overdue_returns_past_deadlines(self):
        from extensions import DeadlineTaskList
        t = DeadlineTaskList()
        t.add("Old", deadline=500)
        t.add("Future", deadline=2000)
        overdue = t.overdue(now=1000)
        titles = [task.title for task in overdue]
        assert titles == ["Old"]

    def test_overdue_excludes_completed(self):
        """A completed task — even if its deadline has passed — is NOT overdue."""
        from extensions import DeadlineTaskList
        t = DeadlineTaskList()
        old_done = t.add("Old but done", deadline=500)
        old_pending = t.add("Old and pending", deadline=600)
        t.complete(old_done.task_id)
        overdue = t.overdue(now=1000)
        titles = [task.title for task in overdue]
        assert titles == ["Old and pending"]

    def test_overdue_excludes_no_deadline_tasks(self):
        """Tasks with no deadline are never overdue."""
        from extensions import DeadlineTaskList
        t = DeadlineTaskList()
        t.add("No deadline")  # no deadline kwarg
        t.add("Past", deadline=500)
        overdue = t.overdue(now=1000)
        assert len(overdue) == 1
        assert overdue[0].title == "Past"

    def test_list_tasks_unchanged(self):
        """list_tasks() must still return ALL tasks, not just non-overdue ones."""
        from extensions import DeadlineTaskList
        t = DeadlineTaskList()
        t.add("Old", deadline=500)
        t.add("New", deadline=2000)
        assert len(t.list_tasks()) == 2


# ─────────────────────────────────────────────
# 3. AuditedTaskList
# ─────────────────────────────────────────────
# Goal: every state-changing operation appends a log entry.
# Read operations do NOT log.

class TestAuditedTaskList:

    def test_inherits_from_task_list(self):
        from extensions import AuditedTaskList
        from task_list import TaskList
        assert issubclass(AuditedTaskList, TaskList)

    def test_audit_log_starts_empty(self):
        from extensions import AuditedTaskList
        t = AuditedTaskList()
        assert t.audit_log == []

    def test_add_logs(self):
        from extensions import AuditedTaskList
        t = AuditedTaskList()
        task = t.add("Hello")
        assert len(t.audit_log) == 1
        entry = t.audit_log[0]
        assert "add" in entry.lower()
        assert str(task.task_id) in entry

    def test_complete_logs(self):
        from extensions import AuditedTaskList
        t = AuditedTaskList()
        task = t.add("X")
        t.audit_log.clear()  # reset to isolate
        t.complete(task.task_id)
        assert len(t.audit_log) == 1
        assert "complete" in t.audit_log[0].lower()

    def test_remove_logs(self):
        from extensions import AuditedTaskList
        t = AuditedTaskList()
        task = t.add("Y")
        t.audit_log.clear()
        t.remove(task.task_id)
        assert len(t.audit_log) == 1
        assert "remove" in t.audit_log[0].lower()

    def test_get_does_not_log(self):
        from extensions import AuditedTaskList
        t = AuditedTaskList()
        task = t.add("Z")
        t.audit_log.clear()
        t.get(task.task_id)
        assert len(t.audit_log) == 0

    def test_list_tasks_does_not_log(self):
        from extensions import AuditedTaskList
        t = AuditedTaskList()
        t.add("A")
        t.add("B")
        t.audit_log.clear()
        t.list_tasks()
        t.count()
        assert len(t.audit_log) == 0

    def test_failed_complete_does_not_log(self):
        """Logging a failed mutation is a real interview judgement call.
        For this assignment: only successful mutations are logged."""
        from extensions import AuditedTaskList
        t = AuditedTaskList()
        t.complete(999)  # nothing to complete
        assert len(t.audit_log) == 0

    def test_failed_remove_does_not_log(self):
        from extensions import AuditedTaskList
        t = AuditedTaskList()
        t.remove(999)
        assert len(t.audit_log) == 0


# ─────────────────────────────────────────────
# 4. Open/Closed Sanity Check
# ─────────────────────────────────────────────
# Confirm subclasses don't accidentally break the base.
# This is the "did you respect the base?" gate.

class TestBaseStillWorks:

    def test_base_TaskList_still_works(self):
        """If your subclasses monkey-patched the base, this fails."""
        from task_list import TaskList
        t = TaskList()
        a = t.add("plain")
        assert a.task_id == 1
        assert t.count() == 1
        assert t.list_tasks() == [a]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
