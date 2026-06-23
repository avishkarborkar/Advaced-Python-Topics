from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, color: str, name: str):
        self.color = color
        self.name = name

    @abstractmethod
    def can_move(self, start, end, board):
        pass


class Pawn(Piece):
    def can_move(self, start, end, board) -> bool:
        r, c = start
        nr, nc = end
        direction = 1 if self.color == 'W' else -1
        starting_row = 1 if self.color == 'W' else 6

        if not (0 <= nr <= 7 and 0 <= nc <= 7):
            return False

        # One square forward, destination empty
        if nr == r + direction and nc == c and board[nr][nc] is None:
            return True

        # Two squares forward from starting row, both squares empty
        if (r == starting_row and nr == r + 2 * direction
                and nc == c
                and board[r + direction][c] is None
                and board[nr][nc] is None):
            return True

        # Diagonal capture
        if (nr == r + direction and abs(nc - c) == 1
                and board[nr][nc] is not None
                and board[nr][nc].color != self.color):
            return True

        return False


class Rook(Piece):
    def __init__(self, color, name):
        super().__init__(color, name)

    def can_move(self, start, end, board) -> bool:
        r, c = start
        nr, nc = end
        if not (0 <= nr <= 7 and 0 <= nc <= 7):
            return False
        # Must move along a row or column, not diagonally or nowhere
        if r != nr and c != nc:
            return False
        if r == nr and c == nc:
            return False
        # Can't capture own piece
        if board[nr][nc] is not None and board[nr][nc].color == self.color:
            return False
        # Path must be clear
        if r == nr:
            step = 1 if nc > c else -1
            for col in range(c + step, nc, step):
                if board[r][col] is not None:
                    return False
        else:
            step = 1 if nr > r else -1
            for row in range(r + step, nr, step):
                if board[row][c] is not None:
                    return False
        return True


class Knight(Piece):
    def __init__(self, color, name):
        super().__init__(color, name)

    def can_move(self, start, end, board) -> bool:
        r, c = start
        nr, nc = end
        if not (0 <= nr <= 7 and 0 <= nc <= 7):
            return False
        if board[nr][nc] is not None and board[nr][nc].color == self.color:
            return False
        dr, dc = abs(nr - r), abs(nc - c)
        return (dr, dc) in ((2, 1), (1, 2))


class Bishop(Piece):
    def __init__(self, color, name):
        super().__init__(color, name)

    def can_move(self, start, end, board) -> bool:
        r, c = start
        nr, nc = end
        if not (0 <= nr <= 7 and 0 <= nc <= 7):
            return False
        if abs(nr - r) != abs(nc - c) or r == nr:
            return False
        if board[nr][nc] is not None and board[nr][nc].color == self.color:
            return False
        row_step = 1 if nr > r else -1
        col_step = 1 if nc > c else -1
        row, col = r + row_step, c + col_step
        while (row, col) != (nr, nc):
            if board[row][col] is not None:
                return False
            row += row_step
            col += col_step
        return True


class Queen(Piece):
    def __init__(self, color, name):
        super().__init__(color, name)

    def can_move(self, start, end, board) -> bool:
        return (Rook(self.color, self.name).can_move(start, end, board) or
                Bishop(self.color, self.name).can_move(start, end, board))


class King(Piece):
    def __init__(self, color, name):
        super().__init__(color, name)

    def can_move(self, start, end, board) -> bool:
        r, c = start
        nr, nc = end
        if not (0 <= nr <= 7 and 0 <= nc <= 7):
            return False
        if board[nr][nc] is not None and board[nr][nc].color == self.color:
            return False
        return abs(nr - r) <= 1 and abs(nc - c) <= 1 and (nr, nc) != (r, c)




