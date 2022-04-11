from collections import namedtuple
from itertools import product
from string import Template

Symbols = namedtuple("Symbol", ["EMPTY", "KNIGHT", "VISITED"])


class ChessBoard:
    MOVES = [*product((1, -1), (2, -2)), *product((2, -2), (1, -1))]
    SYMBOLS = Symbols("_", "X", "*")

    size_x: int
    size_y: int
    moves_max: int

    _board: list[list[str | int]]
    _marked_cells: list[tuple[int, int]]

    def _empty_board(self) -> None:
        self._board = [
            [self.SYMBOLS.EMPTY for _ in range(self.size_x)] for _ in range(self.size_y)
        ]

    def __init__(self, size_x: int, size_y: int) -> None:
        self.size_x, self.size_y = size_x, size_y
        self.moves_max = size_x * size_y
        self._marked_cells = []
        self._empty_board()

    def _is_cell_empty(self, pos: tuple) -> bool:
        try:
            return self[pos] == self.SYMBOLS.EMPTY
        except IndexError:
            return False

    def _is_move_valid(self, dest: tuple) -> bool:
        return dest in self._marked_cells

    def _get_moves(self, start: tuple) -> list[tuple]:
        moves = [tuple(map(sum, zip(start, delta))) for delta in self.MOVES]
        return list(filter(self._is_cell_empty, moves))

    def _get_cell_score(self, pos: tuple) -> int:
        return len(self._get_moves(pos))

    def _clear_scores(self) -> None:
        for pos in self._marked_cells:
            self[pos] = self.SYMBOLS.EMPTY
        self._marked_cells = []

    def _mark_scores(self, pos: tuple) -> None:
        for move in self._get_moves(pos):
            self[move] = self._get_cell_score(move)
            self._marked_cells.append(move)

    def has_solution(self, start: tuple) -> bool:
        self[start] = 1
        solution_possible = self.solve(start)
        self._empty_board()

        return solution_possible

    def has_moves_left(self) -> bool:
        return self._marked_cells != []

    def move_knight(self, start: tuple | None, dest: tuple) -> None:
        if start is None:
            self[dest] = self.SYMBOLS.KNIGHT
        else:
            if not self._is_move_valid(dest):
                raise ValueError

            self[start] = self.SYMBOLS.VISITED
            self[dest] = self.SYMBOLS.KNIGHT

            self._marked_cells.remove(dest)
            self._clear_scores()
        self._mark_scores(dest)

    def solve(self, start: tuple, counter: int = 2) -> bool:
        if counter > self.moves_max:
            return True

        scored_moves = sorted(
            {
                dest: self._get_cell_score(dest) for dest in self._get_moves(start)
            }.items(),
            key=lambda x: x[1],
        )

        for dest, _ in scored_moves:
            self[dest] = counter
            if self.solve(dest, counter + 1):
                return True
            self[dest] = self.SYMBOLS.EMPTY

        return False

    def show(self) -> None:
        cell_w = len(str(self.size_x * self.size_y))
        y_marker_w = len(str(self.size_y))
        line = "".join((" " * y_marker_w, "-" * (self.size_x * (cell_w + 1) + 3)))
        x_markers = [str(x).rjust(cell_w) for x in range(1, self.size_x + 1)]

        print(line)
        for y in range(self.size_y, 0, -1):
            print(str(y).rjust(y_marker_w), end="| ")
            cells = [
                self.SYMBOLS.EMPTY * cell_w
                if self[x, y] == self.SYMBOLS.EMPTY
                else str(self[x, y]).rjust(cell_w)
                for x in range(1, self.size_x + 1)
            ]
            print(*cells, "|")
        print(line)
        print(" " * (y_marker_w + 1), *x_markers, end=" \n\n")

    def __getitem__(self, pos: tuple[int, int]) -> str | int:
        x, y = pos
        if (x < 1 or x > self.size_x) or (y < 1 or y > self.size_y):
            raise IndexError
        return self._board[self.size_y - y][x - 1]

    def __setitem__(self, pos: tuple[int, int], value: str | int) -> None:
        x, y = pos
        if (x < 1 or x > self.size_x) or (y < 1 or y > self.size_y):
            raise IndexError
        self._board[self.size_y - y][x - 1] = value


class Puzzle:
    MESSAGE = {
        "dim": "Enter your board dimensions: ",
        "pos0": "Enter the knight's starting position: ",
        "pos1": "Enter your next move: ",
        "win": "What a great tour! Congratulations!",
        "loss": Template("No more possible moves!\nYour knight visited ${n} squares!"),
        "no_sln": "No solution exists!",
        "has_sln": "\nHere's the solution!",
    }
    ERROR = {
        "mode": "Invalid option!",
        "dim": "Invalid dimensions!",
        "pos0": "Invalid position!",
        "pos1": "Invalid move!",
    }
    board: ChessBoard

    def create_board(self) -> tuple:
        size_x, size_y = Puzzle.get_dim()
        self.board = ChessBoard(size_x, size_y)

        return Puzzle.get_pos(size_x, size_y, first=True)

    def start(self, start: tuple) -> None:
        while True:
            match input("Do you want to try the puzzle? (y/n): "):
                case "y" | "Y":
                    if self.board.has_solution(start):
                        self.board.move_knight(None, start)
                        self.board.show()
                        self.play(start)
                    else:
                        print(Puzzle.MESSAGE["no_sln"])
                    break
                case "n" | "N":
                    if self.board.has_solution(start):
                        print(Puzzle.MESSAGE["has_sln"])
                        self.board[start] = 1
                        self.board.solve(start)
                        self.board.show()
                    else:
                        print(Puzzle.MESSAGE["no_sln"])
                    break
                case _:
                    print(Puzzle.ERROR["mode"])

    def play(self, start: tuple) -> None:
        moves_made = 1

        while self.board.has_moves_left():
            dest = Puzzle.get_pos(self.board.size_x, self.board.size_y)
            try:
                self.board.move_knight(start, dest)
            except ValueError:
                print(Puzzle.ERROR["pos1"], end=" ")
            else:
                moves_made += 1
                start = dest
                self.board.show()

        if moves_made == self.board.moves_max:
            print(Puzzle.MESSAGE["win"])
        else:
            print(Puzzle.MESSAGE["loss"].substitute(n=moves_made))

    @classmethod
    def get_dim(cls) -> tuple:
        while True:
            try:
                size_x, size_y = map(int, input(cls.MESSAGE["dim"]).split())
            except ValueError:
                pass
            else:
                if size_x > 0 and size_y > 0:
                    return size_x, size_y
            print(cls.ERROR["dim"])

    @classmethod
    def get_pos(cls, size_x: int, size_y: int, first: bool = False) -> tuple:
        while True:
            try:
                x, y = map(int, input(cls.MESSAGE[f"pos{int(not first)}"]).split())
            except ValueError:
                pass
            else:
                if (1 <= x <= size_x) and (1 <= y <= size_y):
                    return x, y
            print(cls.ERROR[f"pos{int(first)}"], end=" ")


if __name__ == "__main__":
    puzzle = Puzzle()
    puzzle.start(puzzle.create_board())
