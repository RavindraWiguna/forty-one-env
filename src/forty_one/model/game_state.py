from forty_one.card import Card, Hand
from dataclasses import dataclass


@dataclass(frozen=True)
class VisibleGameState:
    """
    Define a visible game state relative to a player such as:

    - Players hand ( 0 being ourself, 1,2,3 etc being next player up until -1 guy)
    for other player use unknown with real value if like we saw it via discard and keep track
    - Current state of each players garbage [previous garbage, your garbage, next player and so on]
    - Total card in deck left
    - possible deck card ( all unseen card )
    Note:
    - Possible deck card maybe more than total card in deck because it include unseen card that is on other player hand
    - It should consist of 52 Cards - seen card by the player
    """

    player_hands: list[Hand]
    player_discards: list[list[Card]]
    total_card_in_deck: int
    possible_deck_card: set[Card]

    def __repr__(self):
        lines = ["<VisibleGameState>"]

        # Player hands
        lines.append("  Hands:")
        for i, hand in enumerate(self.player_hands):
            lines.append(f"    Player {i}: {hand}")

        # Discards
        lines.append("  Discards:")
        for i, discards in enumerate(self.player_discards):
            lines.append(f"    Player {i-1:2d}: {discards}")

        # Deck info
        lines.append(f"  Total cards left in deck: {self.total_card_in_deck}")

        # Possible deck (sorted by rank+suit for readability)
        sorted_deck = sorted(
            self.possible_deck_card,
            key=lambda c: (
                c.rank.value[0] if not c.is_unknown else 0,
                str(c.suit) if c.suit else "",
            ),
        )
        lines.append(f"  Possible deck ({len(sorted_deck)} cards):")
        # chunk into rows of ~13 for readability
        chunk_size = 13
        for i in range(0, len(sorted_deck), chunk_size):
            lines.append(
                "    " + " ".join(str(c) for c in sorted_deck[i : i + chunk_size])
            )

        return "\n".join(lines)
