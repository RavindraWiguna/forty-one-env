from dataclasses import dataclass


@dataclass
class PlayerIdentifier:
    index: int
    name: str


@dataclass
class ScoreData:
    player_id: PlayerIdentifier
    score: int


@dataclass
class GameResult:
    """
    Consist of:
    - sorted scores -> list of tuple with PlayerIdentifier and their score
    - reached_target_score -> list of PlayerIdentifier that reach the target score
    """

    sorted_scores: list[ScoreData]
    reached_target_score: list[PlayerIdentifier]
