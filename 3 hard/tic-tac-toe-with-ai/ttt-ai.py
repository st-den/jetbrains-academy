import abc
import random
import sys
from typing import Callable


class Player(metaclass=abc.ABCMeta):
    game: "TicTacToe"
    symbol: str
    enemy: "Player"  # Post-init

    def __init__(self, game, symbol):
        self.game = game
        self.symbol = symbol

    @abc.abstractmethod
    def make_move(self, y: int = None, x: int = None) -> None:
        if y is not None and x is not None:
            self.game.board[y][x] = self.symbol
        else:
            raise ValueError


class Human(Player):
    def make_move(self, y: int = None, x: int = None) -> None:
        if y is None and x is None:
            super().make_move(*self._take_coordinates())
        else:
            super().make_move(y, x)

    def _take_coordinates(self) -> tuple[int, int]:
        while True:
            coordinates = input("Enter the coordinates: ").split()

            if not all(c.isdigit() for c in coordinates) or not coordinates:
                print("You should enter numbers!")

            elif not all(map(lambda c: "1" <= c <= "3", coordinates)):
                print("Coordinates should be from 1 to 3!")

            else:
                y, x = map(int, coordinates)
                if self.game.board[y - 1][x - 1] != self.game.EMPTY:
                    print("This cell is occupied! Choose another one!")
                else:
                    return y - 1, x - 1


class Computer(Player):
    LEVELS: dict[str, Callable]
    level: str

    def __init__(self, game: "TicTacToe", symbol: str, level: str):
        self.LEVELS = {"easy": self._easy, "medium": self._medium, "hard": self._hard}

        if level not in self.LEVELS:
            raise ValueError

        super().__init__(game, symbol)
        self.level = level

    def make_move(self, y: int = None, x: int = None) -> None:
        print(f"Making move level {self.level!r}")

        if y is None and x is None:
            super().make_move(*self.LEVELS[self.level]())
        else:
            super().make_move(y, x)

    def _easy(self) -> tuple[int, int]:
        return random.choice(self.game.get_available_moves())

    def _medium(self) -> tuple[int, int]:
        for combination in self.game.WIN_COMBINATIONS:
            values = [self.game.board[y][x] for y, x in combination]

            if len(set(values)) == 2 and values.count(self.game.EMPTY) == 1:
                return combination[values.index(self.game.EMPTY)]

        return self._easy()

    def _hard(self) -> tuple[int, int]:
        _, move = self.game.minimax(self)

        if move is not None:
            return move
        else:
            raise ValueError


class TicTacToe:
    WIN_COMBINATIONS: list[list[tuple[int, int]]] = [
        [(0, 0), (0, 1), (0, 2)],  # horizontal top
        [(1, 0), (1, 1), (1, 2)],  # horizontal middle
        [(2, 0), (2, 1), (2, 2)],  # horizontal bottom
        [(0, 0), (1, 0), (2, 0)],  # vertical left
        [(0, 1), (1, 1), (2, 1)],  # vertical middle
        [(0, 2), (1, 2), (2, 2)],  # vertical right
        [(0, 0), (1, 1), (2, 2)],  # diagonal major
        [(0, 2), (1, 1), (2, 0)],  # diagonal minor
    ]
    EMPTY: str = "_"
    X: str = "X"
    O: str = "O"

    board: list[list[str]]
    current_player: "Player"
    X_player: "Player"
    O_player: "Player"

    def __init__(self):
        while True:
            self._process_command()
            self._set_board()
            self._show_board()

            while not (winner := self.get_winner()):
                self.current_player.make_move()
                self.current_player = self.current_player.enemy
                self._show_board()
            else:
                print(winner if winner == "Draw" else f"{winner} wins", end="\n\n")

    def get_available_moves(self) -> list[tuple[int, int]]:
        available_moves = []

        for y, row in enumerate(self.board):
            for x, el in enumerate(row):
                if el == self.EMPTY:
                    available_moves.append((y, x))

        return available_moves

    def get_winner(self) -> str:
        has_empty = False

        for combination in self.WIN_COMBINATIONS:
            values = {self.board[y][x] for y, x in combination}

            if values == {self.X}:
                return self.X

            if values == {self.O}:
                return self.O

            if self.EMPTY in values:
                has_empty = True

        return "" if has_empty else "Draw"

    def minimax(
        self, player: "Player", depth: int = 0, alpha: int = -10, beta: int = 10
    ) -> tuple[int, tuple[int, int] | None]:
        match self.get_winner():
            case self.current_player.symbol:
                return 10 - depth, None
            case "Draw":
                return 0, None
            case self.current_player.enemy.symbol:
                return -10 + depth, None

        best_score = -10 if player.symbol == self.current_player.symbol else 10
        move = None

        for y, x in self.get_available_moves():
            self.board[y][x] = player.symbol
            score, _ = self.minimax(player.enemy, depth + 1, alpha, beta)
            self.board[y][x] = self.EMPTY

            if player.symbol == self.current_player.symbol:
                if score > best_score:
                    best_score, move = score, (y, x)

                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score, move = score, (y, x)

                beta = min(beta, best_score)

            if alpha >= beta:
                break

        return best_score, move

    def _create_player(self, symbol: str, level: str) -> "Player":
        return Human(self, symbol) if level == "user" else Computer(self, symbol, level)

    def _process_command(self) -> None:
        while True:
            match input("Input command: ").split():
                case ["exit"]:
                    sys.exit()

                case ["start", player1, player2]:
                    try:
                        self.X_player = self._create_player(self.X, player1)
                        self.O_player = self._create_player(self.O, player2)
                    except ValueError:
                        pass  # Default to general error
                    else:
                        self.X_player.enemy = self.O_player
                        self.O_player.enemy = self.X_player
                        self.current_player = self.X_player
                        break

            print("Bad parameters!")

    def _show_board(self) -> None:
        print("-" * 9)
        for row in self.board:
            print("|", " ".join(row).replace(self.EMPTY, " "), "|")
        print("-" * 9)

    def _set_board(self) -> None:
        self.board = [[self.EMPTY] * 3 for _ in range(3)]


if __name__ == "__main__":
    TicTacToe()
