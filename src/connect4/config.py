import logging
import math
import argparse
from connect4 import models


def get_config() -> models.Config:
    parser = argparse.ArgumentParser()
    ref_players_number_field = parser.add_argument(
        "--players-number",
        "-n",
        type=int,
        default=2,
        help="Number of players",
    )
    ref_width = parser.add_argument(
        "--width", type=int, default=6, help="Width of the arena"
    )
    ref_height = parser.add_argument(
        "--height", type=int, default=7, help="Height of the arena"
    )
    ref_sequence_length = parser.add_argument(
        "--sequence-length",
        "-s",
        type=int,
        default=4,
        help="Length of a continuous sequence to win",
    )
    parser.add_argument(
        "--log-level",
        "-l",
        type=str,
        default=logging.getLevelName(logging.INFO),
        help="Application log level",
    )

    parsed = parser.parse_args()
    if parsed.players_number < 2:
        raise argparse.ArgumentError(
            ref_players_number_field, "Too few players for a game to start"
        )

    if parsed.width < 3:
        raise argparse.ArgumentError(ref_width, "Arena should be wider")

    if parsed.height < 3:
        raise argparse.ArgumentError(ref_height, "Arena should be higher")

    if parsed.sequence_length < 1:
        raise argparse.ArgumentError(
            ref_sequence_length, "Sequence length should be bigger"
        )

    if parsed.sequence_length > math.sqrt(parsed.width**2 + parsed.height**2):
        raise argparse.ArgumentError(
            ref_sequence_length, "There is no chance to achieve such a sequence"
        )

    game_config = models.GameConfig(
        players_number=parsed.players_number,
        width=parsed.width,
        height=parsed.height,
        sequence_length=parsed.sequence_length,
    )
    app_config = models.AppConfig(
        log_level=parsed.log_level,
    )
    return models.Config(
        game=game_config,
        app=app_config,
    )
