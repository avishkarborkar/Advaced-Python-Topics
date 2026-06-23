"""
Tests for the BASE TaskList.

DO NOT MODIFY THIS FILE.
Run with: pytest test_task_list.py -v

If any of these tests break after you write your subclasses, you have
modified base behavior. Revert and try again.
"""
from task_list import TaskList, Task


class TestTaskListBaseline:

    def test_new_list_is_empty(self):
        t = TaskList()
        assert t.count() == 0
        assert t.list_tasks() == []

    def test_add_returns_task(self):
        t = TaskList()
        task = t.add("Buy milk")
        assert isinstance(task, Task)
        assert task.title == "Buy milk"
        assert task.completed is False
        assert task.task_id == 1

    def test_ids_are_sequential(self):
        t = TaskList()
        a = t.add("A")
        b = t.add("B")
        c = t.add("C")
        assert a.task_id == 1
        assert b.task_id == 2
        assert c.task_id == 3

    def test_count_reflects_adds(self):
        t = TaskList()
        for i in range(5):
            t.add(f"Task {i}")
        assert t.count() == 5

    def test_get_returns_existing(self):
        t = TaskList()
        added = t.add("Find it")
        found = t.get(added.task_id)
        assert found is added

    def test_get_returns_none_for_missing(self):
        t = TaskList()
        assert t.get(999) is None

    def test_complete_marks_completed(self):
        t = TaskList()
        task = t.add("Done")
        assert t.complete(task.task_id) is True
        assert task.completed is True

    def test_complete_unknown_returns_false(self):
        t = TaskList()
        assert t.complete(999) is False

    def test_remove_deletes(self):
        t = TaskList()
        task = t.add("Gone")
        assert t.remove(task.task_id) is True
        assert t.get(task.task_id) is None
        assert t.count() == 0

    def test_remove_unknown_returns_false(self):
        t = TaskList()
        assert t.remove(999) is False

    def test_list_returns_all_in_insertion_order(self):
        t = TaskList()
        a = t.add("A")
        b = t.add("B")
        c = t.add("C")
        assert t.list_tasks() == [a, b, c]

    def test_kwargs_stored_on_extra(self):
        t = TaskList()
        task = t.add("With metadata", priority=5, deadline=1000)
        assert task.extra["priority"] == 5
        assert task.extra["deadline"] == 1000


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])