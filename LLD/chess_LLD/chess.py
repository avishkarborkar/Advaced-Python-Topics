from board import Board
from players import Player
from pieces import Piece

class Chess:
    def __init__(self, player1: int, player2: int):
        self.board = Board()
        #Player 1 always white and alwyas goes first
        self.player1 = player1
        self.player2 = player2

        self.current_player = self.player1

    def get_available_pieces(self) -> list:
        white_pieces = []
        black_pieces = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j] 
                if piece is None:
                    continue
                if piece.color == 'W':
                    white_pieces.append((piece.color + piece.name))
                elif piece.color == 'B':
                    black_pieces.append((piece.color + piece.name))

    def make_move(self, piece: Piece, start, end):
        if piece.can_move(start, end, self.board.board):
            r, c = start
            nr, nc = end
            self.board.board[r][c] = None
            self.board.board[nr][nc] = piece
            if self.current_player == self.player1:
                self.current_player = self.player2
            else:
                self.current_player = self.player1
        else:
            raise ValueError("Invalid Move !")
        

# flow
# Setup board with all pieces in starting poisiton
# player 1 - White wants to make move
# When we call self.board[0][0] = Rook('W', 'Rook/R', (0,0))
# get_available_pieces()
# make_move()
  # Before making move and updating states of the Piece
  # We must validate
  # to validate we need 1. board state, piece, start, end.
  # we chech using piece.can_move()


# for make_move():
    # We must check which side its moving as well
    # Black and White

[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]
[(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)]
[(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)]
[(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7)]
[(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7)]
[(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7)]
[(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)]
[(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]