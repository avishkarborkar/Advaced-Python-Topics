"""
Tests for the refactored Task Scheduler.
DO NOT MODIFY THIS FILE.
"""
import pytest


# ============================================================
# PART A — Task as a Proper Class + Abstract Base
# ============================================================

class TestTaskClass:
    """Tasks should be proper objects, not dicts."""

    def test_task_base_class_exists(self):
        from tasks import Task
        assert Task is not None

    def test_task_has_name_and_priority(self):
        from tasks import Task
        task = Task(name="deploy", priority=1, action=lambda: None)
        assert task.name == "deploy"
        assert task.priority == 1

    def test_task_default_status_is_pending(self):
        from tasks import Task
        task = Task(name="deploy", priority=1, action=lambda: None)
        assert task.status == "pending"

    def test_task_execute_runs_action(self):
        from tasks import Task
        result = []
        task = Task(name="deploy", priority=1, action=lambda: result.append("done"))
        task.execute()
        assert result == ["done"]
        assert task.status == "completed"

    def test_task_cannot_execute_twice(self):
        from tasks import Task
        task = Task(name="deploy", priority=1, action=lambda: None)
        task.execute()
        with pytest.raises(Exception):
            task.execute()

    def test_task_cancel(self):
        from tasks import Task
        task = Task(name="deploy", priority=1, action=lambda: None)
        task.cancel()
        assert task.status == "cancelled"

    def test_cancelled_task_cannot_execute(self):
        from tasks import Task
        task = Task(name="deploy", priority=1, action=lambda: None)
        task.cancel()
        with pytest.raises(Exception):
            task.execute()

    def test_task_comparison_by_priority(self):
        """Tasks should be comparable by priority for heap operations."""
        from tasks import Task
        t1 = Task(name="low", priority=10, action=lambda: None)
        t2 = Task(name="high", priority=1, action=lambda: None)
        assert t2 < t1


class TestSchedulerCore:
    """Core scheduler functionality with Task objects."""

    def test_add_and_execute(self):
        from scheduler import TaskScheduler
        from tasks import Task
        result = []
        scheduler = TaskScheduler()
        scheduler.add_task(Task("a", 1, lambda: result.append("a")))
        scheduler.execute_next()
        assert result == ["a"]

    def test_priority_order(self):
        from scheduler import TaskScheduler
        from tasks import Task
        result = []
        scheduler = TaskScheduler()
        scheduler.add_task(Task("low", 10, lambda: result.append("low")))
        scheduler.add_task(Task("high", 1, lambda: result.append("high")))
        scheduler.add_task(Task("mid", 5, lambda: result.append("mid")))
        scheduler.execute_all()
        assert result == ["high", "mid", "low"]

    def test_no_duplicate_task_names(self):
        from scheduler import TaskScheduler
        from tasks import Task
        scheduler = TaskScheduler()
        assert scheduler.add_task(Task("a", 1, lambda: None)) is True
        assert scheduler.add_task(Task("a", 2, lambda: None)) is False

    def test_cancel_task(self):
        from scheduler import TaskScheduler
        from tasks import Task
        scheduler = TaskScheduler()
        scheduler.add_task(Task("a", 1, lambda: None))
        assert scheduler.cancel_task("a") is True
        assert scheduler.get_task_status("a") == "cancelled"

    def test_execute_skips_cancelled(self):
        from scheduler import TaskScheduler
        from tasks import Task
        result = []
        scheduler = TaskScheduler()
        scheduler.add_task(Task("a", 1, lambda: result.append("a")))
        scheduler.add_task(Task("b", 2, lambda: result.append("b")))
        scheduler.cancel_task("a")
        scheduler.execute_all()
        assert result == ["b"]

    def test_get_pending_tasks(self):
        from scheduler import TaskScheduler
        from tasks import Task
        scheduler = TaskScheduler()
        scheduler.add_task(Task("c", 3, lambda: None))
        scheduler.add_task(Task("a", 1, lambda: None))
        scheduler.add_task(Task("b", 2, lambda: None))
        assert scheduler.get_pending_tasks() == ["a", "b", "c"]

    def test_execute_next_returns_none_when_empty(self):
        from scheduler import TaskScheduler
        scheduler = TaskScheduler()
        assert scheduler.execute_next() is None


# ============================================================
# PART B — Task Dependencies
# ============================================================

