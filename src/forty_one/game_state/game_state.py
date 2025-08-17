from .hand import Hand
from forty_one import Card
from dataclasses import dataclass


@dataclass(frozen=True)
class VisibleGameState:
    """
    Define a visible game state relative to a player such as:

    - Players hand ( 0 being ourself, 1,2,3 etc being next player up until -1 guy)
    for other player use unknown with real value if like we saw it via discard and keep track
    - Each players garbage [previous garbage, your garbage, next player and so on]
    - Total card in deck left
    - possible deck card ( all unseen card )
    Note:
    - Possible deck card maybe more than total card in deck because it include unseen card that is on other player hand
    """

    player_hands: list[Hand]
    player_discards: list[list[Card]]
    total_card_in_deck: int
    possible_deck_card: list[Card]
