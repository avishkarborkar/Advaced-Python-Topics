# Improvements Over Assignments

---

## Assignment 1: TicTacToe (Starting Point)
- Single class design, no patterns
- Basic OOP with encapsulation (private methods)
- Hard-coded logic, print statements for feedback
- Functional but not extensible
- **Independence: ~20%** — needed step-by-step guidance for everything

---

## Assignment 3: Library & Parking Lot (First Leap)
- Introduced **Strategy Pattern** for swappable behaviors (late fees, pricing)
- Used **abstract base classes** to enforce contracts
- Split code into multiple files with clear separation of concerns
- Applied encapsulation with properties and private attributes
- Began thinking about extensibility and open/closed principle
- **Independence: ~60%** — understood structure, needed help with edge cases

**What improved:** Went from one file to multiple files. Started thinking about "who owns this responsibility?"

---

## Assignment 4: Stock Market (Pattern Confidence)
- Implemented **Observer Pattern** with an Event Bus (pub/sub architecture)
- Designed a full event-driven system across 5 modules (events, observers, event_bus, stocks, stock_market)
- Used polymorphism to handle multiple event types and observer behaviors independently
- Achieved loose coupling: Stock doesn't know about observers, observers don't know about Stock
- Demonstrated that new observer types can be added without modifying existing code
- **Independence: ~70%** — understood concepts quickly, logic errors were the main issue

**What improved:** Asking better questions ("do I store old_volume or pass threshold?"). Self-correcting typos. Moving from needing all answers to needing only hints.

**Remaining issues:** Typos in parameter names (`time_stamp` vs `timestamp`, `>` vs `>=`), accessing wrong event attributes, logic inversions.

---

## Assignment 2: Ultimate TicTacToe (The Real Test)

This was an interview redemption — previously failed by modifying the base class instead of subclassing.

### board_manager.py — Strongest File
- Pure composition: 9 TicTacToe instances in a tuple-keyed dictionary
- Reused base class methods (`get_cell`, `.winner`, `_is_board_full`) instead of rewriting
- Clean API with focused methods
- Nearly independent on first attempt
- **Independence: ~90%**

### rules.py — Clean Structure
- Stateless validator with no stored game state
- Correct use of SubBoardManager API
- Logic needed clarification (inverted conditions, wrong return values)
- Got the final order right: decided check -> free choice -> match check
- **Independence: ~75%**

### ultimate.py — Orchestration Struggle
- Correct inheritance and composition setup
- Understood the concept of overriding `make_move`
- Struggled with: what `active_sub_board` is (tuple vs object), double references (`self.sub_board_manager.sub_board_manager`), missing arguments to method calls
- Needed pseudocode flow before writing implementation
- Forgot query methods and player sync — had to be reminded
- **Independence: ~40%**

**What improved from stock market:**
- `board_manager.py` was nearly perfect on first try (vs stock market where every file needed fixes)
- Understood composition vs inheritance clearly
- Asked architectural questions instead of just "what do I write?"
- Base class left untouched (the exact mistake from the interview, now corrected)

**What still needs work:**
- Orchestration: wiring multiple components in one class
- Type awareness: knowing if a variable is a tuple, object, or string at each point
- Completeness: remembering all required methods before running tests

---

## Progression Summary

| Skill | Assignment 1 | Assignment 3 | Assignment 4 (Stock) | Assignment 2 (Ultimate) |
|-------|-------------|-------------|---------------------|------------------------|
| **OOP** | Basic | ABC + inheritance | Full hierarchy | Inheritance + composition |
| **Patterns** | None | Strategy | Observer + Event Bus | Composition + delegation |
| **File separation** | 1 file | Multiple | 5 modules | 4 files with clear roles |
| **Reuse vs rewrite** | All custom | Some reuse | Good reuse | Excellent (zero new win logic) |
| **Independence** | ~20% | ~60% | ~70% | 40-90% (varies by file) |
| **Design questions** | None | Few | Good | Excellent |

---

