# Assignment 2: Ultimate Tic-Tac-Toe — Interview Prep

## Difficulty: ★★★★☆
## Focus: **Inheritance**, **Composition**, **Reuse over Rewrite**, **Abstraction**

---

## THE INTERVIEW CONTEXT

You already attempted this problem in an interview. The feedback was:
- You modified the base class instead of **subclassing** it
- You did not **reuse** existing logic (win detection, move validation, etc.)
- You did not create separate files — everything was in one place

**This assignment simulates the same problem.** The goal is to practice doing it the RIGHT way this time.

---

## STRICT RULES (These mirror the interview expectations)

### ❌ Do NOT:
1. **Do NOT modify `game.py`** — the base `TicTacToe` class is locked. Treat it as a 3rd-party library you cannot change.
2. **Do NOT rewrite logic that already exists** — no new win-checking code, no new board-full check, no new switch-player logic.
3. **Do NOT put everything in one file** — you must separate concerns across multiple files.
4. **Do NOT copy-paste from `game.py`** — if you need the logic, use inheritance or composition to reach it.

### ✅ You MUST:
1. **Subclass** `TicTacToe` for your `UltimateTicTacToe` class.
2. **Compose** the outer board using a `TicTacToe` instance (since the outer board is itself a 3x3 tic-tac-toe of sub-board winners).
3. **Use a 3x3 grid of `TicTacToe` instances** for the sub-boards.
4. **Reuse** the base class's `_check_winner`, `_is_board_full`, `_switch_player`, and `make_move` logic wherever possible.
5. **Override** only where necessary — `make_move` gets a new signature, everything else should come "for free" from the base.

---

## FILE STRUCTURE (REQUIRED)

| File | Purpose | Status |
|------|---------|--------|
| `game.py` | Base `TicTacToe` class | **LOCKED — do not modify** |
| `ultimate.py` | `UltimateTicTacToe` class (subclass of `TicTacToe`) | **Create this** |
| `board_manager.py` | `SubBoardManager` — manages the 9 sub-boards (composition) | **Create this** |
| `rules.py` | `MoveValidator` — encapsulates move legality rules (sending, active board, etc.) | **Create this** |
| `test_game.py` | Test suite | **DO NOT MODIFY** |

You are expected to split responsibilities across these files. Putting everything in `ultimate.py` will fail the review — same mistake as last time.

---

## PART 1: `board_manager.py` — SubBoardManager (Composition)

This class owns the 9 sub-boards and knows how to query/update them.

### Responsibilities:
- Store a 3x3 grid of `TicTacToe` instances (one per sub-board)
- Expose methods to:
  - `get_sub_board(outer_row, outer_col)` → returns the `TicTacToe` instance
  - `get_cell(outer_row, outer_col, inner_row, inner_col)` → "X", "O", or None
  - `get_sub_board_winner(outer_row, outer_col)` → "X", "O", or None
  - `is_sub_board_full(outer_row, outer_col)` → bool
  - `is_sub_board_decided(outer_row, outer_col)` → bool (won OR full)

### Why this matters:
- **Single Responsibility Principle** — `UltimateTicTacToe` should not directly poke into sub-boards. That's this class's job.
- Makes the outer game code readable: `self.sub_boards.get_sub_board_winner(r, c)` vs. raw 2D indexing.

---

## PART 2: `rules.py` — MoveValidator

This class encapsulates the **rules** of Ultimate TicTacToe (the sending logic, free choice, etc.).

### Responsibilities:
- `is_valid_move(active_sub_board, outer_row, outer_col, sub_boards)` → bool
  - If `active_sub_board` is set: the move's outer position must match
  - If `active_sub_board` is None (free choice): any non-decided sub-board is fine
  - The specific sub-board must not be won or full

- `compute_next_active_sub_board(inner_row, inner_col, sub_boards)` → (row, col) or None
  - After a move, the next active sub-board is `(inner_row, inner_col)`
  - Unless that sub-board is won or full → return None (free choice)

### Why this matters:
- **Rules are separate from game logic** — you can change rules without touching the game class.
- This is where you'd swap in variants (e.g., "anarchy mode" where there's no sending rule).

---

## PART 3: `ultimate.py` — UltimateTicTacToe

This class subclasses `TicTacToe` and orchestrates the game.

### Requirements:

1. **Must subclass `TicTacToe`.** Pass `board_size=3, win_condition=3` to super (the **outer** board is itself a tic-tac-toe of sub-board winners).

