
from game import TicTacToe

# UltimateTicTacToe
#     └── creates SubBoardManager()
#             └── creates 9 TicTacToe() instances internally

class SubBoardManager():
    def __init__(self):
        self.sub_boards : dict[tuple, TicTacToe] = {}
        for i in range(0, 3):
            for j in range(0, 3):
                self.sub_boards[(i, j)] = TicTacToe()
# We have a tuple keying system (i, j) = <TicTacToe>
# Example (0, 0) = <TicTacToe Obj1> (0, 1) = <TicTacToe Obj1> (0, 2) = <TicTacToe Obj1>

    def get_sub_board(self, outer_row: int, outer_col: int) -> TicTacToe:
        return self.sub_boards[(outer_row, outer_col)]
    
    def get_cell(self, outer_row: int, outer_col: int, inner_row: int, inner_col: int) -> str | None:
        sub_board: TicTacToe = self.sub_boards[(outer_row, outer_col)]
        return sub_board.get_cell(inner_row, inner_col)
    
    def get_sub_board_winner(self, outer_row: int, outer_col: int) -> str | None:
        # sub_board : TicTacToe = self.sub_boards[(outer_row, outer_col)]
        # Suggested by Vlad -> Line 10: self.sub_boards : dict[tuple, TicTacToe] = {}
        # This already gives a hint ot the linter
        sub_board = self.sub_boards[(outer_row, outer_col)]
        return sub_board.winner
    
    def is_sub_board_full(self, outer_row: int, outer_col: int) -> bool:
        sub_board : TicTacToe = self.sub_boards[(outer_row, outer_col)]
        return sub_board._is_board_full()
    
    def is_sub_board_decided(self, outer_row: int, outer_col: int) -> bool:
        # If won/full True, else: False
        is_won = self.get_sub_board_winner(outer_row=outer_row, outer_col=outer_col)
        is_full = self.is_sub_board_full(outer_row=outer_row, outer_col=outer_col)

        return is_won is not None or is_full



# CLaude review after I wrote everything from scratch

# Composition over inheritance — you didn't subclass TicTacToe here, you used it. That shows you know the difference.

# Reuse — you called sub_board.winner, sub_board.get_cell(), sub_board._is_board_full() instead of writing your own logic. Interviewers love this.

# Clean API — each method does one thing. The names are self-explanatory. Someone reading ultimate.py later can just call self.sub_boards.is_sub_board_decided(r, c) without knowing the internals.

# Separation of concerns — this file knows nothing about game rules, sending logic, or whose turn it is. It just manages boards.

# What an interviewer would think:

# "This person knows how to decompose a problem. They're not going to write a 300-line god class."

