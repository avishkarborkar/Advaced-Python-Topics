# This is where I write  the rules for the Ultimate TicTacToe

from game import TicTacToe
from board_manager import SubBoardManager

class MoveValidator:
    def __init__(self):
        pass

    def is_valid_move(self, active_sub_board: tuple | None, outer_row: int, outer_col: int, sub_boards: SubBoardManager) -> bool:

        if not (0 <= outer_row < 3 and 0 <= outer_col < 3):
            return False

        if sub_boards.is_sub_board_decided(outer_row, outer_col):
            return False
        
        if active_sub_board is None:
            return True

        return active_sub_board == (outer_row, outer_col)
    
    def compute_next_active_sub_board(self, inner_row: int, inner_col: int, sub_boards: SubBoardManager) -> tuple | None:

        if sub_boards.is_sub_board_decided(inner_row, inner_col):
            return None

        return (inner_row, inner_col)
    
        
# Calude assessment

# You did great! Honest assessment:

# Wins:

# ✓ Understood stateless design — no game state stored in the validator
# ✓ Clean method signatures with proper type hints
# ✓ Correct use of SubBoardManager API (calling is_sub_board_decided instead of raw logic)
# ✓ Got the final logic order right (decided → free choice → match)
# ✓ Only needed hints on the logic, not on the structure