2. **Compose with `SubBoardManager`** — don't store sub-boards as raw 2D lists.

3. **Use `MoveValidator`** — don't inline rule checks in `make_move`.

4. **Override `make_move`** with signature:
   ```python
   def make_move(self, outer_row, outer_col, inner_row, inner_col) -> bool
   ```

5. **When a sub-board is won:** call `super().make_move(outer_row, outer_col)` to record the winner on the **outer** board. This way, the base class's `_check_winner` automatically detects if the OUTER game is won.
   - This is the key insight: the outer game state IS a tic-tac-toe, and you already have that logic!

6. **Required query methods:**
   - `get_sub_board_cell(outer_row, outer_col, inner_row, inner_col)` → "X", "O", or None
   - `get_sub_board_winner(outer_row, outer_col)` → "X", "O", or None
   - `get_active_sub_board()` → (row, col) tuple or None

7. **Inherited properties** (from base class — do NOT redefine):
   - `self.current_player`
   - `self.game_over`
   - `self.winner`

---

## THE KEY INSIGHT (This is what the interviewer is looking for)

The OUTER board in Ultimate TicTacToe is itself a 3x3 tic-tac-toe — where each "cell" is the winner of the corresponding sub-board.

**So:**
- `UltimateTicTacToe` IS-A `TicTacToe` (for the outer board)
- `UltimateTicTacToe` HAS 9 `TicTacToe` instances (for the sub-boards, via `SubBoardManager`)

When a sub-board is won:
```python
# Don't write new logic to check if the outer game is over!
# Just call the base class and let it do the work.
super().make_move(outer_row, outer_col)  # base class updates self.board, self.winner, self.game_over
```

If you find yourself writing `for i in range(3): for j in range(3): check 3 in a row...` — **STOP**. You're rewriting base class logic. Use `super()`.

---

## COMMON MISTAKES (Do not repeat these)

| Mistake | Why It Fails Review |
|---------|---------------------|
| Modifying `game.py` to accept 4 parameters | You were asked to EXTEND, not rewrite |
| Copying `_check_winner` into `ultimate.py` | Violates DRY, misses inheritance |
| Storing sub-boards as `[[None]*9]*9` raw grid | Misses composition opportunity |
| Putting all rules inline in `make_move` | Violates Single Responsibility |
| Creating parallel `self.x_current_player` instead of reusing `self.current_player` | Duplicates state |
| Everything in one file | Fails separation of concerns review |

---

## STEP-BY-STEP APPROACH (Recommended Order)

1. **Read `game.py` carefully.** Note what you get "for free" via inheritance.
2. **Read `test_game.py`.** Understand the exact interface expected.
3. **Write `board_manager.py`** — get sub-board storage working.
4. **Write `rules.py`** — encode the sending rules.
5. **Write `ultimate.py`:**
   - `__init__` calls `super().__init__(3, 3)` and creates a `SubBoardManager` + `MoveValidator`.
   - `make_move` delegates validation to `MoveValidator`, plays the move on the right sub-board, and if won, calls `super().make_move(outer_row, outer_col)`.
6. **Run tests incrementally:**
   ```bash
   pytest test_game.py::TestUltimateTicTacToeInheritance -v
   pytest test_game.py::TestBasicMoves -v
   pytest test_game.py::TestSendingLogic -v
   pytest test_game.py::TestSubBoardWinning -v
   pytest test_game.py -v
   ```

---

## EVALUATION CRITERIA (This is exactly what the interviewer scores on)

| Criteria | What They Look For |
|----------|-------------------|
| **Did you subclass?** | Is `UltimateTicTacToe(TicTacToe)`, or did you write a standalone class? |
| **Did you reuse?** | Are you calling `super().make_move()` for outer win detection? |
| **Did you separate concerns?** | Are rules in `rules.py`, sub-boards in `board_manager.py`, orchestration in `ultimate.py`? |
| **Did you avoid modifying the base?** | `game.py` must be byte-identical to the original. |
| **Did you avoid duplicating logic?** | No new `_check_winner`, no new `_is_board_full`. |
| **Is the code clean?** | Would a reviewer say "yes, this is how I'd write it"? |
| **Does it pass tests?** | All of `test_game.py` must be green. |

---

## Run Tests

```bash
cd assignment_2_ultimate_tictactoe
pytest test_game.py -v
```

---

Good luck. This time, **subclass**, **reuse**, **separate**.
