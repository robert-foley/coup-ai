from .state import GameState

def print_game(state: GameState):
    """ Print the current game state """
    for player in range(state.num_players):
        print(f"Player {player}:\n\tCards: {state.player_cards[player]}\n\tCoins: {state.player_coins[player]}")

    print(f"Visible Cards: {state.visible_cards}")
    print(f"Turn Type: {state.turn_type}")
    print(f"Action Taken: {state.action_taken}")
    