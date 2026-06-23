class Board:
    def __init__(self):
        self.board = [[0]*10 for _ in range(10)]
        idx = 1
        for i in range(10):
            for j in range(10):
                self.board[i][j] = idx
                idx += 1

    def tile_to_coord(self, tile):
        return ((tile - 1) // 10, (tile - 1) % 10)