from forty_one.card import Card, CardDeck, Hand
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
    possible_deck_card: list[Card]


@dataclass
class FullGameState:
    """
    Game state of the whole game

    All card is revealed ( no hidden one )
    It has:
    - Hand of each player
    - Current state of player discard
    - Current state of the dect
    - dictionary consist of set of seen card by players
    """

    player_hands: list[Hand]
    player_discards: list[list[Card]]
    deck: CardDeck
    seen_cards: dict[str, set[Card]]
