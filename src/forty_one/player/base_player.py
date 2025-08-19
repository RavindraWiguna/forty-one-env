"""
Define an abstract base player class for all type of player down the line
"""

from abc import ABC, abstractmethod
from typing import Any


class BasePlayer(ABC):
    def __init__(self, name: str = "Player"):
        self.name = name

    @abstractmethod
    def choose_action(self, game_state: Any):
        pass
