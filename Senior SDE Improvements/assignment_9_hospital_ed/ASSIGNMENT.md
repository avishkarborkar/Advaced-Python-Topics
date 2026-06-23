# Interview Tickets: Metro General — Emergency Department Expansion

## Background

This repository contains a working emergency department (ED) triage system
in the [`hospital/`](hospital/) package. It supports:

- Registering doctors
- Queuing patients in arrival order (FIFO)
- Assigning the next patient to the first available doctor
- Completing consultations and freeing doctors
- Querying waiting patients and active/completed consultations

Your task is to extend it into a **smart, specialty-aware ED system**
with bed management and multi-site coordination.

---

## The Protocol (mandatory, not optional)

1. **Read** [hospital/models.py](hospital/models.py) and [hospital/triage.py](hospital/triage.py) end-to-end. Do not skim.
2. **Fill out [DESIGN_TEMPLATE.md](DESIGN_TEMPLATE.md)** — every section — before opening any `.py` to write code.
3. **Only then** start implementing.

The design doc is the engineering. The code is just transcription.

---

## Ticket 1: Priority Triage

**Priority**: High | **Estimated Time**: 20–25 min

### Description

Real EDs do not see patients in arrival order. A CRITICAL patient who arrives
after a MINIMAL patient must be seen first.

Change `assign_next()` so that the **most critical waiting patient** is always
assigned next, regardless of arrival order. When two patients share the same
severity, the one who arrived first takes precedence (stable sort by severity then arrival time).

### Requirements

1. `Severity` is already defined with numeric values — CRITICAL=1 is most urgent.
2. The matching change must live in or be coordinated through `TriageQueue`.
3. A CRITICAL patient who joins behind three MINIMAL patients is assigned first.
4. Arrival-time tiebreaking: two MODERATE patients → earlier arrival goes first.
5. All other behaviour (doctor assignment, consultation lifecycle, queries) is unchanged.

### Key design question

> "Where does the sorting logic live — inside `assign_next`, in a helper,
> or in `add_patient`? What are the trade-offs?"

Answer this in DESIGN_TEMPLATE Section 3 before coding.

### Acceptance Criteria

- [ ] Most critical patient always assigned next
- [ ] Same-severity patients ordered by arrival time
- [ ] `get_waiting()` returns remaining patients in priority order
- [ ] No regression in `complete_consultation`, `register_doctor`, or queries

---

## Ticket 2: Doctor Specialties and Condition Matching

**Priority**: High | **Estimated Time**: 30–35 min
**Depends on**: Ticket 1

### Prompt

Generalist assignment is not sufficient for a real ED. A cardiac patient
should ideally see a cardiologist; a child should see a paediatrician.
When no specialist of the right kind is available, the system should still
gracefully fall back to whoever can help. Among equally suitable doctors,
prefer the one who has been idle the longest.

Build this. Decide the abstractions yourself.

### What to figure out (don't expect me to tell you)

- How do you represent a doctor's expertise? An enum? A string? A list of strings? Something else?
- How do you represent a patient's condition? Is it the same type as expertise, or different?
- What does "matches" mean — exact equality, subset, hierarchy?
- How do you express "any doctor will do" for a patient with no specialty need?
- How do you track "longest idle" — store a timestamp? Order? Where?

There are multiple defensible answers. Pick one. Be able to defend it.

### Acceptance Criteria *(the only contract — implementation is up to you)*

- [ ] When a specialist matching the patient's condition is available, they are preferred over a generalist
- [ ] When no specialist is available, a generalist (or any other available doctor) is assigned
- [ ] A patient with no specialty need can be seen by any doctor
- [ ] If two equally suitable doctors are available, the one who has been idle the longest is chosen
- [ ] If no doctor is available at all, `assign_next()` returns `None` (same as before)
- [ ] Priority from Ticket 1 still wins: a CRITICAL cardiac patient gets priority **and** the cardiologist (when available)

### The trap

This is the same architecture question that broke you in the interview:

> Do you subclass `TriageQueue` to add specialty matching? Modify it in place?
> Introduce a separate matcher object? Each has trade-offs.
> Make this decision **explicitly, in writing, before coding** — not mid-keystroke.

Answer it in DESIGN_TEMPLATE Section 3 and Section 6.

