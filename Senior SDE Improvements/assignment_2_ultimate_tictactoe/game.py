"""
Base TicTacToe class.
This is your FOUNDATION. You must subclass this to build Ultimate TicTacToe.
You may modify this class IF NEEDED, but the goal is to EXTEND, not rewrite.
"""


class TicTacToe:
    """A standard NxN Tic-Tac-Toe game."""

    def __init__(self, board_size=3, win_condition=3):
        self.board_size = board_size
        self.win_condition = win_condition
        self.board = [[None for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = "X"
        self.game_over = False
        self.winner = None

    def make_move(self, row, col):
        """Place current player's mark at (row, col). Returns True if valid."""
        if self.game_over:
            return False
        if not self._is_valid_position(row, col):
            return False
        if self.board[row][col] is not None:
            return False

        self.board[row][col] = self.current_player

        if self._check_winner(row, col):
            self.game_over = True
            self.winner = self.current_player
        elif self._is_board_full():
            self.game_over = True
        else:
            self._switch_player()

        return True

    def _is_valid_position(self, row, col):
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    def _switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def _check_winner(self, row, col):
        """Check if the last move at (row, col) won the game."""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        player = self.board[row][col]

        for dr, dc in directions:
            count = 1
            # Check forward
            r, c = row + dr, col + dc
            while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            # Check backward
            r, c = row - dr, col - dc
            while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc

            if count >= self.win_condition:
                return True
        return False

    def _is_board_full(self):
        return all(self.board[r][c] is not None
                   for r in range(self.board_size)
                   for c in range(self.board_size))

    def get_cell(self, row, col):
        """Returns the value at (row, col) — 'X', 'O', or None."""
        if self._is_valid_position(row, col):
            return self.board[row][col]
        return None

    def reset(self):
        """Reset the board to initial state."""
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = "X"
        self.game_over = False
        self.winner = None

    def display(self):
        symbols = {None: ".", "X": "X", "O": "O"}
        for row in self.board:
            print(" | ".join(symbols[cell] for cell in row))
        print()

# Base class that represents a 3x3 TicTacToe - Standard.
# Has methods to 1. Make board, 2. Make Moves, 3. Check if Board full, 4. Check Winner, 5. Reset Board
# So there is no need to rewrite for a bigger board, We will inbherit from baseclass to use.
