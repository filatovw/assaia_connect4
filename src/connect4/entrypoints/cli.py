import sys
from connect4.config import get_config
from connect4.logger import get_logger
from connect4.app import App


def main():
    config = get_config()
    logger = get_logger("CONNECT4", config.app.log_level)
    app = App(logger, config, sys.stdin, sys.stdout)
    try:
        app.run()
    except KeyboardInterrupt:
        logger.info("Game was interrupted by the User")


if __name__ == "__main__":
    main()
