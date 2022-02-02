from collections import defaultdict
from random import shuffle


class Domino:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y
        self.rank = x + y
        self.is_double = x == y

    def reorient(self):
        self.x, self.y = self.y, self.x

    def __add__(self, other):
        return self.rank + other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __lt__(self, other):
        return self.rank < other.rank

    def __repr__(self):
        return f"[{self.x}, {self.y}]"


class DominoesHand:
    def __init__(self, hand: list[Domino], is_table=False):
        self.hand = hand
        self.is_table = is_table

    def get_doubles(self) -> list[Domino]:
        return [domino for domino in self.hand if domino.is_double]

    def take(self, index=-1) -> Domino:
        return self.hand.pop(index)

    def remove(self, domino: Domino):
        self.hand.remove(domino)

    def place_left(self, domino: Domino):
        if self.is_table and len(self.hand) and domino.y != self.hand[0].x:
            domino.reorient()
            if domino.y != self.hand[0].x:
                raise ValueError
        self.hand.insert(0, domino)

    def place_right(self, domino: Domino):
        if self.is_table and len(self.hand) and self.hand[-1].y != domino.x:
            domino.reorient()
            if self.hand[-1].y != domino.x:
                raise ValueError
        self.hand.append(domino)

    def __add__(self, other):
        return self.hand + other.hand

    def __getitem__(self, sliced):
        return self.hand[sliced]

    def __len__(self):
        return len(self.hand)

    def __str__(self):
        if self.is_table:
            if len(self.hand) > 6:
                return (
                    "".join(str(d) for d in self.hand[:3])
                    + "..."
                    + "".join(str(d) for d in self.hand[-3:])
                )
            return "".join(str(d) for d in self.hand)
        return "\n".join([f"{i + 1}:{self.hand[i]}" for i in range(len(self.hand))])


class DominoesGame:
    STATUS_MESSAGES = {
        "win": "The game is over. You won!",
        "lose": "The game is over. The computer won!",
        "draw": "The game is over. It's a draw!",
        "player": "It's your turn to make a move. Enter your command.",
        "comp": "Computer is about to make a move. Press Enter to continue...",
    }

    def __init__(self):
        self.deck = [Domino(i, j) for i in range(7) for j in range(i, 7)]
        self.table = DominoesHand([], is_table=True)
        self.status = ""

    def play(self):
        self._split_deck()
        self._make_first_move()

        while True:
            self._check_game_end()
            print(self)
            if self.status == "player":
                self._make_player_move()
            elif self.status == "comp":
                self._make_comp_move()
            else:
                break

    def _split_deck(self):
        shuffle(self.deck)
        self.comp, self.player, self.stock = (
            DominoesHand(self.deck[:7]),
            DominoesHand(self.deck[7:14]),
            DominoesHand(self.deck[14:]),
        )

    def _check_game_end(self):
        if len(self.player) == 0:
            self.status = "win"
        elif len(self.comp) == 0:
            self.status = "lose"
        elif (
            self.table[0].x == self.table[-1].y
            and len([d for d in self.table if self.table[0].x in (d.x, d.y)]) == 7
        ):
            self.status = "draw"

    def _make_first_move(self):
        try:
            max_double = max(self.comp.get_doubles() + self.player.get_doubles())
        except ValueError:
            self._split_deck()
            self._make_first_move()
        else:
            try:
                self.comp.remove(max_double)
                self.status = "player"
            except ValueError:
                self.player.remove(max_double)
                self.status = "comp"
            self.table.place_right(max_double)

    def _make_player_move(self):
        while True:
            try:
                action = int(input())
                if -len(self.player) <= action <= len(self.player):
                    try:
                        if action < 0:
                            self.table.place_left(self.player[abs(action) - 1])
                            self.player.take(abs(action) - 1)
                        elif action > 0:
                            self.table.place_right(self.player[action - 1])
                            self.player.take(action - 1)
                        elif len(self.stock):
                            self.player.place_right(self.stock.take())
                    except ValueError:
                        print("Illegal move. Please try again.")
                        continue
                    break
                raise ValueError
            except ValueError:
                print("Invalid input. Please try again.")
        self.status = "comp"

    def _make_comp_move(self):
        scores = defaultdict(int)
        for d in self.table + self.comp:
            scores[d.x] += 1
            scores[d.y] += 1
        comp_scored = sorted({d: scores[d.x] + scores[d.y] for d in self.comp})

        while comp_scored:
            try:
                self.table.place_left(comp_scored[0])
            except ValueError:
                try:
                    self.table.place_right(comp_scored[0])
                except ValueError:
                    comp_scored.pop(0)
                    continue
            self.comp.remove(comp_scored[0])
            break
        else:
            if len(self.stock):
                self.comp.place_right(self.stock.take())
        self.status = "player"
        input()

    def __str__(self):
        return "\n".join(
            (
                "=" * 70,
                f"Stock size: {len(self.stock)}",
                f"Computer pieces: {len(self.comp)}\n",
                str(self.table),
                "\nYour pieces:",
                str(self.player),
                f"\nStatus: {self.STATUS_MESSAGES[self.status]}",
            )
        )


if __name__ == "__main__":
    game = DominoesGame()
    game.play()
