from forty_one.model import VisibleGameState
from forty_one.action import Action
from forty_one.player import BasePlayer
from forty_one.card import Hand
from copy import deepcopy


class SimpleHeuristicPlayer(BasePlayer):
    def __init__(self, name="SimpleHeuristic"):
        super().__init__(name)

    def _simple_discard_logic(self, hand: Hand):
        max_score = -1
        idx_to_discard = 0
        cards = hand.get_copy_cards()
        for i, card in enumerate(cards):
            # discard it first
            hand.discard(card)

            score_after_discard = hand.calculate_score()
            if score_after_discard > max_score:
                idx_to_discard = i
                max_score = score_after_discard

            # add it again
            hand.add(card)

        return idx_to_discard, max_score

    def choose_action(self, game_state: VisibleGameState):
        sum_take_from_possible_deck_score = 0
        mutable_hand = deepcopy(game_state.player_hands[0])
        for card in game_state.possible_deck_card:
            # add card to hand
            mutable_hand.add(card)
            _, max_score = self._simple_discard_logic(mutable_hand)
            sum_take_from_possible_deck_score += max_score
            mutable_hand.discard(card)

        avg_take_from_possible_deck = sum_take_from_possible_deck_score / len(
            game_state.possible_deck_card
        )
        max_score_if_take_discard = -1
        if game_state.player_discards[0]:
            mutable_hand.add(game_state.player_discards[0][0])
            _, max_score_if_take_discard = self._simple_discard_logic(mutable_hand)

        if avg_take_from_possible_deck > max_score_if_take_discard:
            return Action.TAKE_FROM_DECK

        return Action.TAKE_FROM_DISCARD

    def discard_card(self, game_state: VisibleGameState):
        mutable_hand = deepcopy(game_state.player_hands[0])
        idx_to_discard, _ = self._simple_discard_logic(mutable_hand)
        return idx_to_discard
