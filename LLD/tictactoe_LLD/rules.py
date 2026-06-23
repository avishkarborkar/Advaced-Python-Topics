from tictactoe_LLD import TicTacToe

class Rules:
    def is_valid_move(self, action: int, board: TicTacToe):
        if action < 0 or action > 8:
            return False

        row, col = action // 3, action % 3

        if board[row][col] == 0:
            return False

        board[row][col] = action
        
        return True
