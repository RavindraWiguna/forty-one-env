"""
Define a card deck class, to organize 52 Cards
"""

from forty_one.card import Card, CardRank, CardSuit

from copy import deepcopy
import random


class CardDeck:
    """
    Class to organize 52 cards into a deck with built in function to shuffle and deal cards
    """

    def __init__(self):
        self._unshuffled_card = [
            Card(rank, suit) for rank in CardRank for suit in CardSuit
        ]
        self.reset()

    def get_copy_unshuffled_card(self):
        return deepcopy(self._unshuffled_card)

    def reset(self):
        """
        Reset the deck into ordered 52 cards
        """
        self.cards = self.get_copy_unshuffled_card()

    def shuffle(self):
        """
        Shuffle a deck of card in place
        """
        random.shuffle(self.cards)

    def deal(self, n: int = 1) -> list[Card]:
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
    deck = CardDeck()
    print("Total cards:", len(deck))
    print("Shuffling deck...")
    deck.shuffle()
    print("Dealing first 4 card")
    four_cards = deck.deal(4)
    print(four_cards)
