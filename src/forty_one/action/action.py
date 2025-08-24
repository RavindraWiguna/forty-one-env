"""
Define Action Enum that a player can choose
"""

from enum import StrEnum, auto


class Action(StrEnum):
    """
    Define an action that a player can take during their turn

    Either:
    1. TAKE_FROM_DECK: Take a card from deck:
    2. TAKE_FROM_DISCARD: Take a card from previous player's discard
    """

    TAKE_FROM_DECK = auto()
    TAKE_FROM_DISCARD = auto()

    def __repr__(self):
        return self.value
