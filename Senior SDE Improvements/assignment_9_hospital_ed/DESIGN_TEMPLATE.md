# Design Document — Fill This Out BEFORE Writing Any Code

If you cannot fill a section, you are not ready to code that ticket yet.

---

## Section 0: What does the existing code do?

Read [hospital/models.py](hospital/models.py) and [hospital/triage.py](hospital/triage.py).
Then close the files and write this from memory. If you have to re-open them to fill this in,
that means you read too fast — read again, slowly.

In 5–8 bullet points, describe:
- What classes exist? What does each own?
- What is the assignment strategy in `assign_next()`?
- What happens when a consultation is completed?
- What can you NOT do with the current system?

*(Write here — do not skip to Section 1 until this is done)*

-

---

## Section 1: Reuse vs Replace

For each existing class, decide before writing a single line:

| Class           | Reuse / Modify / Replace | Why                                      |
|-----------------|--------------------------|------------------------------------------|
| `Patient`       |                          |                                          |
| `Doctor`        |                          |                                          |
| `Consultation`  |                          |                                          |
| `TriageQueue`   |                          |                                          |

**Force yourself to write a "Why" for every row.** Blank = not ready to code.

---

## Section 2: New Nouns (per ticket)

What new classes, enums, or types are you introducing for each ticket?

### Ticket 1
| New thing | Kind | Data it owns | Why it must exist |
|-----------|------|--------------|-------------------|
|           |      |              |                   |

### Ticket 2
| New thing | Kind | Data it owns | Why it must exist |
|-----------|------|--------------|-------------------|
|           |      |              |                   |

### Ticket 3
| New thing | Kind | Data it owns | Why it must exist |
|-----------|------|--------------|-------------------|
|           |      |              |                   |

---

## Section 3: Ownership Decisions (answer ALL before coding)

**Ticket 1:**

1. Where does the priority-sort logic live: inside `assign_next`, in `add_patient`,
   in a private helper, or somewhere else? What are the trade-offs of each?

2. Does `get_waiting()` return patients in priority order or arrival order?
   Who is responsible for that ordering?

**Ticket 2:**

3. Do you subclass `TriageQueue` to change matching behaviour, or do you modify it?
   If subclassing: can every existing caller use the new subclass without knowing about specialties?
   If modifying: what is the risk?

4. How does `assign_next` decide between two available doctors for a given patient?
   Write the decision logic in plain English (not code).

5. "Longest-idle doctor" — what does `Doctor` need to track to make this possible?
   Where does that state live?

**Ticket 3:**

6. Does `admit_patient` live on `TriageQueue`, or on a new class?
   If a new class: what does `TriageQueue` need to expose to it?

7. Who owns the list of wards? `TriageQueue`, a `HospitalManager`, or somewhere else?
   Can a ward exist without a triage queue?

8. Where does the safety check "refuse to admit from active consultation" live?
   On `admit_patient`, on `Consultation`, or on `Ward`?

---

## Section 4: Walk-Through (do this for every ticket before coding it)

### Ticket 1 walk-through

Scenario:
> Dr. Lee registers. Three patients arrive in order:
> Eve (MINIMAL), Frank (CRITICAL), Grace (HIGH).
> `assign_next()` is called three times.

Narrate each call — who is assigned, in what order, and why:

Call 1:
Call 2:
Call 3:

### Ticket 2 walk-through

Scenario:
> Dr. Patel (CARDIOLOGY) and Dr. Kim (GENERAL) are available.
> Henry (CRITICAL, CARDIOLOGY) and Iris (MODERATE, NEUROLOGY) are waiting.
> `assign_next()` is called twice.

Call 1 (who gets assigned to whom, and why?):
Call 2:

### Ticket 3 walk-through

Scenario:
> A CARDIAC ward has 2 beds. Both are occupied.
> James finishes his consultation; doctor recommends CARDIAC admission.
> `admit_patient(james_consultation, WardType.CARDIAC)` is called.

What happens? (trace the error path):

---

## Section 5: Edge Cases (at least 4, before coding)

1.
2.
3.
4.
5.

---

## Section 6: The Trap Question

From Ticket 2:
> "Do you subclass `TriageQueue` or modify it?"

This is the same question as Ultimate TicTacToe: "Does `UltimateTicTacToe` extend `TicTacToeGame`?"

Write your answer here **and justify it**. One paragraph. Reference LSP if relevant.

*(The point is not to get the "right" answer — it's to make the decision explicitly
rather than implicitly, mid-coding.)*

---

## Section 7: Post-Coding Reflection *(fill in after finishing)*

- Did the code match your design? Where did it diverge?
- Which bugs did the walk-through catch before you coded them?
- What would you do differently in the design phase next time?
