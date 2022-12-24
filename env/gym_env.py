import gymnasium as gym

from .state import GameState
from .action import decode_action

class Observation():
    pass

class CoupGymEnv(gym.Env):
    state: GameState
    action_space: gym.spaces.Discrete
    observation_space: gym.spaces.Discrete


    def __init__(self, num_players: int = 6) -> None:
        self.state = GameState(num_players)
        self.action_space = gym.spaces.Discrete()  # TODO: length
        self.observation_space = gym.spaces.Discrete()  # TODO: length

    def reset(self) -> Observation:
        self.state.init()
        return self.observation()

    def step(self, action_code) -> tuple[Observation, int, bool, dict]:
        """ Take an action and return the new state, reward, done, and info """
        action = decode_action(action_code)
        if self.state.turn_type == TurnType.ACTION:
            self.state.handle_action(action)
        elif self.state.turn_type == TurnType.CHALLENGE_OP:
            pass
        self.state.handle_action(action)
        return self.observation(), self.reward(), self.done(), {}


    def observation(self) -> Observation:
        """ 
        Return an observation used by gym.env
        Encodes all state variables
        """
        # one-hot encode state type
        raise NotImplementedError()
    
    def action_mask(self) -> list[bool]:
        """ Return a mask of valid actions """
        raise NotImplementedError()
