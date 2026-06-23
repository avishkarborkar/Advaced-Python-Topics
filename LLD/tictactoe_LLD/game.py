from board import Board
from rules import Rules
from players import Player
import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = Board()
        self.rules = Rules()
        self.current_player = 1

    def make_move(self, action):
        if self.rules.is_valid_move(action, self.board):
            return True
        
        return False

    def check_winner(self):
        for row in range(3):
            row_sum = int(self.board[row, :].sum() == 3)
            if abs(row_sum) == 3:
                return self.board[row, 0]
            
        for col in range(3):
            col_sum = int(self.board[:, col].sum() == 3)
            if abs(col_sum) == 3:
                return self.board[0, col]
            
        if abs(np.diag(self.board)) == 3:
            return self.board[0, 0]
        
        if abs(np.fliplr(self.board).trace()) == 3:
            return int(self.board[0, 2])

        if not np.any(self.board == 0):
            return 0
        
        return None
    

        
            