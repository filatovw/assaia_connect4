# Connect4

## Задача:
Написать двухпользовательскую консольную версию игры Connect 4
(как крестики-нолики, но 4 в ряд одного цвета, на поле 6x7, с “гравитацией”), для одного
компьютера.

Посмотреть, как работает игра, можно здесь: https://connect4.gamesolver.org

## Минимальные требования:
Язык – python, предпочтительно 3.

Пользователи ходят по очереди.

В самом начале и после очередного хода:

- программа показывает , чей сейчас должен быть ход; позволяет его осуществить;
- после хода выводит новое состояние доски и автоматически анализирует , есть ли
победитель;
- если он есть, эта информация выводится на экран и игра завершается.

## На усмотрение исполнителя:
Способ и формат вывода на экран доски;

Способ осуществления нового хода.

Время выполнения – 1:30 (максимум 1:45).


## Helping commands

    make help
    Application: connect4

    Run command:
    make <target>

    install         install core dependencies
    install/test    install testing/linting dependencies
    install/dev     install testing and debugging tools
    lint            execute linter
    lint/fix        execute linter and apply propsed fixes
    fmt             apply formatter
    test            run tests
    typecheck       check typing annotations
    app/run         run the application
    app/help        show the application help
    clean           delete trash files

    help            this message

## Application CLI interface

    make app/help
    uv run connect4 -h
    usage: connect4 [-h] [--players-number PLAYERS_NUMBER] [--width WIDTH] [--height HEIGHT] [--sequence-length SEQUENCE_LENGTH] [--log-level LOG_LEVEL]

    options:
    -h, --help            show this help message and exit
    --players-number, -n PLAYERS_NUMBER
                            Number of players
    --width WIDTH         Width of the arena
    --height HEIGHT       Height of the arena
    --sequence-length, -s SEQUENCE_LENGTH
                            Length of a continuous sequence to win
    --log-level, -l LOG_LEVEL
                            Application log level

## Running the app

    make install && make app/run