## Key Growth Trajectory
1. **Pattern recognition**: None -> Strategy -> Observer -> Composition + Inheritance combined
2. **Abstraction**: Hard-coded -> Interfaces -> Event-driven -> Stateless validators
3. **Design thinking**: "How do I make it work?" -> "Where does this responsibility belong?"
4. **Separation of concerns**: One class -> Multiple files -> Each file has one clear job
5. **Reuse mindset**: Copy-paste -> Inheritance -> `super().make_move()` delegation

---

## Identified Weaknesses (Next Focus Areas)

### 1. Orchestration (Critical)
The class that ties everything together is consistently the weakest. Need to practice writing the "wiring" class independently without pseudocode.

### 2. Type Precision
Mixing up what a variable actually is — tuple vs object, string vs bool, method vs attribute. Need to mentally track types through the entire flow.

### 3. Argument Completeness
Forgetting to pass required parameters to methods. Need to check method signatures before calling them.

### 4. Test-First Thinking
Not reading tests before coding. Tests define the contract — they tell you exact parameter names, return types, and expected behavior.

### 5. Syntax Precision
Small typos that cause test failures: `time_stamp` vs `timestamp`, `inner_row` written twice, `>` vs `>=`. Slow down and proofread.

---

## Next Assignment: Task Scheduler
Designed to directly target weaknesses #1-4. Focus areas:
- Write the orchestrator (`scheduler.py`) without pseudocode
- Track types precisely (strings vs Task objects)
- Read tests first, match signatures exactly
- Implement cycle detection (new: graph algorithms)

---

## Assignment 5: Payment Processing System (Multi-Pattern Integration)

Refactoring ~400 lines of legacy code into 6 files using **Factory, Adapter, and Observer** patterns simultaneously. First assignment combining three patterns in one system.

### payments.py — Data Layer
- Enums (`PaymentMethod`, `PaymentStatus`) + dataclasses (`PaymentRequest`, `PaymentResult`)
- Cleanest file — passed tests on first run after removing debug scratch code
- **Independence: ~95%**

### validators.py — Factory Pattern
- `PaymentValidator` ABC with three concrete validators (credit card, bank transfer, wallet)
- `ValidatorFactory` using a **class-as-value dict** — `{PaymentMethod.CREDIT_CARD: CreditCardValidator}`
- First time recognizing classes as first-class objects that can be stored and called later
- **Independence: ~80%** — needed nudges on `@abstractmethod` and `self`

### providers.py — Registration-Based Factory
- `PaymentProvider` ABC with `name` as abstract property
- `ProviderFactory` using `register()` + first-match-via-`supports()` iteration
- Correctly understood why registration beats if/elif for OCP
- **Independence: ~75%** — confused `self.provider` vs `self.name`, initial list `[PaymentProvider]` instead of `[]`

### adapters.py — The Hard Part
- `LegacyLedgerAdapter(PaymentProvider)` using composition (not inheritance — corrected mid-task)
- Translated four interface mismatches: float dollars → int cents, `PaymentRequest` → flat params, `PaymentMethod` → `"DEBIT"` string, callback → return value
- Callback-catching pattern (local `result_holder` dict captured by closure) was genuinely new territory
- **Independence: ~50%** — needed explicit hints on composition vs inheritance and the callback trick

### receipts.py — Observer Pattern
- `TransactionObserver` ABC; `ReceiptGenerator` filters on `SUCCESS`, `TransactionLogger` logs all
- Cleanest pattern of the three — mapped directly to the `on_transaction(request, result)` contract
- **Independence: ~85%** — typo-heavy (`RecieptGenerator`, `[{}]` vs `[]`)

### processing.py — Orchestrator
- DI via `__init__(provider_factory, validator_factory)` — no hardcoded dependencies
- Retry loop, early returns for validation/no-provider, single observer notification at end
- Requested code completion for this file (knew the logic, wanted to save time)
- **Independence: deferred** — own assessment: ~70%

