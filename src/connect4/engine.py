import logging
from connect4.models import GameConfig
from dataclasses import dataclass


class GameEngineError(Exception):
    pass


class GameEngineNextPlayerError(GameEngineError):
    pass


class GameEngineNoPlayerError(GameEngineError):
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

    def find_player_by_id(self, player_id: int) -> Player:
        for player in self._players:
            if player.number == player_id:
                return player
        raise GameEngineNoPlayerError("Couldn't find player by id")

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

    def check_direction(self, i: int, j: int, x: int, y: int) -> bool:
        """Check the direction.
        [
            [0, 1, 2, 2],
            [0, 0, 1, 0],
            [0, 0, 2, 0],
            [0, 0, 1, 0],
        ]
        left top corner is the beginning of axis.
        (0, 0)  ---> X (1, 0)
        |
        |
        v
        Y (0, 1)     (1, 1)

        Right direction: (1, 0)
        Down direction: (0, 1)
        Right Down direction (1, 1)
        Left Down direction (-1, 1)

        Args:
            i: starting point X
            j: starting point Y
            x: direction vector X
            y: direction vector Y

        Returns:
            Boolean flag answering the question: Is there a continuous sequence of the same integer values?
        """
        arena = self._arena
        seq_len = self._config.sequence_length
        self._logger.debug(
            "Direction: (%s, %s) to (%s, %s), len: %s",
            i,
            j,
            x,
            y,
            self._config.sequence_length,
        )

        try:
            arena[i + x * seq_len - 1][j + y * seq_len - 1]
        except IndexError as err:
            self._logger.debug("Failed %s", err)
            return False

        last_player_id = None
        for _ in range(seq_len):
            self._logger.info("SEQ NUM %s", i)
            if last_player_id and last_player_id != arena[i][j]:
                # last player is different from the current player in a sequence. Stopping
                return False
            last_player_id = arena[i][j]
            i += x
            j += y
        return True

    def find_winner_id(self) -> int | None:
        max_columns = len(self._arena[0])
        max_rows = len(self._arena)
        winner_id = None
        # iterate over rows
        for i in range(max_rows):
            # iterate over columns
            for j in range(max_columns):
                if self._arena[i][j] == self.STATE_EMPTY:
                    continue
                if (
                    self.check_direction(i, j, 1, 0)
                    or self.check_direction(i, j, 0, 1)
                    or self.check_direction(i, j, 1, 1)
                    or self.check_direction(i, j, -1, 1)
                ):
                    winner_id = self._arena[i][j]
                    break
        return winner_id

    def get_winner(self) -> Player | None:
        """Get Player who won this round

        Returns:
            Player entity if found
        """
        winner_id = self.find_winner_id()
        if winner_id:
            self._logger.info("WinnerID: %s", winner_id)
            return self.find_player_by_id(winner_id)
        return None
