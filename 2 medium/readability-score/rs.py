import argparse
import math
import pathlib
import re
from typing import Callable


def _score_to_age_agi(score: int) -> int:
    if score == 1:
        return 6
    elif 1 < score < 13:
        return score + 6
    elif score == 13:
        return 24
    else:
        return 25


def _score_to_age_dc(score: float) -> int:
    if score < 5:
        return 10
    elif 5 <= score < 6:
        return 12
    elif 6 <= score < 7:
        return 14
    elif 7 <= score < 8:
        return 16
    elif 8 <= score < 9:
        return 18
    else:
        return 24


class ReadabilityIndex:
    def __init__(
        self,
        acronym: str,
        name: str,
        score: int | float,
        score_to_age_func: Callable,
    ):
        self.acronym = acronym
        self.name = name
        self.score = score
        self.score_to_age_func = score_to_age_func

    @property
    def age(self) -> int:
        return self.score_to_age_func(self.score)

    def show(self) -> None:
        print(f"{self.name}:", self.score, "(about", self.age, "year olds).")


class Text:
    sentences: list[str]
    words: list[str]
    characters: list[str]
    n_syllables: int
    n_polysyllables: int
    n_difficult_words: int

    def _count_syllables(self) -> tuple[int, int]:
        pattern = re.compile(r"(?!e$)[aeiouy]+", re.I)
        syllables = [len(re.findall(pattern, word)) or 1 for word in self.words]

        return sum(syllables), len([x for x in syllables if x > 2])

    def _tokenize(self) -> None:
        self.sentences = re.split(r"[.!?]\s+", self.text)
        self.words = re.findall(r"\w+", self.text)
        self.characters = re.findall(r"\S", self.text)

    def __init__(self, text: str, wordlist: list[str]):
        self.text = text
        self._tokenize()
        self.n_syllables, self.n_polysyllables = self._count_syllables()
        self.n_difficult_words = len(
            [w for w in self.words if w.lower() not in wordlist]
        )

    def show(self) -> None:
        print("The text is:", self.text, sep="\n", end="\n\n")
        print("Words:", len(self.words))
        print("Difficult words:", self.n_difficult_words)
        print("Sentences:", len(self.sentences))
        print("Characters:", len(self.characters))
        print("Syllables:", self.n_syllables)
        print("Polysyllables:", self.n_polysyllables)


def compute_ari(text: Text) -> ReadabilityIndex:
    return ReadabilityIndex(
        "ARI",
        "Automated Readability Index",
        math.ceil(
            4.71 * (len(text.characters) / len(text.words))
            + 0.5 * (len(text.words) / len(text.sentences))
            - 21.43
        ),
        _score_to_age_agi,
    )


def compute_fk(text: Text) -> ReadabilityIndex:
    return ReadabilityIndex(
        "FK",
        "Flesch–Kincaid readability tests",
        math.ceil(
            0.39 * (len(text.words) / len(text.sentences))
            + 11.8 * (text.n_syllables / len(text.words))
            - 15.59
        ),
        _score_to_age_agi,
    )


def compute_smog(text: Text) -> ReadabilityIndex:
    return ReadabilityIndex(
        "SMOG",
        "Simple Measure of Gobbledygook",
        math.ceil(
            1.043 * math.sqrt(text.n_polysyllables * 30 / len(text.sentences)) + 3.1291
        ),
        _score_to_age_agi,
    )


def compute_cl(text: Text) -> ReadabilityIndex:
    return ReadabilityIndex(
        "CL",
        "Coleman–Liau index",
        math.ceil(
            5.88 * (len(text.characters) / len(text.words))
            - 29.6 * (len(text.sentences) / len(text.words))
            - 15.8
        ),
        _score_to_age_agi,
    )


def compute_dc(text: Text) -> ReadabilityIndex:
    diff_words_percent = text.n_difficult_words / len(text.words) * 100
    score = 3.6365 if diff_words_percent > 5 else 0

    return ReadabilityIndex(
        "DC",
        "Dale-Chall score",
        round(
            0.1579 * diff_words_percent
            + 0.0496 * (len(text.words) / len(text.sentences))
            + score,
            2,
        ),
        _score_to_age_dc,
    )


readability_idxs: dict[str, Callable] = {
    "ARI": compute_ari,
    "FK": compute_fk,
    "SMOG": compute_smog,
    "CL": compute_cl,
    "DC": compute_dc,
}


def show_scores(text: Text) -> None:
    options = ", ".join(readability_idxs)
    answer = input(f"Enter the score you want to calculate ({options}, all): ")

    idxs = readability_idxs.keys() if answer == "all" else answer.split()
    idxs = [idx.upper() for idx in idxs if idx.upper() in readability_idxs]

    print()
    total_age = 0
    for idx in idxs:
        ri = readability_idxs[idx](text)
        ri.show()
        total_age += ri.age

    print(
        "\nThis text should be understood in average by",
        round(total_age / len(idxs), 1),
        "year olds.",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Text statistics")
    parser.add_argument("--infile", help="path to the text file", default="in.txt")
    parser.add_argument("--words", help="path to the words file", default="words.txt")
    args = parser.parse_args()

    txt = Text(
        pathlib.Path(args.infile).read_text(),
        pathlib.Path(args.words).read_text().split(),
    )
    txt.show()
    show_scores(txt)
