from collections import defaultdict
import random
import re

from typing import DefaultDict


class TextGenerator:
    _checks = {
        "start": lambda token: bool(re.match(r"^[A-Z][\sA-Za-z,'-]+$", token)),
        "end": lambda token: bool(re.match(r"[A-Za-z'-]+[.!?]+", token)),
    }

    def __init__(self):
        self._checks["mid"] = lambda token: not (
            self._checks["start"](token) or self._checks["end"](token)
        )

        self.corpus: list[str] = self._load_corpus()

        self.trigrams: list[tuple[str, str]] = self._make_trigrams(self.corpus)

        self.chains: DefaultDict[str, DefaultDict[str, int]] = self._make_chains(
            self.trigrams
        )

        self.heads: list[str] = list(self.chains)

    def show_text(self):
        """stages 4-6"""
        print(*self._make_text(), sep="\n")

    def show_chain(self, head: str):
        """stage 3"""
        print("Head:", head)
        if tails := self.chains.get(head):
            print(self._get_chain_repr(tails))
        else:
            print(
                "Key Error. The requested word is not in the model. Please input another word."
            )
        print()

    def show_token(self, index: int, bigram: bool = False):
        """stages 1-2"""
        try:
            print(
                self._get_bigram_repr(*self.bigrams[int(index)])
                if bigram
                else self.corpus[int(index)]
            )
        except IndexError:
            print(
                "Index Error. Please input an integer that is in the range of the corpus."
            )
        except ValueError:
            print("Type Error. Please input an integer.")

    def show_stats(self, bigrams=False):
        """stages 1-2"""
        if bigrams:
            print(
                "Corpus statistics",
                f"All tokens: {len(self.corpus)}",
                f"Unique tokens: {len(set(self.corpus))}\n",
                sep="\n",
            )
        else:
            print(f"Number of bigrams: {len(self.corpus) - 1}\n")

    def _get_tail(self, head: str, type_: str = "any") -> str:
        """stages 5-6"""
        try:
            tails = list(self.chains[head])
            freq = list(self.chains[head].values())

            token = random.choices(
                population=list(self.chains[head]),
                weights=list(self.chains[head].values()),
            )[0]

        except:
            head = random.choice(self.heads)
            tails = list(self.chains[head])
            freq = list(self.chains[head].values())

            token = random.choices(
                population=tails,
                weights=freq,
            )[0]

        finally:
            if type_ == "any":
                return token

            elif type_ in ("start", "mid", "end"):
                i = 0
                while not self._checks[type_](token):
                    if (i := 0 if i == 5 else i + 1) == 5:
                        token = self._get_tail(random.choice(self.heads), type_)

                    else:
                        token = random.choices(
                            population=tails,
                            weights=freq,
                        )[0]

            return token

    def _make_text(self, n_sentences: int = 10, min_tokens: int = 5) -> list[str]:
        """stages 4-6"""
        text = []

        while not self._checks["start"](head := random.choice(self.heads)):
            continue
        sentence = [*(head.split())]

        for i in range(n_sentences):
            if i > 0:
                sentence = [self._get_tail(" ".join(head), "start")]

                sentence.append(
                    self._get_tail(" ".join((head[-1], sentence[-1])), "mid")
                )

            if min_tokens > 3:
                for _ in range(min_tokens - 3):
                    sentence.append(self._get_tail(" ".join(sentence[-2:]), "mid"))

            while not self._checks["end"](
                tail := self._get_tail(" ".join(sentence[-2:]))
            ):
                sentence.append(tail)
            sentence.append(tail)

            head = sentence[-2:]
            text.append(" ".join(sentence))

        return text

    @staticmethod
    def _make_trigrams(corpus: list[str]) -> list[tuple[str, str]]:
        """stage 6"""
        return [
            (" ".join(corpus[i : i + 2]), corpus[i + 2]) for i in range(len(corpus) - 2)
        ]

    @staticmethod
    def _make_chains(
        ngrams: list[tuple[str, str]]
    ) -> DefaultDict[str, DefaultDict[str, int]]:
        """stages 3-6"""
        chains = defaultdict(lambda: defaultdict(int))
        for head, tail in ngrams:
            chains[head][tail] += 1
        return chains

    @staticmethod
    def _get_chain_repr(tails: DefaultDict[str, int]) -> str:
        """stage 3"""
        return "\n".join(
            [f"Tail: {tail}\t Count: {freq}" for tail, freq in tails.items()]
        )

    @staticmethod
    def _make_bigrams(corpus: list[str]) -> list[tuple[str, str]]:
        """stages 2-5"""
        return [(corpus[i], corpus[i + 1]) for i in range(len(corpus) - 1)]

    @staticmethod
    def _get_bigram_repr(head: str, tail: str) -> str:
        """stages 1-2"""
        return f"Head: {head}\tTail: {tail}"

    @staticmethod
    def _load_corpus() -> list[str]:
        """stages 1-6"""
        with open(input(), encoding="utf-8") as f:
            return f.read().split()


def main():
    tg = TextGenerator()
    tg.show_text()


if __name__ == "__main__":
    main()
