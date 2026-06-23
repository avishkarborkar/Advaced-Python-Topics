# Final Interview Prep — Subclassing & Refactoring Drill

**Time budget: 90 minutes total. 60 for Part A, 30 for Part B.**

This document gives you two interview-style scenarios. They mirror the two prompts you're most likely to face: *"extend this working code with a new feature"* and *"this method is too big — clean it up."*

---

## What the interviewer is actually testing

When an interviewer hands you working code and asks for an extension, they are watching for **three** things, in order:

1. **Did you read the existing code carefully before touching anything?** Most candidates skip this step. Read every method. Understand state. Trace one full operation end-to-end before opening a new file.

2. **Did you respect the base class?** This is where you failed Ultimate TicTacToe the first time. Modifying the base to make your feature work is the wrong answer almost every time. The base class has tests. Those tests are a contract. If you break them, you break the contract.

3. **Did you make your subclass *minimal*?** A good subclass overrides one or two methods and reuses everything else via `super()`. A bad subclass copy-pastes most of the base and mutates it. If your subclass is bigger than the base, something has gone wrong.

---

## How to start (the first 10 minutes)

Before you write any code, do this in order:

1. Open `task_list.py`. Read it top-to-bottom. Don't skim.
2. Open `test_task_list.py`. Read every test. The tests describe the *behavior contract* you must preserve.
3. Run the tests. Confirm they pass on the baseline.
4. Open `test_extensions.py`. Read those tests. Now you know exactly what your subclasses must do.
5. **Only now** open `extensions.py` and start writing.

Resist the urge to start coding immediately. The five minutes spent reading will save you twenty minutes of confused rewriting.

---

## Part A — Extend by Subclassing (60 min)

### The setup

You've inherited a working `TaskList` class used by another team. They have tests that pass. They are happy with it. **You may not modify `task_list.py` or `test_task_list.py`.** If a test in `test_task_list.py` breaks because of your work, you have failed.

### The feature request

Product wants three new variants of the task list, each for a different team:

1. **`PrioritizedTaskList`** — tasks have priority levels. When listing tasks, return them sorted by priority (highest first). When marking a task complete, behave exactly like the base.

2. **`DeadlineTaskList`** — tasks have deadlines. The list exposes a new method `overdue(now)` that returns all tasks whose deadline has passed and that are not yet complete.

3. **`AuditedTaskList`** — every state-changing operation (`add`, `complete`, `remove`) appends a record to a log. Reading operations (`list`, `get`) do not log.

The exact contracts are in `test_extensions.py`. Read them.

### Constraints

- `task_list.py` and `test_task_list.py` are **frozen**. Do not edit either file.
- Your work goes in `extensions.py`. That is the only file you write.
- Both test files must pass when you're done.

### What good looks like

