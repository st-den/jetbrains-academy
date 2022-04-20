import json
import sys
from argparse import ArgumentParser
from dataclasses import asdict, dataclass
from io import StringIO
from pathlib import Path
from random import choices
from shutil import copyfileobj
from typing import Callable

_logbuffer: StringIO = StringIO()


def _print(text: object = "") -> None:
    print(text, file=_logbuffer)
    print(text)


def _input(prompt: object = "") -> str:
    input_ = input(prompt)
    print(prompt, input_, sep="", file=_logbuffer)
    return input_


@dataclass
class Card:
    term: str
    definition: str
    errors: int


class Controller:
    _import_from: str | None
    _export_to: str | None
    cards: dict[str, Card] = {}  # card.term : card

    def __init__(self, **kwargs) -> None:
        self._import_from = kwargs.get("import_from")
        self._export_to = kwargs.get("export_to")

    def start(self) -> None:
        if self._import_from is not None:
            self.import_(self._import_from)

        options: dict[str, Callable] = {
            "add": self.add,
            "remove": self.remove,
            "import": self.import_,
            "export": self.export,
            "ask": self.ask,
            "exit": self.exit,
            "log": self.log,
            "hardest card": self.hardest_card,
            "reset stats": self.reset_stats,
        }

        while True:
            choice = _input(f"Input the action ({', '.join(options)}):\n")
            if choice in options:
                options[choice]()
            _print()

    def add(self) -> None:
        term = _input("The card:\n")
        while term in self.cards.keys():
            term = _input(f'The card "{term}" already exists. Try again:\n')

        def_ = _input("The definition of the card:\n")
        while def_ in [card.definition for card in self.cards.values()]:
            def_ = _input(f'The definition "{def_}" already exists. Try again:\n')

        _print(f'The pair ("{term}":"{def_}") has been added.')
        self.cards[term] = Card(term, def_, 0)

    def remove(self) -> None:
        term = _input("Which card?\n")
        if term in self.cards.keys():
            _print("The card has been removed.")
            del self.cards[term]
        else:
            _print(f'Can\'t remove "{term}": there is no such card.')

    def import_(self, file_name: str | None = None) -> None:
        if file_name is None:
            file_name = _input("File name:\n")
        try:
            cards = json.loads(Path(file_name).read_text())
        except FileNotFoundError:
            _print(f'File "{file_name}" not found.')
        else:
            self.cards = {card["term"]: Card(**card) for card in cards}
            _print(f"{len(self.cards)} cards have been loaded.")

    def export(self, file_name: str | None = None) -> None:
        if file_name is None:
            file_name = _input("File name:\n")
        Path(file_name).write_text(
            json.dumps([asdict(card) for card in self.cards.values()])
        )
        _print(f"{len(self.cards)} cards have been saved.")

    def ask(self) -> None:
        def wrong(answer_def, correct_def) -> str:
            if existing := list(
                filter(lambda x: x.definition == answer_def, self.cards.values())
            ):
                msg = [
                    f'Wrong. The right answer is "{correct_def}", ',
                    f'but your definition is correct for "{existing[0].term}".',
                ]
            else:
                msg = [f'Wrong. The right answer is "{correct_def}".']
            return "".join(msg)

        n_cards = int(_input("How many times to ask?\n"))

        for card in choices(list(self.cards.values()), k=n_cards):
            answer = _input(f'Print the definition of "{card.term}":\n')

            if answer == card.definition:
                _print("Correct!")
            else:
                _print(wrong(answer, card.definition))
                card.errors += 1

    def hardest_card(self) -> None:
        if with_errors := list(filter(lambda x: x.errors > 0, self.cards.values())):
            hardest = sorted(with_errors, key=lambda x: x.errors, reverse=True)
            top = [card for card in hardest if card.errors == hardest[0].errors]

            if len(top) > 1:
                msg = [
                    "The hardest cards are ",
                    ", ".join(f'"{card.term}"' for card in top),
                    f". You have {top[0].errors} errors answering them.",
                ]
            else:
                msg = [
                    "The hardest card is ",
                    f'"{hardest[0].term}". ',
                    f"You have {hardest[0].errors} errors answering it.",
                ]

            _print("".join(msg))

        else:
            _print("There are no cards with errors.")

    def reset_stats(self) -> None:
        for card in self.cards.values():
            card.errors = 0
        _print("Card statistics have been reset.")

    def exit(self) -> None:
        _print("Bye bye!")
        if self._export_to is not None:
            self.export(self._export_to)
        sys.exit()

    @staticmethod
    def log() -> None:
        file_name = _input("File name:\n")
        with Path(file_name).open(mode="a") as file:
            _logbuffer.seek(0)
            copyfileobj(_logbuffer, file)
        _print("The log has been saved.")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--import_from")
    parser.add_argument("--export_to")
    args = parser.parse_args()

    Controller(**vars(args)).start()
