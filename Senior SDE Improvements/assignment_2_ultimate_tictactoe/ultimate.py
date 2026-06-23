from game import TicTacToe
from board_manager import SubBoardManager
from rules import MoveValidator

# UltimateTicTacToe (IS-A TicTacToe)
#     ├── super() gives you: current_player, game_over, winner, board (the outer 3x3)
#     ├── HAS-A SubBoardManager  → manages the 9 inner boards
#     ├── HAS-A MoveValidator    → checks if moves are legal
#     └── HAS-A active_sub_board → tracks where next player must play


class UltimateTicTacToe(TicTacToe):
    def __init__(self, board_size=3, win_condition=3):
        super().__init__(board_size, win_condition)
        self.sub_board_manager = SubBoardManager()
        self.move_validator = MoveValidator()
        self.active_sub_board = None

    def make_move(self, outer_row, outer_col, inner_row, inner_col) -> bool:

        if self.game_over:
            return False
        
        if not self.move_validator.is_valid_move(active_sub_board=self.active_sub_board, outer_row=outer_row, outer_col=outer_col, sub_boards=self.sub_board_manager):
            return False
        
        sub_board = self.sub_board_manager.get_sub_board(outer_row, outer_col)
        sub_board.current_player = self.current_player
        if not sub_board.make_move(inner_row, inner_col):
            return False
        
        if sub_board.winner is not None:
            super().make_move(outer_row, outer_col)  # records win on outer board
        else:
            self._switch_player()  # no win, just switch turns

        
        self.active_sub_board = self.move_validator.compute_next_active_sub_board(inner_row, inner_col, self.sub_board_manager)

        return True

    def get_sub_board_cell(self, outer_row, outer_col, inner_row, inner_col):
        return self.sub_board_manager.get_cell(outer_row, outer_col, inner_row, inner_col)

    def get_sub_board_winner(self, outer_row, outer_col):
        return self.sub_board_manager.get_sub_board_winner(outer_row, outer_col)

    def get_active_sub_board(self):
        return self.active_sub_board

        
# Honest assessment of ultimate.py - Based on CLaude PRompts:

# What you got RIGHT:

# ✓ Correct inheritance: UltimateTicTacToe(TicTacToe)
# ✓ super().__init__() called correctly
# ✓ Composition: created SubBoardManager and MoveValidator in __init__
# ✓ active_sub_board = None tracked correctly
# ✓ Understood the concept of overriding make_move
# What you struggled with:

# ✗ Took multiple attempts to get make_move right
# ✗ Kept confusing what active_sub_board is (tuple vs sub-board object)
# ✗ Double references: self.sub_board_manager.sub_board_manager
# ✗ Missing arguments to validator calls
# ✗ Forgot to add the query methods (get_sub_board_cell, etc.) — I had to add those
# ✗ Forgot to sync sub_board.current_player = self.current_player — I had to hint that
# ✗ Needed the pseudocode flow given to you before you could write it
    