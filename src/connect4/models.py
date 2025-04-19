from dataclasses import dataclass


@dataclass
class GameConfig:
    players_number: int
    width: int
    height: int
    sequence_length: int


@dataclass
class AppConfig:
    log_level: str


@dataclass
class Config:
    game: GameConfig
    app: AppConfig
