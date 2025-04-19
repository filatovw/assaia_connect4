import logging
from connect4.models import GameConfig
from dataclasses import dataclass


class GameEngineError(Exception):
    pass


class GameEngineNextPlayerError(GameEngineError):
    pass


class GameEngineWrongColumnValueError(GameEngineError):
    pass


class GameEngineWrongColumnNumberError(GameEngineError):
    pass


class GameEngineArenaIsFullError(GameEngineError):
    pass


@dataclass
class Player:
    number: int
    title: str


class Game:
    STATE_EMPTY = -1

    def __init__(self, logger: logging.Logger, config: GameConfig) -> None:
        self._logger = logger
        self._config = config
        self._players = self._init_players(config.players_number)
        self._current_player = self._players[0]
        self._arena = self._init_arena(config.width, config.height)

    def _init_players(self, players_number: int) -> list[Player]:
        players = []
        for player_id in range(1, players_number + 1):
            players.append(
                Player(
                    number=player_id,
                    title=f"player_{player_id}",
                )
            )
        return players

    def get_current_player(self) -> Player:
        return self._current_player

    def get_next_player(self) -> Player:
        next_id = self._current_player.number + 1
        if next_id > len(self._players):
            self._current_player = self._players[0]
            return self._players[0]

        for player in self._players:
            if player.number == next_id:
                self._current_player = player
                return player
        raise GameEngineNextPlayerError("Could not find the next player")

    def _init_arena(self, rows: int, columns: int) -> list[list[int]]:
        return [[self.STATE_EMPTY] * columns for _ in range(rows)]

    def get_arena(self) -> list[list[int]]:
        return self._arena

    def step(self, player: Player, column: int):
        max_columns = len(self._arena[0])
        max_rows = len(self._arena)
        if column < 0 or column > max_columns - 1:
            raise GameEngineWrongColumnNumberError("Wrong column number")

        last_empty_row = -1
        for i in range(max_rows):
            if self._arena[i][column] == self.STATE_EMPTY:
                last_empty_row = i
            else:
                break
        if last_empty_row < 0:
            raise GameEngineWrongColumnValueError(f"Column {column} is full already")
        self._arena[last_empty_row][column] = player.number

    def is_arena_filled(self) -> bool:
        for i in range(len(self._arena)):
            for j in range(len(self._arena[i])):
                if self._arena[i][j] == self.STATE_EMPTY:
                    return False
        return True

    def get_winner(self) -> Player | None:
        return None
