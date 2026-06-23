# Assignment 6: Notification Dispatch System — Design Challenge

## Difficulty: ★★★★★
## Focus: Chain of Responsibility, Decorator, Factory — Pattern Selection & Pipeline Design

---

## The Scenario

Your team runs a notification platform. It sends emails, SMS, and Slack messages. Along the way, each notification passes through rules (is this user in quiet hours? are we rate-limiting them? is this a duplicate?) and transformations (add a priority prefix, truncate long bodies, append a signature).

The current code is a 300-line `send_notification` method with every concern crammed together. Product wants Discord next sprint, compliance wants credit card redaction, and customer success wants per-organization quiet-hours rules. Right now, each one is a multi-file change.

Your job: **redesign the system so that each of those additions is a single new class.**

---

## The Two Patterns at the Heart of This Assignment

This assignment is less about rules and more about a single design question:

> **"When does a step in a pipeline *filter*, and when does it *transform*?"**

Those are two different responsibilities, and the right pattern for each is different:

### Chain of Responsibility (filtering)

Each link in the chain decides: **continue, or stop?**
If it stops, the notification never gets sent. The link may give a reason ("blocked: quiet hours"), but it doesn't change the notification itself.

**Use when** a step might *veto* the flow. Examples: quiet hours, rate limiting, deduplication, permissions.

### Decorator (transforming)

Each layer **modifies** the object and passes it along. The pipeline always produces an output.

**Use when** a step adjusts content but never blocks. Examples: prefixing, truncating, redacting, localizing.

### Why the distinction matters

If you collapse them into one abstraction, you get steps that both filter *and* transform — a classic SRP violation. Now the testing story is messy: does this step handle input X by blocking it, transforming it, or both? A new engineer can't tell without reading the body.

Keeping them separate makes the *intent* visible from the type alone. A `Middleware` can veto. A `Decorator` cannot. That's a contract, not a convention.

---

## Files You Create

| File | Responsibility | Pattern(s) |
|------|---------------|-----------|
| `notifications.py` | Data objects | (none — pure data) |
| `channels.py` | How notifications leave your system | Factory |
| `middleware.py` | What's allowed through | Chain of Responsibility |
| `decorators.py` | How content is shaped | Decorator |
| `dispatcher.py` | Wiring it together | (orchestrator — no new pattern) |

You will also be given `legacy_notifications.py` and `test_notifications.py`. Read the legacy code to understand behavior; the tests define the clean interface.

---

## The Real Design Questions

Each of these is worth thinking about *before* you write any code. In a senior interview, these are exactly the kinds of questions you'll be asked to defend.

### 1. Where does "URGENT notifications bypass quiet hours" live?

Three options:
- **In the QuietHoursMiddleware itself** — it checks priority and waves URGENT through.
- **In the dispatcher** — before running middleware, the dispatcher checks priority.
- **In a priority-aware wrapper** — a separate decision layer sitting above the chain.

Each has consequences. Which gives you the best answer to *"what if later we want URGENT to also bypass rate limiting, but not dedup?"*

### 2. Does decorator order matter?

- Does `truncate → add-prefix` produce the same output as `add-prefix → truncate`?
- If you redact credit card numbers and also truncate, which goes first? Getting it wrong leaks data.

The pipeline needs a *deliberate* order. How do you make that order visible and easy to reason about?

### 3. Is the factory's job lookup, or creation?

In Assignment 5, your `ProviderFactory` stored *instances* (already-created providers). Is that the right model here too, or should `ChannelFactory` store *classes* and instantiate on demand?

Hint: think about how channels differ from providers. Providers were stateless processors. Channels in this system hold *state* (sent-message lists). Does that change the answer?

### 4. What happens when no channel is registered for the requested type?

- Throw an exception?
- Return a failure result?
- Use a default channel (e.g., email)?

Each is legitimate. Pick one and know *why*. The test file will tell you which one the team chose — reading the test first saves you from guessing.

### 5. Should retry live in the dispatcher or the channel?

Same question as Assignment 5. Same answer (probably). But be able to articulate *why*, not just repeat it.

---

## The Open/Closed Test

The test file will verify that you can add the following **without touching any existing file**:

- A new channel (`DiscordChannel`) — register it, done.
- A new middleware (e.g., a working-hours filter for low-priority notifications) — add to the chain, done.
- A new decorator (e.g., credit card redaction) — add to the pipeline, done.

If any of these requires editing an existing file, your design is wrong. Fix it before moving on.

---

## What You Are Being Graded On (Conceptually)

Not "did your tests pass" — that's the floor. The real questions:

1. **Can you explain why middleware and decorators are different abstractions**, even though both "wrap" a notification?
2. **Can you defend the order of your middleware chain and decorator pipeline?**
3. **Can you show what happens to each file when a new requirement lands** — which files change, which don't, and why?
4. **Can you point to where each SOLID principle shows up** in your design? Especially OCP and SRP.

If you can answer those four, the code almost writes itself.

---

## Order of Work

1. **Read `legacy_notifications.py`** — trace 2-3 flows end to end
2. **Read ALL of `test_notifications.py`** — the interface is defined there, not in this document
3. `notifications.py` — 5 min, pure data
4. `channels.py` — 10 min
5. `middleware.py` — 15 min, new pattern, take your time
6. `decorators.py` — 15 min, new pattern, take your time
7. `dispatcher.py` — 15 min, smallest but ties everything together
8. Green tests

**Before writing each file**, skim its section of the test file. You lost time on Assignment 5 guessing at interfaces that were documented in the tests. Don't repeat that.

---

## Weaknesses From Assignment 5 This Targets

| Weakness | How this assignment attacks it |
|----------|-------------------------------|
| Test-first habit | Each sub-pattern has a tight test suite. One test = one method's contract. |
| Orchestration | Dispatcher chains three independent pipelines (middleware → decorators → channel). Harder flow than Assignment 5. |
| Pattern recognition under pressure | You have to *choose* between Chain of Responsibility and Decorator for each step. No spec tells you which to use. |
| Conceptual clarity | Every design decision here has a "why" question attached. Practice saying the why out loud as you go. |

---

## The One-Sentence Goal

**By the end of this assignment, you should be able to look at any pipeline-shaped problem and immediately know whether each step is a filter (middleware) or a transformer (decorator) — and why.**

That's the skill. The code is just practice.
