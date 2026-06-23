from board import Board
from players import Player
from dice import Dice
from typing import List
from rules import Rules
from board_setup import StandardStrategy

class SnakesAndLadders:
    def __init__(self):
        self.board = Board()
        self.dice = Dice(6)
        self.rules = Rules()
        self.board_setup = StandardStrategy()
        self.player_queue: list[Player] = []
        self.current_player = None

    def add_player(self, player: Player):
        self.player_queue.append(player)

    def get_next_player(self):
        return self.player_queue.pop(0)
    
    def requeue_player(self, player):
        self.player_queue.append(player)
    
    def make_move(self):
        current_player = self.get_next_player()
        if not current_player.game_over:
            dice_roll = self.dice.roll_dice
            valid_move = self.rules.is_valid_move(dice_roll, current_player)

            if valid_move:
                next_move = current_player.player_tile_number + dice_roll

                if next_move in self.board_setup.snakes:
                    next_move = self.board_setup.snakes[next_move]
                elif next_move in self.board_setup.ladders:
                    next_move = self.board_setup.ladders[next_move]

                current_player.player_tile_number = next_move
            else:
                raise ValueError("Invalid Move")
            
            if self.rules.is_winner(current_player):
                current_player.game_over = True

            if not current_player.game_over:
                self.requeue_player(current_player)


