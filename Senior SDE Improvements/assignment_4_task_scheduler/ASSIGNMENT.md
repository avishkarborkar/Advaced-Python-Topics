# Assignment 4: Task Scheduler with Dependencies

## Difficulty: ★★★★☆
## Focus: Orchestration, State Management, Graph Algorithms, Knowing What Type Each Variable Is

---

## WHY THIS ASSIGNMENT

From your Ultimate TicTacToe assessment, your weaknesses are:
1. **Orchestration** — wiring multiple components together in one class
2. **Type confusion** — mixing up tuples, objects, strings, bools
3. **Missing arguments** — forgetting to pass required parameters to methods
4. **Reading tests first** — not checking what interface the tests expect

This assignment attacks ALL of those. The scheduler is an orchestrator (like `ultimate.py` was), and you must be precise about types.

---

## STRICT RULES

### READ BEFORE YOU CODE:
1. **Read `test_scheduler.py` FIRST.** Every method signature, every argument, every return type is defined there.
2. **Know your types.** Before writing any method, write a comment: `# takes: X, returns: Y`
3. **Don't put dependency logic in `Task`.** Tasks don't know about other tasks. The scheduler manages relationships.

### File Structure:

| File | Purpose | Status |
|------|---------|--------|
| `tasks.py` | `Task` class — encapsulates a single task | **Create this** |
| `scheduler.py` | `TaskScheduler` — orchestrates tasks + dependencies | **Refactor this** |
| `test_scheduler.py` | Test suite | **DO NOT MODIFY** |

---

## PART A: `tasks.py` — The Task Class

### TYPE MAP (know these BEFORE you code)

| Attribute/Method | Type | Example |
|-----------------|------|---------|
| `task.name` | `str` | `"deploy"` |
| `task.priority` | `int` | `1` (lower = more important) |
| `task.action` | `callable` | `lambda: print("done")` |
| `task.status` | `str` | `"pending"`, `"completed"`, `"cancelled"` |
| `task.execute()` | returns nothing | raises Exception if not pending |
| `task.cancel()` | returns nothing | sets status to cancelled |
| `task < other_task` | `bool` | compares by priority |

### What Task Does:
- Stores name, priority, action, status
- Manages its own state transitions: pending -> completed, pending -> cancelled
- Refuses invalid transitions (completed -> executed again, cancelled -> executed)
- Supports `<` comparison by priority (needed for heap sorting)

### What Task Does NOT Do:
- Does NOT know about other tasks
- Does NOT know about dependencies
- Does NOT know about the scheduler

### How to make Task comparable:
```python
def __lt__(self, other):
    return self.priority < other.priority
```
This lets `heapq` sort tasks by priority automatically.

---

## PART B: `scheduler.py` — The Orchestrator

This is where your weakness shows. You need to wire together:
- A **priority queue** (heap) for execution order
- A **task lookup** (dict) for finding tasks by name
- A **dependency graph** (dict of sets) for tracking what depends on what

### TYPE MAP (know these BEFORE you code)

| Variable | Type | Example |
|----------|------|---------|
| `self._queue` | `list` (heap of tuples) | `[(1, 0, task_obj), (5, 1, task_obj)]` |
| `self._counter` | `int` | `0, 1, 2...` (tie-breaker for heap) |
| `self._task_lookup` | `dict[str, Task]` | `{"deploy": <Task>, "test": <Task>}` |
| `self._dependencies` | `dict[str, set[str]]` | `{"deploy": {"test", "build"}}` |

### METHOD SIGNATURES (match these EXACTLY)

```
add_task(task: Task) -> bool
    # Takes a Task OBJECT (not name, priority, action separately!)
    # Returns True if added, False if duplicate name

execute_next() -> str | None
    # Returns the task NAME (string), not the task object
    # Returns None if nothing to execute

execute_all() -> list[str]
    # Returns list of task NAMES (strings)

cancel_task(name: str) -> bool
    # Takes a NAME (string), not a Task object

get_task_status(name: str) -> str | None
    # Returns STATUS STRING: "pending", "completed", "cancelled", or None

get_pending_tasks() -> list[str]
    # Returns list of NAMES (strings) in priority order

add_dependency(task_name: str, depends_on_name: str) -> bool
    # Both are NAMES (strings), not Task objects
    # task_name depends on depends_on_name
    # Returns False if either doesn't exist or would create cycle

get_dependencies(task_name: str) -> list[str]
    # Returns list of dependency NAMES (strings)
```

### NOTICE THE PATTERN:
- Methods that **receive** task identity use **strings** (names)
- Only `add_task` receives an actual **Task object**
- Methods that **return** task info return **strings** (names, statuses)
- The scheduler converts between objects and strings internally

