import logging
from connect4 import models
from connect4 import ui


class App:
    def __init__(
        self,
        logger: logging.Logger,
        config: models.Config,
        user_interface: ui.AbstractUI,
    ) -> None:
        self._logger = logger
        self._config = config
        self._ui = user_interface

    def run(self):
        self._ui.show_intro()
        while True:
            player_id = 1
            self._ui.print_active_player(player_id)
            value = self._ui.read_line()
            self._logger.info("VAL: %s", value)
            if value == "":
                self._ui.print_wrong_input("Value cannot be empty")
                value = self._ui.read_line()

            state = [
                [" ", "+", "#", " ", " "],
                [" ", "+", "#", " ", " "],
                [" ", "+", "#", "#", " "],
                [" ", " ", "#", "#", " "],
                [" ", " ", "#", "#", " "],
            ]
            self._ui.print_state(state)
            self._ui.print_winner(player_id)