class TestTaskDependencies:
    """Tasks can depend on other tasks — B won't run until A completes."""

    def test_add_dependency(self):
        from scheduler import TaskScheduler
        from tasks import Task
        scheduler = TaskScheduler()
        scheduler.add_task(Task("a", 1, lambda: None))
        scheduler.add_task(Task("b", 1, lambda: None))
        result = scheduler.add_dependency("b", "a")  # b depends on a
        assert result is True

    def test_dependency_on_nonexistent_task_fails(self):
        from scheduler import TaskScheduler
        from tasks import Task
        scheduler = TaskScheduler()
        scheduler.add_task(Task("a", 1, lambda: None))
        result = scheduler.add_dependency("a", "nonexistent")
        assert result is False

    def test_dependent_task_waits(self):
        """B depends on A. Even though B has higher priority, A runs first."""
        from scheduler import TaskScheduler
        from tasks import Task
        result = []
        scheduler = TaskScheduler()
        scheduler.add_task(Task("a", 10, lambda: result.append("a")))  # Low priority
        scheduler.add_task(Task("b", 1, lambda: result.append("b")))   # High priority
        scheduler.add_dependency("b", "a")  # b depends on a
        scheduler.execute_all()
        assert result == ["a", "b"]

    def test_multiple_dependencies(self):
        """C depends on both A and B. C runs after both are done."""
        from scheduler import TaskScheduler
        from tasks import Task
        result = []
        scheduler = TaskScheduler()
        scheduler.add_task(Task("a", 2, lambda: result.append("a")))
        scheduler.add_task(Task("b", 1, lambda: result.append("b")))
        scheduler.add_task(Task("c", 0, lambda: result.append("c")))  # Highest priority
        scheduler.add_dependency("c", "a")
        scheduler.add_dependency("c", "b")
        scheduler.execute_all()
        # c has highest priority but depends on a and b
        assert result.index("a") < result.index("c")
        assert result.index("b") < result.index("c")

    def test_chain_dependencies(self):
        """A → B → C (C depends on B, B depends on A)."""
        from scheduler import TaskScheduler
        from tasks import Task
        result = []
        scheduler = TaskScheduler()
        scheduler.add_task(Task("a", 3, lambda: result.append("a")))
        scheduler.add_task(Task("b", 2, lambda: result.append("b")))
        scheduler.add_task(Task("c", 1, lambda: result.append("c")))
        scheduler.add_dependency("b", "a")
        scheduler.add_dependency("c", "b")
        scheduler.execute_all()
        assert result == ["a", "b", "c"]

    def test_circular_dependency_detected(self):
        """Adding a circular dependency should fail."""
        from scheduler import TaskScheduler
        from tasks import Task
        scheduler = TaskScheduler()
        scheduler.add_task(Task("a", 1, lambda: None))
        scheduler.add_task(Task("b", 1, lambda: None))
        scheduler.add_dependency("b", "a")
        result = scheduler.add_dependency("a", "b")  # Would create cycle
        assert result is False

    def test_circular_dependency_chain(self):
        """A→B→C→A should be detected as circular."""
        from scheduler import TaskScheduler
        from tasks import Task
        scheduler = TaskScheduler()
        scheduler.add_task(Task("a", 1, lambda: None))
        scheduler.add_task(Task("b", 1, lambda: None))
        scheduler.add_task(Task("c", 1, lambda: None))
        scheduler.add_dependency("b", "a")
        scheduler.add_dependency("c", "b")
        result = scheduler.add_dependency("a", "c")  # Creates A→B→C→A
        assert result is False

    def test_cancelled_dependency_unblocks(self):
        """If A is cancelled, B (which depends on A) should become executable."""
        from scheduler import TaskScheduler
        from tasks import Task
        result = []
        scheduler = TaskScheduler()
        scheduler.add_task(Task("a", 1, lambda: result.append("a")))
        scheduler.add_task(Task("b", 2, lambda: result.append("b")))
        scheduler.add_dependency("b", "a")
        scheduler.cancel_task("a")
        scheduler.execute_all()
        assert result == ["b"]

    def test_independent_tasks_unaffected(self):
        """Tasks without dependencies should execute normally by priority."""
        from scheduler import TaskScheduler
        from tasks import Task
        result = []
        scheduler = TaskScheduler()
        scheduler.add_task(Task("a", 2, lambda: result.append("a")))
        scheduler.add_task(Task("b", 1, lambda: result.append("b")))
        scheduler.add_task(Task("c", 3, lambda: result.append("c")))
        # No dependencies
        scheduler.execute_all()
        assert result == ["b", "a", "c"]

    def test_get_dependencies(self):
        """Should be able to query a task's dependencies."""
        from scheduler import TaskScheduler
        from tasks import Task
        scheduler = TaskScheduler()
        scheduler.add_task(Task("a", 1, lambda: None))
        scheduler.add_task(Task("b", 1, lambda: None))
        scheduler.add_task(Task("c", 1, lambda: None))
        scheduler.add_dependency("c", "a")
        scheduler.add_dependency("c", "b")
        deps = scheduler.get_dependencies("c")
        assert set(deps) == {"a", "b"}

    def test_get_dependencies_empty(self):
        from scheduler import TaskScheduler
        from tasks import Task
        scheduler = TaskScheduler()
        scheduler.add_task(Task("a", 1, lambda: None))
        deps = scheduler.get_dependencies("a")
        assert deps == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
