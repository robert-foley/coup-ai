from enum import Enum
class Card(Enum):
    """ Enum representing types of cards"""
    DUKE = "duke"
    ASSASSIN = "assassin"
    AMBASSADOR = "ambassador"
    CAPTAIN = "captain"
    CONTESSA = "contessa"

    def __str__(self):
        return self.value