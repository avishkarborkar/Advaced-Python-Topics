"""
Task Scheduler — Starter Code

A working but rigid task scheduler. Tasks have priorities and get executed
in priority order. That's it. No dependencies, no extensibility.

Your job: refactor this into proper OOP and add task dependencies.
"""
import heapq
from datetime import datetime
from tasks import Task

class TaskScheduler:
    """
    A priority-based task scheduler.
    Lower priority number = higher priority (runs first).
    """
    
    def __init__(self):
        self._queue = []  
        self._counter = 0
        self._completed = []
        self._task_lookup = {} 

    def add_task(self, task: Task):
        """
        Add a task to the scheduler.
        name: unique string identifier
        priority: int (lower = more important)
        action: callable to execute
        """

        if task.name in self._task_lookup:
            return False
        
        self._task_lookup[task.name] = task
        heapq.heappush(self._queue, (task.priority, self._counter, task))
        self._counter += 1
        return True
    

    def execute_next(self):
        """Execute the highest priority task. Returns task name or None."""
        while self._queue:
            priority, _, task = heapq.heappop(self._queue)
            if task.status != 'pending':
                continue
            task.execute()
            self._completed.append(task)
            return task.name

        return None
    
    def execute_all(self):
        """Execute all pending tasks in priority order. Returns list of task names."""
        executed = []
        while True:
            name = self.execute_next()
            if name is None:
                break
            executed.append(name)
        return executed

    def cancel_task(self, name) -> bool:
        """Cancel a pending task. Returns True if cancelled, False if not found."""
        if name not in self._task_lookup:
            return False
        task: Task = self._task_lookup[name]
        task.cancel()
        return True

    def get_task_status(self, name):
        """Get the status of a task: 'pending', 'completed', 'cancelled', or None."""
        if name not in self._task_lookup:
            return None
        task = self._task_lookup[name]
        return task.status

    def get_pending_tasks(self):
        """Return names of all pending tasks in priority order."""

        pending = [(t.priority, t.name) for t in self._task_lookup.values()
                   if t.status == "pending"]
        pending.sort()
        return [name for _, name in pending]
