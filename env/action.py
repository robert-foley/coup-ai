from enum import Enum

from .card import Card

class ActionType(Enum):
    """ Represents the type of action a player can take """
    INCOME = "income"
    FOREIGN_AID = "foreign_aid"
    COUP = "coup"
    TAX = "tax"
    ASSASSINATE = "assassinate"
    EXCHANGE = "exchange"
    STEAL = "steal"

    def __str__(self):
        return self.value

class Action():
    """ Represents an action taken by a player and the possible target player """
    type: ActionType
    target_player: int | None

    def __init__(self, action_type: ActionType, target_player: int | None = None):
        self.type = action_type
        self.target_player = target_player

    def __str__(self):
        if self.target_player is None:
            return f"{self.type}"
        return f"{self.type} -> player {self.target_player}"

def decode_action(action_code: int) -> Action:
    raise NotImplementedError()
    pass

def is_honest_action(action_type: ActionType, player_cards: list[Card]) -> bool:
    """ Return whether the action is valid """
    if action_type == ActionType.INCOME:
        return True
    elif action_type == ActionType.FOREIGN_AID:
        return True
    elif action_type == ActionType.COUP:
        return True
    elif action_type == ActionType.TAX:
        return Card.DUKE in player_cards
    elif action_type == ActionType.ASSASSINATE:
        return Card.ASSASSIN in player_cards
    elif action_type == ActionType.EXCHANGE:
        return Card.AMBASSADOR in player_cards
    elif action_type == ActionType.STEAL:
        return Card.CAPTAIN in player_cards
    elif action_type == ActionType.ASSASSINATE:
        return Card.ASSASSIN in player_cards
    else:
        raise ValueError(f"Unknown action type: {action_type}")

def is_blockable_action(action_type: ActionType) -> bool:
    """ Return whether the action can be blocked """
    return action_type in {ActionType.FOREIGN_AID, ActionType.ASSASSINATE, ActionType.STEAL}

def is_honest_counteraction(action_type: ActionType, player_cards: list[Card]) -> bool:
    assert is_blockable_action(action_type)
    if action_type == ActionType.FOREIGN_AID:
        return Card.DUKE in player_cards
    elif action_type == ActionType.ASSASSINATE:
        return Card.CONTESSA in player_cards
    elif action_type == ActionType.STEAL:
        return Card.CAPTAIN in player_cards
    else:
        raise ValueError(f"Invalid action type: {action_type}")

def is_challengeable_action(action_type) -> bool:
    """ Return whether the action can be challenged """
    return action_type in {ActionType.TAX, ActionType.ASSASSINATE, ActionType.EXCHANGE, ActionType.STEAL}

