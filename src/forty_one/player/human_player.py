from forty_one.model import VisibleGameState
from forty_one.action import Action
from forty_one.player import BasePlayer
from collections.abc import Callable


class HumanPlayer(BasePlayer):
    def __init__(self, name="HumanPlayer"):
        super().__init__(name)

    def print_game_state(self, game_state: VisibleGameState):
        print(game_state)

    def get_human_input(self, func: Callable):
        notValid = True
        human_input = None
        while notValid:
            try:
                human_input = func()
                notValid = False
            except Exception as e:
                print(e)
                print("Try again...")

        return human_input

    def choose_action(self, game_state: VisibleGameState):
        self.print_game_state(game_state)
        valid_action = [Action.TAKE_FROM_DECK]
        if game_state.player_discards[0]:
            valid_action.append(Action.TAKE_FROM_DISCARD)
        act_dx = None

        def get_valid_action():
            print("Choose one of these action")
            print(valid_action)
            my_dx = int(input("Input index of the action to take (1-indexed):"))
            _ = valid_action[my_dx - 1]
            return my_dx - 1

        act_dx = self.get_human_input(get_valid_action)
        return valid_action[act_dx]

    def discard_card(self, game_state: VisibleGameState):
        self.print_game_state(game_state)

        def get_idx():
            idx = int(input("What index to discard? (1-indexed):"))
            _ = game_state.player_hands[0].card_at(idx - 1)
            return idx - 1

        idx_to_discard = self.get_human_input(get_idx)
        return idx_to_discard
