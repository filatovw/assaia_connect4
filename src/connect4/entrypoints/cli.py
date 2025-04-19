import sys
from connect4.config import get_config
from connect4.logger import get_logger
from connect4.app import App
from connect4 import ui


def main():
    config = get_config()
    logger = get_logger("CONNECT4", config.app.log_level)
    user_interface = ui.CLI(logger, sys.stdin, sys.stdout)

    # CLI limitations
    if user_interface.get_players_limit() < config.game.players_number:
        raise ValueError(
            "The number of players cannot exceed {}", user_interface.get_players_limit()
        )

    app = App(logger, config, user_interface)
    try:
        app.run()
    except KeyboardInterrupt:
        logger.info("Game was interrupted by the User")


if __name__ == "__main__":
    main()