### What improved from prior assignments
- **Pushed back on scope**: interviewer said Factory/Observer/Adapter only → asked to re-scope the assignment spec instead of silently following the ABC-singleton design. Senior-level move.
- **Pattern recognition before coding**: pre-coding comments in legacy file correctly identified factory, observer, and dataclass opportunities.
- **Asked "why", not just "how"**: paused to ask what `ValidatorFactory`'s role actually was instead of copying the shape.
- **Composition clicked**: adapter pivot from inheritance to composition was a one-hint fix.

### What still needs work
- **Test-first habit still missing**: kept asking where `request` came from when the test file had the answer. Weakness #4 from prior list — not yet resolved.
- **Iteration cadence**: wrote multiple classes before running tests. Each test run surfaced a cluster of bugs (missing `self`, `{` vs `(`, typos). Shorter write-test-fix cycles would've cut debugging time.
- **Python fluency gaps**: reached for `__getattribute__`, `is not "string"`, `datetime` vs `datetime.datetime` — all symptoms of unfamiliar syntax. When unsure, simpler forms.
- **Cargo-cult initializers**: `self.supported_providers = [PaymentProvider]` — initialized a list with the ABC class itself as a placeholder for "this holds providers." Declare the container, then ask what goes in it.

### Self-assessed scores
- Pattern understanding: **8/10** — genuinely grasped the *why* of each pattern
- Python fluency: **6/10** — correct intent, wrong syntax on details
- Testing discipline: **5/10** — still writing in large chunks between test runs

### Key takeaway
First assignment where architectural reasoning outpaced execution. Pattern choices were right on the first pass; bugs lived in mechanics (self, tuples vs sets, typos, duplicate calls). The gap to close now is mechanical, not conceptual — drill the write-test-fix loop at smaller granularity.

---

## Assignment 6: Notification Dispatch System (Two New Patterns)

Refactoring legacy notification code into 5 files using **Chain of Responsibility, Decorator, and Factory** patterns. First time integrating two brand-new patterns simultaneously alongside one reinforced.

### notifications.py — Data Layer
- Enums (`Priority`, `Channel`) + `Notification` + `DeliveryResult`
- Initial typos: class named `Notifications` (plural) instead of `Notification`, and `str` leaked in as a parameter name (`def __init__(self, user_id, str, channel: ...)`)
- Did not use `@dataclass` despite the precedent from A5 — manual `__init__` reintroduced the kind of boilerplate dataclasses exist to eliminate
- **Independence: ~80%** — corrections were small, but they were the same shape as A5's typos

### channels.py — Factory (Reinforced)
- **Major conceptual error early**: modeled `NotificationChannel` as something that *holds* a notification (passed via `__init__`) rather than a stateless *sender* (passed via `send()`). Took a redirect to recognize "the email server doesn't hold one email."
- Also shadowed the `Channel` enum by naming the ABC `Channel` — required renaming to `NotificationChannel`
- Misread `_make_notification` (a test helper at module level in `test_notifications.py`) as part of the `NotificationChannel` contract and added it as an abstract method. Useful learning moment about distinguishing test fixtures from spec.
- `ChannelFactory` clicked immediately once the test was decoded — `f.register(Channel.EMAIL, email)` made the dict-storage pattern obvious, transferred cleanly from A5's `ProviderFactory`
- **Independence: ~55%** — conceptual model needed correction, then mechanics fell into place

### middleware.py — Chain of Responsibility (NEW pattern)
- `QuietHoursMiddleware`: had the **wrap-around time bug** (10pm → 7am window). Initial check `hour >= 22 and hour <= 7` produced the wrong allow/block on every input. Asked for a logic fix rather than working through it. Classic time-window bug worth seeing once.
- `DedupMiddleware`: first attempt stored full notification history and compared positions `[0]` and `[1]` regardless of length — broken model. Also missed the per-`(user_id, subject)` keying. Asked for a logic fix.
- `RateLimitMiddleware`: did not attempt — used the hint structure directly.
- `MiddlewareChain`: **strongest part of the file**. Initial attempt inherited from `NotificationMiddleware` (subtle category error) and returned on the first iteration regardless of the result, but the recovery was clean — understood "return early on block, allow if all pass" immediately when prompted.
- **Independence: ~35%** — significant chunks of logic were delegated. The pattern (chain iteration) was understood; the per-middleware state-tracking logic was not written independently.

