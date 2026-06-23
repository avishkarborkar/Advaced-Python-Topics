from abc import ABC, abstractmethod

class BoardStrategy(ABC):

    @abstractmethod
    def set_entity(self) -> None:
        pass


class StandardStrategy(BoardStrategy):

    def __init__(self):
        # Keys are FROM tile, values are TO tile. Snakes go down, ladders go up.
        self.snakes = {
            99: 78,
            95: 75,
            93: 73,
            87: 24,
            64: 60,
            62: 19,
            54: 34,
            17: 7,
        }
        self.ladders = {
            4:  14,
            9:  31,
            20: 38,
            28: 84,
            40: 59,
            51: 67,
            63: 81,
            71: 91,
        }

    def set_entity(self) -> None:
        pass
