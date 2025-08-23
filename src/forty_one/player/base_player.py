"""
Define an abstract base player class for all type of player down the line
"""

from abc import ABC, abstractmethod

from forty_one.game_state import VisibleGameState
from forty_one.action import Action


class BasePlayer(ABC):
    def __init__(self, name: str = "Player"):
        self.name = name

    @abstractmethod
    def choose_action(self, game_state: VisibleGameState) -> Action:
        """
        Define an internal logic of decision making from the player

        Args:
            game_state: a visiable game state from the player perspective

        Return:
            Action: either a player choose to take a card from deck or player's discard
        """
        raise NotImplementedError(
            f"Class '{self.__class__.__name__}' must implement the 'choose_action' method"
        )

    @abstractmethod
    def discard_card(self, game_state: VisibleGameState):
        """
        Define an interna logic of decision making from the player
        """
        raise NotImplementedError(
            f"Class {self.__class__.__name__} must implement the 'discard_card' method"
        )
