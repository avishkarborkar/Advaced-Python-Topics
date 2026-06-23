"""
Tests for your NxN TicTacToe implementation.
These tests MUST pass when you're done.
DO NOT modify these tests.
"""
import pytest


# ============================================================
# PART A TESTS — NxN Board with Configurable Win Condition
# ============================================================

class TestNxNBoard:

    def test_3x3_default_game(self):
        """Standard 3x3 game should still work."""
        from game import TicTacToe
        game = TicTacToe(board_size=3, win_condition=3)
        game.make_move(0, 0)  # X
        game.make_move(1, 1)  # O
        game.make_move(0, 1)  # X
        game.make_move(1, 0)  # O
        game.make_move(0, 2)  # X wins
        assert game.game_over is True
        assert game.winner == "X"

    def test_5x5_with_win_condition_4(self):
        """5x5 board, need 4 in a row to win."""
        from game import TicTacToe
        game = TicTacToe(board_size=5, win_condition=4)
        # X plays row 0: cols 0,1,2,3
        # O plays row 1: cols 0,1,2
        moves_x = [(0, 0), (0, 1), (0, 2), (0, 3)]
        moves_o = [(1, 0), (1, 1), (1, 2)]
        for i in range(3):
            game.make_move(*moves_x[i])
            game.make_move(*moves_o[i])
        game.make_move(*moves_x[3])  # X gets 4 in a row
        assert game.game_over is True
        assert game.winner == "X"

    def test_5x5_three_in_a_row_does_not_win_when_need_4(self):
        """3 in a row shouldn't win when win_condition is 4."""
        from game import TicTacToe
        game = TicTacToe(board_size=5, win_condition=4)
        game.make_move(0, 0)  # X
        game.make_move(1, 0)  # O
        game.make_move(0, 1)  # X
        game.make_move(1, 1)  # O
        game.make_move(0, 2)  # X — 3 in a row but need 4
        assert game.game_over is False

    def test_4x4_diagonal_win(self):
        """Diagonal win on a 4x4 board."""
        from game import TicTacToe
        game = TicTacToe(board_size=4, win_condition=4)
        # X: (0,0), (1,1), (2,2), (3,3)
        # O: (0,1), (0,2), (0,3)
        game.make_move(0, 0)  # X
        game.make_move(0, 1)  # O
        game.make_move(1, 1)  # X
        game.make_move(0, 2)  # O
        game.make_move(2, 2)  # X
        game.make_move(0, 3)  # O
        game.make_move(3, 3)  # X wins diagonal
        assert game.game_over is True
        assert game.winner == "X"

    def test_invalid_move_out_of_bounds(self):
        """Out of bounds move on NxN board should fail."""
        from game import TicTacToe
        game = TicTacToe(board_size=4, win_condition=3)
        result = game.make_move(5, 5)
        assert result is False

    def test_invalid_move_occupied_cell(self):
        """Moving to an occupied cell should fail."""
        from game import TicTacToe
        game = TicTacToe(board_size=4, win_condition=3)
        game.make_move(0, 0)
        result = game.make_move(0, 0)
        assert result is False

    def test_draw_on_full_board(self):
        """A full board with no winner is a draw."""
        from game import TicTacToe
        game = TicTacToe(board_size=3, win_condition=3)
        # Classic draw sequence
        moves = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 1), (2, 0), (2, 2),
        ]
        # X: (0,0), (0,2), (1,1), (2,1), (2,2)
        # O: (0,1), (1,0), (1,2), (2,0)
        for r, c in moves:
            game.make_move(r, c)
        assert game.game_over is True
        assert game.winner is None

    def test_column_win(self):
        """Column win on NxN board."""
        from game import TicTacToe
        game = TicTacToe(board_size=5, win_condition=3)
        # X plays column 2: rows 0, 1, 2
        # O plays column 0: rows 0, 1
        game.make_move(0, 2)  # X
        game.make_move(0, 0)  # O
        game.make_move(1, 2)  # X
        game.make_move(1, 0)  # O
        game.make_move(2, 2)  # X wins with 3 in col 2
        assert game.game_over is True
        assert game.winner == "X"

    def test_anti_diagonal_win(self):
        """Anti-diagonal win."""
        from game import TicTacToe
        game = TicTacToe(board_size=4, win_condition=3)
        # X: (0,3), (1,2), (2,1) — anti-diagonal
        # O: (0,0), (1,0)
        game.make_move(0, 3)  # X
        game.make_move(0, 0)  # O
        game.make_move(1, 2)  # X
        game.make_move(1, 0)  # O
        game.make_move(2, 1)  # X — 3 in anti-diagonal
        assert game.game_over is True
        assert game.winner == "X"


