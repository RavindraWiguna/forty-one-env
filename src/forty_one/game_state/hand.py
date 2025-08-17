from forty_one import Card, CardSuit


class Hand:
    def __init__(self, cards: list[Card]):
        self.cards = cards

    def add(self, card: Card):
        """
        Add a single card to current hand
        """
        Card.ensure_a_card_class(card)

        self.cards.append(card)

    def remove_by_index(self, index: int):
        """
        Delete a card from hand via its index
        """
        if not isinstance(index, int) or index < 0 or index > len(self.cards):
            raise ValueError(
                "index must be a number within range 0 and length of cards"
            )

        self.cards.pop(index)

    def remove_by_value(self, card: Card):
        """
        Delete a card from hand via card class
        """
        Card.ensure_a_card_class(card)

        self.cards.remove(card)

    def count_points(self) -> int:
        """
        Compute total points based on 41 rules:
        - Score is the maximum suit-sum
        - Minus the value of all cards not in that suit
        """
        sums = {suit: 0 for suit in CardSuit}
        for card in self.cards:
            sums[card.suit] += card.get_value()

        max_suit_sum = max(sums.values())
        total = sum(sums.values())
        # read: max_suite_sum - value_of_other_suit , where value_other_suit = total - max_suite_sum
        return 2 * max_suit_sum - total
