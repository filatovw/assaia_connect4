import logging
from connect4 import models
from connect4 import ui
from connect4 import engine


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
        self._engine = engine.Game(logger, config.game)

    def run(self):
        self._ui.show_intro()
        player = self._engine.get_current_player()
        while not self._engine.is_arena_filled():
            self._ui.print_active_player(player.number)

            while True:
                try:
                    column = self._ui.get_column()
                    self._engine.step(player, column)
                    break
                except (
                    engine.GameEngineWrongColumnValueError,
                    engine.GameEngineWrongColumnNumberError,
                ) as err:
                    self._ui.print_wrong_input(str(err))

            state = self._engine.get_arena()
            self._ui.print_state(state)
            winner = self._engine.get_winner()
            if winner:
                self._ui.print_winner(winner.number)
            else:
                player = self._engine.get_next_player()