# ============================================================
# PART B TESTS — Undo / Redo
# ============================================================

# class TestUndoRedo:

#     def test_undo_single_move(self):
#         """Undo should reverse the last move."""
#         from game import TicTacToe
#         game = TicTacToe(board_size=3, win_condition=3)
#         game.make_move(0, 0)  # X
#         game.undo()
#         assert game.board[0][0] is None
#         assert game.current_player == "X"

#     def test_undo_restores_player_turn(self):
#         """After undo, it should be the previous player's turn."""
#         from game import TicTacToe
#         game = TicTacToe(board_size=3, win_condition=3)
#         game.make_move(0, 0)  # X
#         game.make_move(1, 1)  # O
#         game.undo()
#         assert game.current_player == "O"
#         assert game.board[1][1] is None

#     def test_redo_after_undo(self):
#         """Redo should replay the undone move."""
#         from game import TicTacToe
#         game = TicTacToe(board_size=3, win_condition=3)
#         game.make_move(0, 0)  # X
#         game.make_move(1, 1)  # O
#         game.undo()
#         game.redo()
#         assert game.board[1][1] == "O"
#         assert game.current_player == "X"

#     def test_redo_cleared_after_new_move(self):
#         """Making a new move after undo should clear redo history."""
#         from game import TicTacToe
#         game = TicTacToe(board_size=3, win_condition=3)
#         game.make_move(0, 0)  # X
#         game.make_move(1, 1)  # O
#         game.undo()
#         game.make_move(2, 2)  # O plays somewhere else
#         result = game.redo()
#         assert result is False  # Nothing to redo

#     def test_undo_on_empty_game(self):
#         """Undo on a fresh game should fail gracefully."""
#         from game import TicTacToe
#         game = TicTacToe(board_size=3, win_condition=3)
#         result = game.undo()
#         assert result is False

#     def test_redo_without_undo(self):
#         """Redo without prior undo should fail gracefully."""
#         from game import TicTacToe
#         game = TicTacToe(board_size=3, win_condition=3)
#         game.make_move(0, 0)
#         result = game.redo()
#         assert result is False

#     def test_multiple_undo_redo(self):
#         """Multiple undos followed by multiple redos."""
#         from game import TicTacToe
#         game = TicTacToe(board_size=3, win_condition=3)
#         game.make_move(0, 0)  # X
#         game.make_move(1, 1)  # O
#         game.make_move(2, 2)  # X
#         game.undo()  # undo (2,2)
#         game.undo()  # undo (1,1)
#         assert game.board[2][2] is None
#         assert game.board[1][1] is None
#         assert game.current_player == "O"
#         game.redo()  # redo (1,1)
#         assert game.board[1][1] == "O"
#         game.redo()  # redo (2,2)
#         assert game.board[2][2] == "X"
#         assert game.current_player == "O"  # back to O's turn

#     def test_undo_a_winning_move(self):
#         """Undoing a winning move should un-end the game."""
#         from game import TicTacToe
#         game = TicTacToe(board_size=3, win_condition=3)
#         game.make_move(0, 0)  # X
#         game.make_move(1, 0)  # O
#         game.make_move(0, 1)  # X
#         game.make_move(1, 1)  # O
#         game.make_move(0, 2)  # X wins
#         assert game.game_over is True
#         game.undo()
#         assert game.game_over is False
#         assert game.winner is None
#         assert game.current_player == "X"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
