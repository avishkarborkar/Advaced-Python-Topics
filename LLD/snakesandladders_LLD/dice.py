import random

class Dice:
    def __init__(self, sides: int):
        self.sides = sides

    @property
    def roll_dice(self):
        return random.randint(1, self.sides)
    
    