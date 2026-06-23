"""
TaskList — the working baseline.

DO NOT MODIFY THIS FILE during the interview drill.
This is the equivalent of the base class you're handed in the real interview.
Your subclasses must extend this without changing it.
"""


class Task:
    """A single task. Plain data + a completion flag."""

    def __init__(self, task_id: int, title: str, **kwargs):
        self.task_id = task_id
        self.title = title
        self.completed = False
        # Subclass-specific fields ride along in kwargs so the base
        # constructor stays general. This is intentional — a real interviewer
        # might give you a Task with fewer fields and ask you to extend it.
        self.extra = kwargs

    def __repr__(self):
        status = "✓" if self.completed else " "
        return f"[{status}] #{self.task_id} {self.title}"


class TaskList:
    """
    A simple in-memory task list.

    Public API:
      - add(title, **kwargs) -> Task
      - get(task_id) -> Task | None
      - complete(task_id) -> bool
      - remove(task_id) -> bool
      - list_tasks() -> list[Task]
      - count() -> int
    """

    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def add(self, title: str, **kwargs) -> Task:
        task = Task(self._next_id, title, **kwargs)
        self._tasks[task.task_id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def complete(self, task_id: int) -> bool:
        task = self._tasks.get(task_id)
        if task is None:
            return False
        task.completed = True
        return True

    def remove(self, task_id: int) -> bool:
        if task_id not in self._tasks:
            return False
        del self._tasks[task_id]
        return True

    def list_tasks(self) -> list[Task]:
        return list(self._tasks.values())

    def count(self) -> int:
        return len(self._tasks)