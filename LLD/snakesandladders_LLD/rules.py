from players import Player

class Rules:
    
    def is_valid_move(self, dice_roll_number: int, player: Player) -> bool:
        if player.player_tile_number + dice_roll_number > 100:
            return False
        return True
        
    def is_winner(self, player: Player) -> bool:
        if player.player_tile_number == 100:
            return True
        return False
    
