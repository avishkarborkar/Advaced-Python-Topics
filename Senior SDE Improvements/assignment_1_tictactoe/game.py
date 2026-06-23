class TicTacToe:
    """
    A basic 3x3 Tic-Tac-Toe implementation.
    Works fine for 3x3, but NOT designed for NxN or future extensions.
    """

    def __init__(self, board_size: int, win_condition: int):
        self.board_size = board_size
        self.win_condition = win_condition
        self.board = [[None] * board_size for _ in range(board_size)]
        self.current_player = "X"
        self.game_over = False
        self.winner = None

    def make_move(self, row, col):
        if self.game_over:
            print("Game is already over!")
            return False

        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            print("Invalid position!")
            return False

        if self.board[row][col] is not None:
            print("Cell already occupied!")
            return False

        self.board[row][col] = self.current_player

        if self._check_winner():
            self.game_over = True
            self.winner = self.current_player
        elif self._is_board_full():
            self.game_over = True
            self.winner = None  # Draw
        else:
            self.current_player = "O" if self.current_player == "X" else "X"

        return True

    def _check_winner(self):
        p = self.current_player
        b = self.board
        n = self.board_size
        wc = self.win_condition

        def count_consecutive(cells):
            count = 0
            for cell in cells:
                if cell == p:
                    count += 1
                    if count >= wc:
                        return True
                else:
                    count = 0
            return False

        # Check rows
        for row in range(n):
            if count_consecutive(b[row]):
                return True

        # Check columns
        for col in range(n):
            if count_consecutive(b[row][col] for row in range(n)):
                return True

        # Check top-left to bottom-right diagonals
        for start in range(-(n - 1), n):
            diagonal = [b[r][r - start] for r in range(n) if 0 <= r - start < n]
            if count_consecutive(diagonal):
                return True

        # Check top-right to bottom-left diagonals
        for start in range(0, 2 * n - 1):
            diagonal = [b[r][start - r] for r in range(n) if 0 <= start - r < n]
            if count_consecutive(diagonal):
                return True

        return False

    def _is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell is None:
                    return False
        return True

    def display(self):
        symbols = {None: ".", "X": "X", "O": "O"}
        print()
        for row in self.board:
            print(" | ".join(symbols[cell] for cell in row))
            print("-" * 9)
        print(f"Current player: {self.current_player}")
        if self.game_over:
            if self.winner:
                print(f"Winner: {self.winner}")
            else:
                print("It's a draw!")
        print()


if __name__ == "__main__":
    game = TicTacToe(board_size=3, win_condition=3)
    game.display()

    # Example game
    moves = [(0, 0), (1, 1), (0, 1), (1, 0), (0, 2)]  # X wins top row
    for row, col in moves:
        print(f"Player {game.current_player} plays ({row}, {col})")
        game.make_move(row, col)
        game.display()
