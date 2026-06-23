from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        self.board = None
        for i in range(8):
            for j in range(8):
                self.board[i][j] = None

    def setup(self):
        for i in range(8):
            self.board[1][i] = Pawn('B', 'P')
            self.board[i][6] = Pawn('W', 'P')
        self.board[0][0] = Rook('W', 'R')
        self.board[0][7] = Rook('W', 'R')
        self.board[0][1] = Knight('W', 'K')
        self.board[0][6] = Knight('W', 'K')
        self.board[0][2] = Bishop('W', 'B')
        self.board[0][5] = Bishop('W', 'B')
        self.board[0][3] = Queen('W', 'Q')
        self.board[0][4] = King('W', 'K')

        self.board[0][0] = Rook('B', 'R')
        self.board[0][7] = Rook('B', 'R')
        self.board[0][1] = Knight('B', 'K')
        self.board[0][6] = Knight('B', 'K')
        self.board[0][2] = Bishop('B', 'B')
        self.board[0][5] = Bishop('B', 'B')
        self.board[0][3] = Queen('B', 'Q')
        self.board[0][4] = King('B', 'K')



        
