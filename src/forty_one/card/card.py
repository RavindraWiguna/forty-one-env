"""
Define a card model for 41 game

Including a card suit, rank, and deck of card
"""

from enum import Enum
from typing import Any


class CardSuit(Enum):
    """
    Define type of card suit in 41 game
    """

    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

    def __str__(self):
        return self.value


class CardRank(Enum):
    """
    Define card rank ( rank, value ) in 41 game
    """

    TWO = (2, 2)
    THREE = (3, 3)
    FOUR = (4, 4)
    FIVE = (5, 5)
    SIX = (6, 6)
    SEVEN = (7, 7)
    EIGHT = (8, 8)
    NINE = (9, 9)
    TEN = (10, 10)
    JACK = (11, 10)
    QUEEN = (12, 10)
    KING = (13, 10)
    ACE = (14, 11)

    def __str__(self):
        match self:
            case CardRank.ACE:
                return "A"
            case CardRank.JACK:
                return "J"
            case CardRank.QUEEN:
                return "Q"
            case CardRank.KING:
                return "K"
            case _:
                return str(self.value[0])


class Card:
    """
    Card object in the game, consist of rank, and suite
    """

    CARD_VALUE_INDEX = 1

    def __init__(self, rank: CardRank | None, suit: CardSuit | None):
        self.rank = rank
        self.suit = suit
        self.is_unknown = True if rank is None or suit is None else False
        self.is_seen_by_all_player = False  # denote if a card ever discarded to garbage

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return self.__str__()

    def get_value(self):
        """
        return a card value based on 41 game rule
        Note:
            - Unknown card is returned with 0
        """
        if self.is_unknown:
            return 0
        return self.rank.value[self.CARD_VALUE_INDEX]

    @staticmethod
    def ensure_a_card_class(obj: Any):
        if not isinstance(obj, Card):
            raise ValueError(f"{obj} is not a type of Card class")

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.suit, self.rank))


# singleton unknown card
class UnknownCard(Card):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        object.__setattr__(self, "rank", None)
        object.__setattr__(self, "suit", None)
        object.__setattr__(self, "_initialized", True)
        object.__setattr__(self, "is_unknown", True)

    def __setattr__(self, key, value):
        raise AttributeError("UnknownCard is immutable and cannot be modified")

    def __str__(self):
        return "??"


UNKNOWN_CARD = UnknownCard()


if __name__ == "__main__":
    print("Demo Card Module")
    card_rank_ace = CardRank.ACE
    card_rank_ten = CardRank.TEN
    card_suit_club = CardSuit.CLUBS

    card_1 = Card(card_rank_ace, card_suit_club)
    card_2 = Card(card_rank_ten, card_suit_club)
    print(card_1, str(card_1) == "A♣")
    print(card_2, str(card_2) == "10♣")