### decorators.py — Decorator Pattern (NEW pattern)
- All four classes (`PriorityPrefixDecorator`, `TruncateDecorator`, `SignatureDecorator`, `DecoratorPipeline`) were delegated rather than attempted. Skeleton had `apply(self)` with no parameter and `pass` bodies; said "I already know it, please write the logic so I don't waste time."
- The conceptual pattern was understood (immutable transformation, return new `Notification`), but the mechanical practice of *implementing* the immutable-copy idiom in Python (rebuilding via `Notification(...)` constructor) wasn't drilled.
- **Independence: ~15%** — the pattern reasoning was internalized; the code was not written.

### dispatcher.py — Orchestrator
- Initial skeleton had a circular self-import (`from dispatcher import NotificationDispatcher` *inside* `dispatcher.py`), missing `max_retries` default, and a `return` inside the retry loop that exited on first failure
- Treated `middleware_chain.run()` as returning a bool when it returns a tuple — same conceptual gap as A5 ("what does this return?"). Worth flagging as a recurring pattern.
- Asked for the full fix rather than iterating
- **Independence: ~30%**

### What improved from Assignment 5
- **Test-as-spec habit started**: read the dispatcher test before writing `dispatch()`, used `_make_notification` test helper as documentation. Direction is right even when execution stumbles.
- **Pattern transfer works**: `ChannelFactory` was effectively a copy of `ProviderFactory` thinking — registration, dict storage, `.get()` for the None case. Recognized the equivalence without prompting.
- **Cleaner Python**: no `__getattribute__` reaches, no `is not "string"` mistakes. Type hints are present (even when wrong, like `list[Notification]` annotated as `Notification`).

### What got worse
- **Outsourced logic to me four separate times** ("I know this, please fix it for me, I don't want to waste time"). Across both new patterns and the orchestrator. The intent — protect time — is reasonable, but the *consequence* is that the actual implementation muscle for Chain of Responsibility and Decorator wasn't built. Knowing the pattern is not the same as having written it.
- **Test-helper vs contract confusion**: misread `_make_notification` as part of the channel ABC. Distinguishing "things in the test file because they're convenient" from "things in the test file because they're required" is a senior skill that needs sharpening.
- **Same "what does this return" gap as A5**: tried `if status:` on a tuple-returning method. The fix is to look at the method definition before using its return value, every time, until it becomes automatic.
- **Iteration cadence still too coarse**: tests were run in batches that surfaced multiple unrelated failures at once (`send` outside class body, duplicated `self.sent.append({self.sent.append(...)})`, inverted SMS condition). One-class-then-test would've caught each in isolation.

### Self-assessed scores
- Pattern understanding: **8/10** — Chain of Responsibility vs Decorator distinction is internalized; can articulate the filter-vs-transform difference cleanly
- Python fluency: **5/10** — slight regression. Multiple "fix this for me" requests indicate the hands-on syntax practice is being skipped, which was the whole point of doing the assignment
- Testing discipline: **5/10** — no improvement. Still writing multi-class chunks before testing
- **Implementation independence: 4/10** — the lowest score across all assignments. Roughly half the production code in `middleware.py`, `decorators.py`, and `dispatcher.py` was written by Claude on direct request

### Honest takeaway
Two opposing trends. **Conceptually**, the trajectory is still up — the pattern-recognition skill that powered A5 is intact and even sharper. The Chain-of-Responsibility-vs-Decorator distinction (filter vs transform, returns bool vs returns object) was articulated correctly without prompting.

