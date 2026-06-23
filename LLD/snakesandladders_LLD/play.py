from snakesandladders import SnakesAndLadders
from players import Player


def play():
    game = SnakesAndLadders()

    player1 = Player()
    player1.player_id = "Alice"

    player2 = Player()
    player2.player_id = "Bob"

    game.add_player(player1)
    game.add_player(player2)

    turn = 0
    while not all(p.game_over for p in [player1, player2]):
        turn += 1
        game.make_move()
        for p in [player1, player2]:
            status = "WON" if p.game_over else f"tile {p.player_tile_number}"
            print(f"  {p.player_id}: {status}")
        print()

    print(f"Game over in {turn} turns.")


if __name__ == "__main__":
    play()
