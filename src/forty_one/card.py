"""
Define a card model for 41 game

Including a card suit, rank, and deck of card
"""
import copy
from enum import Enum
import random

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
                return 'A'
            case CardRank.JACK:
                return 'J'
            case CardRank.QUEEN:
                return 'Q'
            case CardRank.KING:
                return 'K'
            case _:
                return str(self.value[0])

class Card:
    """
    Card object in the game, consist of rank, and suite
    """
    def __init__(self, rank: CardRank, suit: CardSuit):
        self.rank = rank
        self.suit = suit
    
    def __str__(self):
        return f'{self.rank}{self.suit}'

    def __repr__(self):
        return self.__str__()


class CardDeck:
    """
    Class to organize 52 cards into a deck with built in function to shuffle and deal cards
    """
    def __init__(self):
        self._unshuffled_card = [Card(rank, suit) for rank in CardRank for suit in CardSuit]
        self.reset()
    
    def reset(self):
        """
        Reset the deck into ordered 52 cards
        """
        self.cards = copy.deepcopy(self._unshuffled_card)

    def shuffle(self):
        """
        Shuffle a deck of card in place
        """
        random.shuffle(self.cards)
    
    def deal(self, n:int =1) -> list[Card]:
        """
        Deal N number of card from the deck
        """
        if not isinstance(n, int) or n < 1:
            raise ValueError("n must be a positive integer")
        if n > len(self.cards):
            raise ValueError(f"Cannot deal {n} cards, only {len(self.cards)} remaining")
        

        dealt, self.cards = self.cards[:n], self.cards[n:]
        return dealt

    def draw(self) -> Card:
        """
        Deal a single card
        """
        return self.deal(1)[0]

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return ", ".join(str(c) for c in self.cards)



if __name__ == "__main__":
    print('Demo Card Module')
    card_rank_ace = CardRank.ACE
    card_rank_ten = CardRank.TEN
    card_suit_club = CardSuit.CLUBS

    card_1 = Card(card_rank_ace, card_suit_club)
    card_2 = Card(card_rank_ten, card_suit_club)
    print(card_1, str(card_1)=='A♣')
    print(card_2, str(card_2)=='10♣')

    deck = CardDeck()
    print('Total cards:', len(deck))
    print('Shuffling deck...')
    deck.shuffle()
    print('Dealing first 4 card')
    four_cards = deck.deal(4)
    print(four_cards)