**Mechanically**, this assignment regressed. "I already know this, please write it" used four separate times means four separate opportunities to build hands-on muscle were skipped. Knowing a pattern in the abstract is interview-passable; *writing* it under pressure is what an interview actually tests. The dictate-and-delegate mode that worked for A5's polish phase becomes a problem when applied to the first attempt at a new pattern.

For the next assignment: **rule of thumb — never outsource a pattern you haven't yet implemented yourself end-to-end at least once**. Reinforcement cycles (third or fourth time using Factory, etc.) are fine to compress. First-time Chain of Responsibility and first-time Decorator should have been hand-written all the way through, even if slow.

---

## 2026-04-28 — 3 Month Evaluation Interview (Ultimate TicTacToe Redux)

**Format:** 75-minute live coding evaluation with two senior engineers (Nishith + Sharath). Same Ultimate TicTacToe problem from the original interview that triggered this whole improvement track. Goal: redo it cleanly, demonstrate growth.

**Outcome:** Did not finish Ticket 1 within the time window. Sharath had to leave 20 minutes early. Code shipped was structurally sound but incomplete (no `make_move` override, no `get_valid_actions` override, no active-board logic). The interview was a mixed performance — strong on principles and reasoning, weaker on time management and conviction under questioning.

### What landed well

- **Refused to modify the base class.** When the ticket itself said *"modify TicTacToeGame class in game.py"*, pushed back on Open-Closed grounds. Quote: *"I would not want to modify base class over here... it violates the open close principle and also the single responsibility principle."* That is a senior-level move — most candidates obey the ticket literally.

- **Defined OCP and SRP under direct questioning.** Sharath asked for a definition mid-flow. Delivered: *"open to extend but closed for addition meaning adding a different functionality."* Wording was a bit off (should be "modification," not "addition") but the concept was right. Sharath corrected and reframed it as *"if there's another person who is using the tic tac toe class and suddenly the reset function is changed because somebody changed their base class they're screwed"* — accepted the reframe cleanly.

- **Proposed `BoardManager` (composition).** Recognized that board-state tracking was a separate concern from `UltimateTicTacToe` itself. Sharath actively endorsed this: *"that's actually good design... this class would be like the orchestrator which just calls everything."* This contradicts the earlier self-report that the suggestion was "asked to ignore" — the transcript shows the interviewer agreed.

- **Arrived at the numpy reuse insight under pressure.** When the interviewers asked if there was a better data structure than a dict for `big_board_winners`, worked through the trade-offs out loud and landed on: *if `self.big_board_winners` is a numpy array, the existing `check_winner` logic copy-pastes onto the meta-board.* That is the elegant solution. It came out during the session, not before — which is harder.

- **Reused base `check_winner` per sub-board.** Quote: *"by inheriting I mean we could just call check winner on every support."* Correct instinct: the base class is a tool, called as `sub.check_winner()`, not reimplemented.

### What hurt the score

- **The `super()` blunder.** When asked *"why would you want to super, isn't the init of UltimateTicTacToe different from the init of what you're looking for"*, the answer was: *"when I wrote super, I did not actually see what was in that. It's just like I haven't made my decisions yet."* That is the worst possible answer. It tells the interviewer the line of code was written without thinking. **Fix forward:** before writing any line in an `__init__`, look at the parent's `__init__` for 5 seconds. Decide explicitly: inherit it, partially inherit it, or replace it.

- **Wavered on inheritance under critique.** When Sharath asked *"is there any need for you to inherit from TicTacToeGame?"*, the answer was: *"I see that we don't actually need it and ultimate can be a class of its own."* That conceded the design without defending it. The right counter — *"I'm reusing `sub.check_winner()` per sub-board and the same logic on the meta-board via the numpy trick; the inheritance is load-bearing"* — was available but never said. Conceding to interviewer pressure when you actually have a defensible answer is a costly habit.

- **Time spent on environment setup and import discussions.** ~5 minutes lost on `source activate` vs `conda activate`, then more time on Python import semantics (`from game import` vs `from .game import`, `__init__.py` and `__all__`). These weren't part of the test. Should have been dispatched in 30 seconds with *"let me move on, I'll fix imports if it actually breaks."*

