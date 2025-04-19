import logging
from connect4 import models


class App:
    def __init__(self, logger: logging.Logger, config: models.Config) -> None:
        self._logger = logger
        self._config = config

    def run(self):
        while True:
            pass
