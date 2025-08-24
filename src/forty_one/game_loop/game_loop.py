from forty_one.player import BasePlayer
from forty_one.card import CardDeck, Hand, UNKNOWN_CARD, Card
from forty_one.model import VisibleGameState, GameResult, PlayerIdentifier, ScoreData
from forty_one.action import Action
import random


class GameLoop:
    CARD_PER_PLAYER = 4
    TARGET_SCORE = 41

    def __init__(self, players: list[BasePlayer]):
        self.deck = CardDeck()
        max_player = len(self.deck) // self.CARD_PER_PLAYER
        assert len(players) <= max_player

        self.players = players
        self.total_player = len(self.players)
        self.ordered_deck = set(self.deck.get_copy_unshuffled_card())
        self.player_hands = []
        self.player_discards = []
        self.seen_cards: list[set[Card]] = []

    def _restart_game(self):
        self.deck.reset()
        self.deck.shuffle()

        self.player_hands = self._init_player_hands()

        self.player_discards = []
        self.seen_cards = []

    def _init_player_hands(self) -> list[Hand]:
        hands = []
        for _ in self.players:
            cards = self.deck.deal(self.CARD_PER_PLAYER)
            hands.append(Hand(cards=cards))

        return hands

    def _obscure_player_hand(self, curr_player_idx: int, tgt_player_idx: int) -> Hand:
        """
        Obscure a player hand based on the knowledge of current player
        """
        tgt_hand = self.player_hands[tgt_player_idx]
        obscured_hand = [UNKNOWN_CARD for _ in range(len(tgt_hand))]
        for i, card in enumerate(tgt_hand):
            if card in self.seen_cards[curr_player_idx]:
                obscured_hand[i] = card

        # shuffle so that player can't infer what's the hand by comparing previous turn and current turn
        random.shuffle(obscured_hand)
        return Hand(cards=obscured_hand)

    def _rotate_list(self, list_to_rotate: list, start_idx: int) -> list:
        return list_to_rotate[start_idx:] + list_to_rotate[:start_idx]

    def _get_possible_deck_card(self, curr_player_idx: int) -> set[Card]:
        possible_deck_card = self.ordered_deck - self.seen_cards[curr_player_idx]
        return possible_deck_card

    def _create_visible_game_state(self, curr_player_idx: int) -> VisibleGameState:
        visible_hands = []
        for i in range(self.total_player):
            if i == curr_player_idx:
                continue

            obscured_hand = self._obscure_player_hand(curr_player_idx, i)
            visible_hands.append(obscured_hand)

        prev_player_idex = curr_player_idx - 1

        visible_hands = self._rotate_list(visible_hands, curr_player_idx)
        ordered_discard = self._rotate_list(self.player_discards, prev_player_idex)
        possible_deck_card = self._get_possible_deck_card(curr_player_idx)

        visible_game_state = VisibleGameState(
            player_hands=visible_hands,
            player_discards=ordered_discard,
            total_card_in_deck=len(self.deck),
            possible_deck_card=possible_deck_card,
        )
        return visible_game_state

    def _prev_player_has_discard(self, curr_player_idx: int) -> bool:
        return bool(self.player_discards[curr_player_idx - 1])

    def _print_player_move(self, curr_player_idx: int, player_name: str, message: str):
        print(f"Player #{curr_player_idx}:{player_name} {message}")

    def _mark_card_as_seen(self, card: Card):
        for i in range(self.total_player):
            self.seen_cards[i].add(card)

    def _check_if_game_ended(self, curr_player_idx: int) -> bool:
        curr_player_score = self.player_hands[curr_player_idx].calculate_score()
        if curr_player_score == self.TARGET_SCORE:
            return True

        if len(self.deck) == 0:
            return True

        return False

    def _get_game_result(self) -> GameResult:
        player_scores: list[ScoreData] = []
        reached_target_score: list[PlayerIdentifier] = []
        for i, player_hand in enumerate(self.player_hands):
            player_name = self.players[i].name
            player_identifier = PlayerIdentifier(i, player_name)
            player_score = player_hand.calculate_score()
            score_data = ScoreData(player_identifier, player_score)
            player_scores.append(score_data)

            if player_score == self.TARGET_SCORE:
                reached_target_score.append(player_identifier)
        game_result = GameResult(
            sorted_scores=sorted(player_scores, key=lambda x: x.score),
            reached_target_score=reached_target_score,
        )
        return game_result

    def _celebrate_result(self, game_result: GameResult):
        if game_result.reached_target_score:
            if len(game_result.reached_target_score) > 1:
                print("Wow, we got ourself a multiwinner")

            for player_id in game_result.reached_target_score:
                print(f"Player #{player_id.index}:{player_id.name} WON!")

        else:
            print(f"No one reach the target score of {self.TARGET_SCORE}")
            print("Where is the score of each player sorted")
            for i, score_data in enumerate(game_result.sorted_scores):
                print(
                    f"[{i+1}] #{score_data.player_id.index}:{score_data.player_id.name} [{score_data.score}]"
                )

    def _main_loop(self):
        isPlaying = True
        turn_number = 0
        while isPlaying:
            curr_player_idx = turn_number % self.total_player
            player_ai = self.players[curr_player_idx]

            print(f"[TURN {turn_number}] Player: {player_ai.name} move...")
            player_visible_game_state = self._create_visible_game_state(curr_player_idx)
            player_action = player_ai.choose_action(player_visible_game_state)

            self._print_player_move(
                curr_player_idx, player_ai.name, f"has choosen to {player_action}"
            )

            card_to_add = None
            if player_action == Action.TAKE_FROM_DISCARD:
                if self._prev_player_has_discard(curr_player_idx):
                    card_to_add = self.player_discards.pop(0)
                else:
                    self._print_player_move(
                        curr_player_idx,
                        player_ai.name,
                        "unable to take from discard, taking from deck instead",
                    )

            # player choose to take from deck or unable to take from discard
            if card_to_add is None:
                card_to_add = self.deck.deal(1)

            # add this card to seen card for this player
            self.seen_cards[curr_player_idx].add(card_to_add)
            self.player_hands[curr_player_idx].add(card_to_add)

            # get card to discard from player
            player_visible_game_state = self._create_visible_game_state(curr_player_idx)
            discarded_card_idx = player_ai.discard_card(player_visible_game_state)
            discarded_card = self.player_hands[curr_player_idx].card_at(
                discarded_card_idx
            )

            self._print_player_move(
                curr_player_idx,
                player_ai.name,
                f"has choosen to discard: {discarded_card}",
            )

            self.player_discards[curr_player_idx] = self.player_hands[
                curr_player_idx
            ].discard_at(discarded_card_idx)

            # mark it as seen by all player
            self._mark_card_as_seen(discarded_card)

            # check game ended
            isPlaying = self._check_if_game_ended(curr_player_idx)
            turn_number += 1

    def play(self):
        self._restart_game()
        self._main_loop()
        result = self._get_game_result()
        self._celebrate_result(result)