**This is where you got confused in ultimate.py** — mixing up tuples and objects. Here: strings go IN, strings come OUT. Task objects live only INSIDE the scheduler.

---

## THE ORCHESTRATION FLOW (Your Weakness)

### `add_task(task)` flow:
```
1. Is task.name already in self._task_lookup? -> return False
2. Store task in self._task_lookup[task.name] = task
3. Push to heap: heapq.heappush(self._queue, (task.priority, self._counter, task))
4. Increment self._counter
5. Initialize empty dependency set: self._dependencies[task.name] = set()
6. Return True
```

### `execute_next()` flow:
```
1. Collect blocked tasks (to re-insert later)
2. While queue is not empty:
   a. Pop from heap: (priority, counter, task)
   b. Is task.status not "pending"? -> skip (continue)
   c. Is task blocked? (any dependency still pending) -> save it, continue
   d. Task is ready! Call task.execute()
   e. Re-insert any blocked tasks we popped
   f. Return task.name
3. Re-insert any blocked tasks we popped
4. Return None
```

### `add_dependency(task_name, depends_on_name)` flow:
```
1. Either name not in self._task_lookup? -> return False
2. Would this create a cycle? -> return False
3. Add: self._dependencies[task_name].add(depends_on_name)
4. Return True
```

### Cycle Detection (DFS):
```
To check if adding task_name -> depends_on_name creates a cycle:
    Start from depends_on_name
    Can you reach task_name by following dependencies?
    If yes -> cycle exists -> return False
    If no -> safe to add
```

---

## HELPER METHOD: `_is_blocked(task_name)`

Write this helper. It checks if a task has any pending dependencies:

```
For each dependency in self._dependencies[task_name]:
    If get_task_status(dependency) == "pending":
        return True  # Still waiting
return False  # All dependencies done (completed or cancelled)
```

**A cancelled dependency UNBLOCKS the dependent task.** Only "pending" blocks.

---

## COMMON MISTAKES TO AVOID (from your previous assignments)

| Mistake | What To Do Instead |
|---------|-------------------|
| Passing task object where string expected | Check: does the method take `name: str` or `task: Task`? |
| Forgetting to pass `self` in helper calls | `self._is_blocked(task_name)` not `_is_blocked(task_name)` |
| Storing wrong type in dict | `_task_lookup[name] = task` not `_task_lookup[task] = name` |
| Missing return statement | Every method must return something explicit |
| Not re-inserting blocked tasks | If you pop a blocked task from the heap, push it back! |
| Writing cycle detection in Task | Dependencies belong in Scheduler, not Task |

---

## STEP-BY-STEP ORDER

1. **Read `test_scheduler.py`** — understand every test before writing code
2. **Write `tasks.py`** — this is straightforward, similar to Event classes
3. **Run Part A tests:** `pytest test_scheduler.py::TestTaskClass -v`
4. **Refactor `scheduler.py`** — change `add_task` to accept Task objects
5. **Run core tests:** `pytest test_scheduler.py::TestSchedulerCore -v`
6. **Add `_dependencies` dict and `_is_blocked` helper**
7. **Add `add_dependency` with cycle detection**
8. **Update `execute_next` to skip blocked tasks**
9. **Run all tests:** `pytest test_scheduler.py -v`

---

## WHAT'S DIFFERENT FROM ULTIMATE TICTACTOE

| Ultimate TicTacToe | Task Scheduler |
|-------------------|----------------|
| 3 helper files + 1 orchestrator | 1 helper file + 1 orchestrator |
| Game state (active board, players) | Task state (pending, completed, cancelled) |
| Sub-board objects passed around | Task names (strings) passed around |
| Move validation | Dependency validation + cycle detection |
| Linear flow (validate -> play -> check win) | Graph problem (dependencies form a DAG) |

**The new challenge:** graph algorithms (cycle detection via DFS). You haven't done this before. Take your time on `add_dependency`.

---

## Run Tests

```bash
cd assignment_4_task_scheduler
conda activate mpet
python -m pytest test_scheduler.py -v                         # All tests
python -m pytest test_scheduler.py::TestTaskClass -v          # Part A only
python -m pytest test_scheduler.py::TestSchedulerCore -v      # Core scheduler
python -m pytest test_scheduler.py::TestTaskDependencies -v   # Dependencies
```

---

## GOAL

By the end of this assignment you should be able to:
1. Write an orchestrator class **without pseudocode given to you**
2. Know exactly what type every variable is at every point
3. Read tests and match signatures precisely
4. Implement a graph algorithm (cycle detection) from understanding, not from copy-paste

Good luck. Read the tests first.
