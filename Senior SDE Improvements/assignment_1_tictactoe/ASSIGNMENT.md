# Assignment 1: NxN Tic-Tac-Toe with Undo/Redo

## Overview
You are given a working 3x3 Tic-Tac-Toe implementation in `game.py`. It works, but it's rigid — hardcoded to a 3x3 board with hardcoded win-checking logic. Your job is to refactor and extend it.

---

## Files
- `game.py` — Starter code. A working 3x3 TicTacToe class. **Edit this file.**
- `test_game.py` — Test suite. **Do NOT modify.** All tests must pass when you're done.

---

## Part A: Make It NxN with Configurable Win Condition

### Requirements

1. **The `TicTacToe` constructor must accept two parameters:**
   - `board_size` (int) — the board will be `board_size x board_size`
   - `win_condition` (int) — how many in a row/column/diagonal needed to win

2. **Board initialization:** Create an NxN board (list of lists, `None` for empty cells).

3. **Move validation:** `make_move(row, col)` should:
   - Reject moves outside the NxN bounds
   - Reject moves on occupied cells
   - Reject moves after game is over
   - Return `False` for invalid moves, `True` for valid moves

4. **Win detection:** Must work for ANY board size and ANY win condition. The hardcoded row/col/diagonal checks in the starter code will NOT work for NxN. You need a general algorithm that:
   - Checks all rows for `win_condition` consecutive same-player marks
   - Checks all columns for `win_condition` consecutive same-player marks
   - Checks all diagonals (both directions) for `win_condition` consecutive same-player marks
   - Works even when `win_condition < board_size` (e.g., 3-in-a-row on a 5x5 board)

5. **Draw detection:** Board is full and no winner.

### Hints
- Think about how to check for N consecutive marks in a line without hardcoding indices.
- The win check only needs to look around the last move played — you don't need to scan the entire board every time (but it's okay if you do).

---

## Part B: Add Undo / Redo

### Requirements

1. **Add an `undo()` method:**
   - Reverses the last move
   - Restores the board cell to `None`
   - Switches back to the previous player's turn
   - If the undone move was a winning move, un-ends the game (`game_over = False`, `winner = None`)
   - Returns `False` if there's nothing to undo (no moves made)
   - Returns `True` on successful undo

2. **Add a `redo()` method:**
   - Replays the last undone move
   - Returns `False` if there's nothing to redo
   - Returns `True` on successful redo

3. **Redo history is cleared when a new move is made after an undo.**
   - Example: move → move → undo → **new move** → redo should return `False`

### Hints
- Think about what data structure naturally supports undo/redo.
- What's the minimum state you need to store per move?

---

## How to Run Tests

```bash
cd assignment_1_tictactoe
pytest test_game.py -v
```

---

## Evaluation Criteria

| Criteria | What I'm Looking For |
|----------|---------------------|
| **Correctness** | All 18 tests pass |
| **Generalization** | Win check works for any N and any win_condition, not just 3x3 |
| **Code clarity** | Can I read your win-check logic and immediately understand it? |
| **State management** | Undo/redo is clean, doesn't leak or corrupt state |
| **No over-engineering** | You didn't add stuff that wasn't asked for |
| **Edge cases** | Bounds checking, empty undo, redo after new move |

---

## Get Started
1. Read `game.py` — understand what's there
2. Read `test_game.py` — understand what's expected
3. Modify `game.py` to pass all Part A tests first
4. Then add undo/redo to pass Part B tests
5. Run `pytest test_game.py -v` and make sure everything is green

Good luck.