- **Closing self-reflection undersold.** Quote: *"I don't know I was expecting that... I have done this before but I remember that I took a completely different approach... when I practiced and now... if I did it back then it should have just gone with that."* This signal — "I did better when I had practiced this exact problem" — is anti-marketing. The right closer was: *"This implementation went a direction I hadn't tried before — using numpy arrays at the meta-level to reuse `check_winner`. I think it's actually cleaner than my previous approach, even though I had less time to finish it."* Same honesty, framed forward.

- **Did not finish Ticket 1.** No `make_move` override, no `get_valid_actions` override, no active-board enforcement logic, no `render`. The shipping code was a `check_winner` infrastructure with `winner_big_board` and `winner_ultimate` helpers — but the actual game cannot be played end-to-end with this code. Time pressure was real (Sharath leaving early) but the import/setup detours cost the budget needed to finish.

- **Typo bug shipped.** `self.big_board_winner` (singular) declared in `__init__`, `self.big_board_winners` (plural) referenced in `winner_big_board()`. Would crash on first call. Tests would have caught it in 30 seconds. Were not run.

### Honest score

| Dimension | Score |
|-----------|-------|
| Architectural reasoning | **8/10** — held principles, recognized modular boundaries, arrived at the elegant solution |
| Communication of design | **6/10** — articulated OCP/SRP, but caved on inheritance question instead of defending |
| Code execution | **4/10** — typo, missing super().__init__, missing core overrides, didn't run tests |
| Time management | **3/10** — environment + import detours; ticket 1 incomplete |
| Conviction under pressure | **5/10** — defended base-class refusal cleanly; gave up on inheritance defense too easily |
| Closing | **4/10** — undersold the work, framed it as "I did better in practice" |

### The recurring pattern across A5 → A6 → this interview

A5 had `__getattribute__` reaches and `is not "string"` mistakes. A6 had ABC-vs-Enum confusion and treating tuples as bools. This interview had `super().__init__()` written without inspecting the parent and a typo that would crash on first invocation. **Same root cause, three different surface symptoms: writing code without first reading the thing it depends on.**

The drills built the night before this interview (assignment_7_interview_prep_29thApril) target exactly this — `super()` discipline, capture-and-react patterns, coordinated multi-method overrides. Done correctly on the drills. The gap between the drills and the interview was: **the drills were done after the interview**, not before. There is no shortcut here — the muscle memory only forms by writing the pattern repeatedly under tests.

### Forward-looking lessons

1. **Five-second rule for any inherited method:** before writing `super().<anything>()`, open the parent file for five seconds. Confirm what's there. Decide what to keep.
2. **Defend, don't capitulate, when you have a reason:** if the interviewer challenges a design and you have a defensible answer, say it. *"Here's what I'd reuse, here's why inheritance isn't dead weight."* If you've genuinely changed your mind, fine — but don't change it just because a senior asked.
3. **30-second budget for setup/imports:** if it's not the test, it's not worth the clock. Patch around it and move on.
4. **Run tests every 5 minutes, not at the end.** The typo bug was a 30-second find. It got shipped.
5. **Closer should be forward-framed:** "this approach went somewhere new" beats "I'd have done better with my old approach." Both are honest. Only one helps.
6. **Reread the ticket twice before coding.** "All existing method signatures remain compatible" was a flashing neon sign saying "override these specific methods." The signal was present; reading was incomplete.

### Net read

Not a disaster. Not a win. The thinking was strong enough that an evaluator paying attention would see growth from the original Ultimate TicTacToe interview. The execution was weak enough that an evaluator reading only the artifact (code at end of session) would see incomplete work with a crash bug. Outcome will depend on how much weight Sharath and Nishith give to the *process* vs the *product* — and that is genuinely uncertain.

**The next interview-shaped event must show the inverse:** strong product, even if the process is less articulate. The drills target that. Do them.
