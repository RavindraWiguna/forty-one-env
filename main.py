from forty_one.game_loop import GameLoop
from forty_one.player import SimpleHeuristicPlayer, RandomPlayer, HumanPlayer
import random


def main():
    players = [
        SimpleHeuristicPlayer(),
        RandomPlayer(),
        HumanPlayer(),
        SimpleHeuristicPlayer(),
    ]
    random.shuffle(players)

    game = GameLoop(players=players)

    game.play()


if __name__ == "__main__":
    main()
