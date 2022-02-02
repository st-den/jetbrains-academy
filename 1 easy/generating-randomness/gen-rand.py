import random
from typing import Sequence


class ZeroOneGame:
    NGRAM_SIZE = 3
    MIN_DATA_LEN = 100
    START_CAPITAL = 1000
    INPUT_MESSAGE = "\nPrint a random string containing 0 or 1:\n"

    def __init__(self):
        self.corpus = ""
        self.ngrams: dict[str:dict] = {}
        self.user_data = ""
        self.prediction = ""
        self.dollars = self.START_CAPITAL

    def play(self):
        self._enter_corpus()
        self._make_ngrams(self.corpus)

        print(
            f"You have ${self.dollars}. Every time the system successfully predicts your next press, you lose $1.",
            '\nOtherwise, you earn $1. Print "enough" to leave the game. Let\'s go!',
        )

        while self._enter_user_data():
            self._generate_prediction()
            self._show_prediction_accuracy()
            self._make_ngrams(self.user_data)
            self.user_data = ""

    def _enter_corpus(self):
        corpus = []
        print("Please give AI some data to learn...")
        while True:
            print(
                f"The current data length is {len(corpus)}, {self.MIN_DATA_LEN - len(corpus)} symbols left"
            )
            corpus.extend(c for c in input(self.INPUT_MESSAGE) if c in "01")
            if len(corpus) >= self.MIN_DATA_LEN:
                break

        self.corpus = "".join(corpus)
        print(f"Final data string:\n{self.corpus}\n")

    def _enter_user_data(self) -> bool:
        while not self.user_data:
            user_data = input(self.INPUT_MESSAGE)
            if user_data == "enough":
                print("Game over!")
                return False
            self.user_data = "".join(c for c in user_data if c in "01")
        return True

    def _make_ngrams(self, user_data: Sequence[str]):
        for i in range(len(user_data) - self.NGRAM_SIZE):
            ngram = user_data[i : i + self.NGRAM_SIZE]
            self.ngrams.setdefault(ngram, {"0": 0, "1": 0})
            self.ngrams[ngram][self.corpus[i + self.NGRAM_SIZE]] += 1

    def _generate_prediction(self):
        in_ai = "".join(random.choices(self.corpus, k=self.NGRAM_SIZE)) + self.user_data
        out_ai = []
        for i in range(len(in_ai) - self.NGRAM_SIZE):
            ngram = self.ngrams[in_ai[i : i + self.NGRAM_SIZE]]
            out_ai.append(
                random.choice("01")
                if ngram["0"] == ngram["1"]
                else max(ngram, key=ngram.get)
            )

        self.prediction = "".join(out_ai)

    def _show_prediction_accuracy(self):
        n_guessed = sum(
            self.user_data[i] == self.prediction[i]
            for i in range(self.NGRAM_SIZE, len(self.prediction))
        )

        n_predicted = len(self.prediction) - self.NGRAM_SIZE
        self.dollars += n_predicted - 2 * n_guessed

        print(f"prediction:\n{self.prediction}")
        print(
            f"\nComputer guessed right {n_guessed} out of {n_predicted} symbols",
            f"({round(n_guessed / n_predicted * 100, 2)} %)",
            f"\nYour balance is now ${self.dollars}",
        )


if __name__ == "__main__":
    ZeroOneGame().play()
