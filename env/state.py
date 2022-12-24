from enum import Enum
from random import shuffle
from typing import Generator

from .action import Action, ActionType, is_honest_action, is_blockable_action, is_honest_counteraction, is_challengeable_action
from .card import Card

class TurnType(Enum):
    """ Enum representing different types of turns in Coup """
    ACTION = "action"  # Player can take an action (macro_turn = micro_turn)
    CHALLENGE_OP = "challenge_op"  # Player can challenge last action
    COUNTERACTION_OP = "counteraction_op"  # Player can make counteraction
    CA_CHALLENGE_OP = "ca_challenge_op"  # Player can challenge counteraction
    CARD_EXCHANGE = "card_exchange"  # Player making ambassador action can exchange cards
    LOSE_CARD = "lose_card"  # Player losing challenge must lose a card

    def __str__(self):
        return self.value

class GameState():
    """ Represents the current state of a game of Coup """
    num_players: int
    deck: list[Card]
    player_cards: dict[int, list[Card]]
    visible_cards: list[Card]
    player_coins: dict[int, int]
    turn_type: TurnType
    action_taken: Action | None

    def __init__(self, num_players: int = 6) -> None:
        self.num_players = num_players
        self.init()

    def _deal_cards(self) -> None:
        """ Handle deck/player card initialization """
        deck = [Card.DUKE] * 3 + [Card.ASSASSIN] * 3 + [Card.AMBASSADOR] * 3 + [Card.CAPTAIN] * 3 + [Card.CONTESSA] * 3
        shuffle(deck)
        for player in range(self.num_players):
            self.player_cards[player].append(deck.pop())
            self.player_cards[player].append(deck.pop())

    def init(self) -> None:
        """ Initialize the game state """
        self.player_coins = {num: 2 for num in range(self.num_players)}
        self.player_cards = {num: [] for num in range(self.num_players)}
        self.visible_cards = []
        self._deal_cards()
        self.turn_type = TurnType.ACTION
        self.action_taken = None

    def _next_player(self, player_num: int) -> int:
        """ Return the next player number """
        return (player_num + 1) % self.num_players

    def game_over(self) -> bool:
        """ Return True if the game is over """
        return any(len(cards) == 0 for cards in self.player_cards.values())

    def play(self) -> Generator[int]:
        """ Play the game """
        current_player = 0
        while not self.game_over():
            # STEP 1: ACTION
            self.turn_type = TurnType.ACTION
            action = yield current_player
            assert isinstance(action, Action)
            self.action_taken = action

            # STEP 2: CHALLENGE
            if is_challengeable_action(action.type):
                if self.turn_type == TurnType.CHALLENGE_OP:
                    successful_challenge = False
                    for challenge_player in [num % self.num_players for num in range(current_player + 1, self.num_players + current_player + 1)]:
                        challenge = yield challenge_player
                        assert isinstance(challenge, bool)
                        if challenge:
                            challenge_successful = not is_honest_action(action.type, self.player_cards[current_player])
                            self.turn_type = TurnType.LOSE_CARD
                            if challenge_successful:
                                successful_challenge = True
                                lost_card = yield current_player
                                self.player_cards[current_player].remove(lost_card)
                                self.visible_cards.append(lost_card)
                            else:
                                lost_card = yield challenge_player
                                self.player_cards[challenge_player].remove(lost_card)
                                self.visible_cards.append(lost_card)
                            break
                    if successful_challenge:
                        continue

            # STEP 3: COUNTERACTION
            if is_blockable_action(action.type):
                self.turn_type = TurnType.COUNTERACTION_OP
                successful_block = False
                for block_player in [num % self.num_players for num in range(current_player + 1, self.num_players + current_player + 1)]:
                    block = yield block_player
                    if block:
                        self.turn_type = TurnType.CA_CHALLENGE_OP
                        # STEP 3a: CA CHALLENGE
                        challenge = yield current_player
                        if challenge:
                            challenge_successful = not is_honest_counteraction(action.type, self.player_cards[current_player])
                            self.turn_type = TurnType.LOSE_CARD
                            if challenge_successful:
                                lost_card = yield block_player
                                self.player_cards[block_player].remove(lost_card)
                                self.visible_cards.append(lost_card)
                            else:
                                successful_block = True
                                lost_card = yield current_player
                                self.player_cards[current_player].remove(lost_card)
                                self.visible_cards.append(lost_card)
                        break
                if successful_block:
                    continue

            # STEP 4: COMPLETE ACTION
            if action.type == ActionType.INCOME:
                self.player_coins[current_player] += 1

            elif action.type == ActionType.FOREIGN_AID:
                self.player_coins[current_player] += 2

            elif action.type == ActionType.COUP:
                self.player_coins[current_player] -= 7
                self.turn_type = TurnType.LOSE_CARD
                lost_card = yield action.target_player
                self.player_cards[action.target_player].remove(lost_card)
                self.visible_cards.append(lost_card)

            elif action.type == ActionType.TAX:
                self.player_coins[current_player] += 3

            elif action.type == ActionType.ASSASSINATE:
                self.player_coins[current_player] -= 3
                self.turn_type = TurnType.LOSE_CARD
                lost_card = yield action.target_player
                self.player_cards[action.target_player].remove(lost_card)
                self.visible_cards.append(lost_card)

            elif action.type == ActionType.EXCHANGE:
                self.turn_type = TurnType.CARD_EXCHANGE
                new_cards = yield current_player
                self.player_cards[current_player] = new_cards

            elif action.type == ActionType.STEAL:
                self.player_coins[current_player] += 2
                self.player_coins[action.target_player] -= 2

            current_player = self._next_player(current_player)

