import typing as t
import logging
from connect4 import models


class App:
    def __init__(
        self,
        logger: logging.Logger,
        config: models.Config,
        input_stream: t.TextIO,
        output_stream: t.TextIO,
    ) -> None:
        self._logger = logger
        self._config = config
        self._ui = UI(logger, input_stream, output_stream)

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

            state = [[1, 0, 0], [0, 1, 1]]
            self._ui.print_state(state)

            self._ui.print_winner(player_id)


class UI:
    def __init__(
        self, logger: logging.Logger, input_stream: t.TextIO, output_stream: t.TextIO
    ) -> None:
        self._logger = logger
        self._sin = input_stream
        self._sout = output_stream

    def _write(self, message: str) -> None:
        self._sout.write(message + "\n")

    def _read_user_prompt(self) -> str:
        self._sout.write("-->\n")
        value = self._sin.readline()
        return value.replace("\n", " ").strip(" ")

    def show_intro(self) -> None:
        self._write("Hello, Gamers!")

    def print_active_player(self, player_id: int) -> None:
        self._write(f"Player {player_id}")

    def read_line(self) -> str:
        return self._read_user_prompt()

    def print_state(self, state: t.Any):
        self._write(str(state))

    def print_winner(self, player_id: int) -> None:
        self._write(f"Winner is Player {player_id}")

    def print_wrong_input(self, message: str) -> None:
        self._write(f"Incorrect input: {message}")

    def print_error(self, message: str) -> None:
        self._write(f"Error: {message}")