- Each subclass overrides only the methods it needs to change.
- `super()` is used liberally — you should never copy a line of base-class logic into a subclass.
- Each subclass is independently testable. Don't make `AuditedTaskList` depend on `PrioritizedTaskList`, etc.
- New behavior is composable. If someone wanted `AuditedPrioritizedTaskList`, your design should make that *possible* (even if you don't write it).

### Pitfalls to avoid

- **Don't override `__init__` without calling `super().__init__()`.** You'll lose the base's state setup.
- **Don't reach into base-class private attributes** (`_tasks`, etc.) unless absolutely necessary. Use the public API. If the public API is missing something you need, that's a real interview question to raise out loud — not a license to dig into internals.
- **Don't pre-sort or pre-filter inside data-mutation methods.** Sorting belongs in retrieval, not in `add`. Mixing the two creates surprises.
- **Don't make your subclass do two things.** `PrioritizedTaskList` sorts. `AuditedTaskList` logs. Don't combine them in one class "because it's easier."

### Stretch goal (if you finish early)

Sketch (don't fully implement) a `LoggedDeadlineTaskList` that combines two of your subclasses. Talk through the trade-offs out loud: multiple inheritance? composition? a wrapper class? This is exactly the kind of question senior interviewers ask after the main task. Have an opinion ready.

---

## Part B — Break Down a Monolith (30 min)

### The setup

Open `report_generator.py`. It contains one class with one giant method that does everything: data loading, filtering, formatting, exporting, emailing. Roughly 150 lines. Tests pass against it.

### The task

Refactor it into clean, focused classes. The tests in `test_report_generator.py` must still pass — exactly. **You are not allowed to change behavior, only structure.**

### How to approach this

1. **Read the method top to bottom.** Identify each *concern* it handles. Mark them with mental boundaries: "this block loads data," "this block filters," etc.
2. **One concern, one class.** Extract each block into its own class with one focused responsibility.
3. **The original class becomes an orchestrator.** It holds the focused classes and delegates to them in order. Its `generate()` method shrinks to maybe 10 lines.
4. **Run tests after each extraction.** Don't extract all five concerns at once. Extract one, run tests, extract the next.

### What good looks like

- The original `generate()` method now reads like a recipe: "load, then filter, then format, then export, then email."
- Each extracted class is small enough that you could write a single sentence describing what it does.
- Each extracted class can be tested without instantiating any of the others (they take their dependencies as constructor arguments).

### Pitfalls to avoid

- **Don't try to identify every smell at once.** Extract the most obvious concern first. Don't get clever.
- **Don't add patterns prematurely.** If you don't see two implementations of "filtering," you don't need a Strategy interface yet. Refactor first, abstract second.
- **Don't break the public interface.** The orchestrator must still expose `generate()` with the same signature. The tests assume it.

---

## Time-boxing rules (the most important section)

**Set a literal timer.** 60 min for Part A. 30 min for Part B. When the timer ends:

- If you're not done with Part A in 45 minutes, you are over-engineering. Step back. Are you making subclasses bigger than they need to be? Are you trying to design for extensibility you don't need yet? Make the simplest thing that passes the tests.
- If a test is failing and you've spent 5+ minutes on it, **read the test again from scratch**. The bug is almost always a misread of the test, not a logic error.
- If you get stuck on Part A for more than 20 minutes on a single subclass, *skip it* and move to the next one. A partially complete answer is better than zero answers.

---

## What to do *during* the real interview

These are habits the assignment can't teach you — read them tonight, internalize them.

1. **Talk before you code.** "Before I write anything, let me read the existing code." "Before I touch the base class, let me check whether I can override `list_tasks()` instead." Articulating intent gives the interviewer chances to redirect you cheaply.

2. **State your assumptions.** "I'm assuming priority is an integer, higher is more important — does that match what you had in mind?" Wrong assumptions are forgivable. Silent assumptions are not.

3. **Ask one good question, then stop.** Not five questions. One. Make it count: "Should `overdue` include tasks completed *after* the deadline, or only currently incomplete ones?" That's one specific, scoped question that proves you read the prompt.

4. **Run tests early.** As soon as you can, run the existing tests to confirm baseline. Then run your new tests after each subclass. Don't write three subclasses then run.

5. **If you break a base test, *stop and revert*.** Don't try to patch around it. The fact that you broke a base test is a signal that your design is wrong. Re-read your own diff. The fix is almost never to modify the test.

6. **Out loud, narrate the why.** "I'm putting the sort in `list_tasks` rather than `add` because mutation methods shouldn't do read-side work." That sentence alone is worth real points — it shows you can articulate trade-offs, which is the bar for senior.

---

## What to do if you have time after both parts

- Go back to Part A and add a `__repr__` to each subclass. Small thing, but interviewers notice.
- Add type hints to your code if they're not there yet.
- Re-read your subclasses and ask: *"Could I delete five lines from this and still pass tests?"* If yes, delete them.
- Sketch the `LoggedDeadlineTaskList` stretch goal mentioned above.

---

## Final reminder

**The base class is sacred.** Subclass to extend. `super()` to reuse. Override the minimum. Run tests often. Talk while you work.

Good luck.