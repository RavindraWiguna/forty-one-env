from forty_one.model import VisibleGameState
from forty_one.action import Action
from forty_one.player import BasePlayer
import random


class RandomPlayer(BasePlayer):
    def __init__(self, name="Player"):
        super().__init__(name)

    def choose_action(self, game_state: VisibleGameState):
        return random.choice([Action.TAKE_FROM_DECK, Action.TAKE_FROM_DISCARD])

    def discard_card(self, game_state: VisibleGameState):
        return random.choice([i for i in range(len(game_state.player_hands[0]))])
