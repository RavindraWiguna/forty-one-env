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

        def get_valid_action():
            print("Choose one of these action")
            print(valid_action)
            act_idx = int(input("Input index of the action to take:"))
            if act_idx > len(valid_action):
                raise ValueError(
                    "Not a valid index, must be within length of valid action"
                )

            return act_idx

        act_dx = self.get_human_input(get_valid_action)
        return valid_action[act_dx]

    def discard_card(self, game_state: VisibleGameState):
        self.print_game_state(game_state)

        def get_idx():
            idx = int(input("What index to discard? (0 indexed):"))
            return idx

        idx_to_discard = self.get_human_input(get_idx)
        return idx_to_discard
