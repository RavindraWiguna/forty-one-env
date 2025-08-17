from forty_one import Card, CardSuit


class Hand:
    def __init__(self, cards: list[Card]):
        self._cards = cards

    def add(self, card: Card):
        """
        Add a single card to current hand
        """
        Card.ensure_a_card_class(card)

        self._cards.append(card)

    def card_at(self, index: int):
        """
        get card by its index position
        """
        return self._cards[index]

    def index_of(self, card: Card):
        Card.ensure_a_card_class(card)

        return self._cards.index(card)

    def discard_at(self, index: int):
        """
        Delete a card from hand via its index
        """
        self._cards.pop(index)

    def discard(self, card: Card):
        """
        Delete a card from hand via card class
        """
        Card.ensure_a_card_class(card)

        self._cards.remove(card)

    def calculate_score(self) -> int:
        """
        Compute total points based on 41 rules:
        - Score is the maximum suit-sum
        - Minus the value of all cards not in that suit
        Note:
        - Only count based on the known card
        """
        sums = {suit: 0 for suit in CardSuit}
        for card in self.cards:
            if card.is_unknown:
                continue
            sums[card.suit] += card.get_value()

        max_suit_sum = max(sums.values())
        total = sum(sums.values())
        # read: max_suite_sum - value_of_other_suit , where value_other_suit = total - max_suite_sum
        return 2 * max_suit_sum - total
