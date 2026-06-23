"""
YOUR WORK GOES HERE.

You will write three subclasses of TaskList:

    1. PrioritizedTaskList — sorts list_tasks() by priority (highest first).
    2. DeadlineTaskList    — adds an overdue(now) method.
    3. AuditedTaskList     — logs every state-changing operation.

Constraints:
    - Do NOT modify task_list.py.
    - Do NOT modify test_task_list.py.
    - Both test files (test_task_list.py and test_extensions.py) must pass.
    - Each subclass should override the MINIMUM number of methods.
    - Use super() to call the base implementation wherever possible.

Read test_extensions.py BEFORE writing code. The tests are your spec.
"""
from task_list import TaskList

class PrioritizedTaskList(TaskList):
    
    def list_tasks(self):
        tasks = super().list_tasks()
        return sorted(tasks, key=lambda t: t.extra.get("priority", 0), reverse=True)


class DeadlineTaskList(TaskList):
    def overdue(self, now):
        tasks: TaskList = super().list_tasks()
        overdue_tasks = []
        for t in tasks:
            if t.extra.get('deadline') < now and not t.completed and t.extra.get("deadline") is not None:
                overdue_tasks.append(t)

        return overdue_tasks

class AuditedTaskList(TaskList):
    def __init__(self):
        super().__init__()        # ← critical: initialize base state
        self.audit_log = []        # ← test checks `t.audit_log`, not `t.logs`

    def add(self, title, **kwargs):
        task = super().add(title, **kwargs)
        self.audit_log.append(f"add #{task.task_id}")
        return task

    def complete(self, task_id):
        ok = super().complete(task_id)
        if ok:                    # only log on success — see test_failed_complete_does_not_log
            self.audit_log.append(f"complete #{task_id}")
        return ok

    def remove(self, task_id):
        ok = super().remove(task_id)
        if ok:
            self.audit_log.append(f"remove #{task_id}")
        return ok
