from enum import Enum
from random import shuffle

class Card(Enum):
    """ Enum representing types of cards"""
    DUKE = "duke"
    ASSASSIN = "assassin"
    AMBASSADOR = "ambassador"
    CAPTAIN = "captain"
    CONTESSA = "contessa"

class State():
    """ Represents the current state of a game of Coup """
    num_players: int
    deck: list[Card]
    player_cards: dict[int, list[Card]]
    player_coins: dict[int, int]
    
    def __init__(self, num_players: int = 6):
        self.num_players = num_players
        self.player_coins = {num: 2 for num in range(self.num_players)}
        self.player_cards = {num: [] for num in range(self.num_players)}
        self._deal_cards()

    def _deal_cards(self):
        deck = [Card.DUKE] * 3 + [Card.ASSASSIN] * 3 + [Card.AMBASSADOR] * 3 + [Card.CAPTAIN] * 3 + [Card.CONTESSA] * 3
        shuffle(deck)
        for player in range(self.num_players):
            self.player_cards[player].append(deck.pop())
            self.player_cards[player].append(deck.pop())







