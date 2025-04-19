import typing as t
import logging

from abc import ABC


class AbstractUI(ABC):
    def show_intro(self) -> None:
        raise NotImplementedError

    def print_active_player(self, player_id: int) -> None:
        raise NotImplementedError

    def get_column(self) -> int:
        raise NotImplementedError

    def print_state(self, state: list[list[str]]) -> None:
        raise NotImplementedError

    def print_winner(self, player_id: int) -> None:
        raise NotImplementedError

    def print_wrong_input(self, message: str) -> None:
        raise NotImplementedError

    def print_error(self, message: str) -> None:
        raise NotImplementedError


class CLI(AbstractUI):
    MARKS = ["X", "O", "+", "*", "#", "@"]
    EMPTY_RUNE = " "
    UPPER_BOUNDARY_RUNE = "\u005f"
    BOTTOM_BOUNDARY_RUNE = "\u203e"
    VERTICAL_BOUDNARY_RUNE = "|"

    @classmethod
    def get_players_limit(cls) -> int:
        return len(cls.MARKS)

    def __init__(
        self,
        logger: logging.Logger,
        input_stream: t.TextIO,
        output_stream: t.TextIO,
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

    def get_column(self) -> int:
        while True:
            try:
                return int(self._read_user_prompt())
            except TypeError:
                self.print_wrong_input("Incorrect column number. Try again!")
            except ValueError:
                self.print_wrong_input("Incorrect column value. Try again!")

    def print_state(self, state: list[list[int]]):
        top_horizontal_line = self.UPPER_BOUNDARY_RUNE * (len(state[0]) * 2 + 1)
        bottom_horizontal_line = self.BOTTOM_BOUNDARY_RUNE * (len(state[0]) * 2 + 1)

        for yidx, line in enumerate(state):
            if yidx == 0:
                self._write(top_horizontal_line)
            fmt_line = ""
            for xidx, player_number in enumerate(line):
                if xidx == 0:
                    fmt_line += self.VERTICAL_BOUDNARY_RUNE

                if player_number < 0:
                    rune = self.EMPTY_RUNE
                else:
                    rune = self.MARKS[player_number]

                fmt_line += rune + self.VERTICAL_BOUDNARY_RUNE

            self._write(fmt_line)
            if yidx == len(state) - 1:
                self._write(bottom_horizontal_line)

    def print_winner(self, player_id: int) -> None:
        self._write(f"Winner is Player {player_id}")

    def print_wrong_input(self, message: str) -> None:
        self._write(f"Incorrect input: {message}")

    def print_error(self, message: str) -> None:
        self._write(f"Error: {message}")