---

## Ticket 3: Inpatient Admission

**Priority**: Medium | **Estimated Time**: 30–35 min
**Depends on**: Ticket 2

### Prompt

Some patients can't be sent home after their consultation — they need to
stay. The hospital has different kinds of inpatient areas (ICU, general
wards, paediatric ward, cardiac unit, etc.) with limited capacity. The
system needs to admit patients to the right *kind* of inpatient location,
refuse when capacity is exhausted, and allow discharge to free space later.

A patient cannot be admitted while their consultation is still ongoing —
that's a clinical safety rule.

Build this. Decide what classes exist, what they own, and where the
admission/discharge logic lives.

### What to figure out

- Is "ward type" an attribute, an enum, a class hierarchy?
- What's the difference between a "bed" and a "ward"? Do you need both? Or can one suffice?
- Where does the admission logic live — on the existing `TriageQueue`,
  on a new `Ward`, on a new top-level coordinator? What changes about
  `TriageQueue`'s responsibility if you put it elsewhere?
- How do you handle "no ward of that type exists at all" vs "wards of
  that type exist but are full"? Are these the same error or different?
- How does discharge work? Who knows which bed a patient is in?

### Acceptance Criteria

- [ ] Admitting a patient from a completed consultation succeeds when capacity exists
- [ ] Admitting a patient from an *active* (incomplete) consultation is rejected with a clear error
- [ ] When the requested kind of inpatient capacity is exhausted, the caller gets a clear error (distinguishable from "doesn't exist")
- [ ] Discharge frees capacity so the next admission of that type can succeed
- [ ] A discharged patient cannot be discharged again

### The trap

> Does this functionality belong on `TriageQueue`? Why or why not?
> If you create a new class — what is `TriageQueue`'s responsibility now,
> and does the original module still need to exist as a separate concern?

Section 3, in writing, before coding.

---

## Ticket 4 (BONUS): Multi-Hospital Network

**Priority**: Low | **Estimated Time**: 25–30 min
**Depends on**: Ticket 3

### Prompt

Metro General is part of a network of hospitals across the city. When one
hospital is full, the network should help find another with capacity for the
patient — ideally the closest one — and support transferring the patient
there.

Build the network layer. The existing single-hospital code from Tickets 1–3
should keep working unchanged when no transfer is needed.

### What to figure out

- What does a "hospital" look like as a class? What does it own?
  Does it contain a `TriageQueue`, *be* one, or something else?
- Where does location live? What's the right coordinate system?
- What's the network's actual responsibility — finding capacity? Routing?
  Both? Is it stateful or pure-query?
- When a transfer happens, who initiates it — the source hospital, the
  network, or the caller?
- Does the patient's consultation history follow them across hospitals?

### Acceptance Criteria

- [ ] Given several hospitals at different locations, the network can find
      the *nearest* hospital with available capacity of the requested kind
- [ ] When no hospital in the network has capacity, the caller gets a clear error
- [ ] A transferred patient ends up admitted at the destination, with appropriate
      bookkeeping at both source and destination
- [ ] Single-hospital workflows from Tickets 1–3 are unaffected

### The trap

> Is `HospitalNetwork` a subclass of `Hospital`? Of `TriageQueue`?
> Or is it pure composition that holds a list of hospitals?
> Can you reuse the matching logic from earlier tickets, or do you have
> to re-implement?

---

## Evaluation Criteria

1. **You read the code before designing.** (DESIGN_TEMPLATE Section 0 proves this.)
2. **Reuse vs replace decisions are explicit and justified in writing.**
3. **You picked the abstractions yourself** — names, attributes, error semantics — and can defend them.
4. **No inheritance where composition is right.** The interview trap — same one as Ultimate TTT.
5. **Each ticket's acceptance criteria met without breaking earlier tickets.**
6. **Honest class boundaries.** No class that does two unrelated things.

---

## Notes

- You may add or modify any file. The existing code is a starting point, not a contract.
- The acceptance criteria are the only hard requirements. Everything else — names,
  enum values vs strings, where methods live, how errors are typed — is a design
  decision **you** make.
- If you find yourself writing code without having answered Section 3 of the
  design doc, **stop and go back**. Every time.
