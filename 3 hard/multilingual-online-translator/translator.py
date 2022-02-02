import argparse
import sys

import requests
from bs4 import BeautifulSoup


def save_translation(translation: str, filename: str) -> None:
    with open(f"{filename}.txt", "w", encoding="utf-8") as f:
        f.write(translation)


class Translator:
    BASE_URL: str = "https://context.reverso.net/translation"
    HEADERS: dict = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    LANGUAGES: list = [
        "arabic",
        "german",
        "english",
        "spanish",
        "french",
        "hebrew",
        "japanese",
        "dutch",
        "polish",
        "portuguese",
        "romanian",
        "russian",
        "turkish",
    ]

    def translate(self, from_lang: str, to_lang: str, word: str) -> str:
        output = []
        n_max = 1 if to_lang == "all" else 5
        from_lang, to_langs = self._parse_langs(from_lang, to_lang)

        for lang in to_langs:
            r = self._request(from_lang, lang, word)
            page = BeautifulSoup(r.text, "html.parser")

            found = self._format_translations(self._find_translations(page), n_max)
            if found:
                output.append(f"\n{lang.capitalize()} Translations:")
                output.append(found)
            else:
                print("Sorry, unable to find", word)
                sys.exit()

            found = self._format_examples(self._find_examples(page), n_max)
            if found:
                output.append(f"\n{lang.capitalize()} Examples:")
                output.append(found)
            else:
                print("Sorry, unable to find", word)
                sys.exit()

        return "\n".join(output)

    def _parse_langs(self, from_lang: str, to_lang: str) -> tuple[str, list[str]]:
        if from_lang not in self.LANGUAGES:
            print("Sorry, the program doesn't support", from_lang)
            sys.exit()

        if to_lang == "all":
            to_langs = [lang for lang in self.LANGUAGES if lang != from_lang]
        elif to_lang in self.LANGUAGES:
            to_langs = [to_lang]
        else:
            print("Sorry, the program doesn't support", to_lang)
            sys.exit()

        return from_lang, to_langs

    def _request(self, from_lang: str, to_lang: str, word: str) -> requests.Response:
        direction = f"{from_lang}-{to_lang}"
        try:
            return requests.get(
                "/".join([self.BASE_URL, direction, word]), headers=self.HEADERS
            )
        except requests.exceptions.RequestException:
            print("Something wrong with your internet connection")
            sys.exit()

    @staticmethod
    def _find_translations(page: BeautifulSoup) -> list[str]:
        selector = "div#translations-content a"
        return [a.text.strip() for a in page.select(selector)]

    @staticmethod
    def _find_examples(page: BeautifulSoup) -> list[str]:
        selector = "section#examples-content span.text"
        return [span.text.strip() for span in page.select(selector)]

    @staticmethod
    def _format_translations(translations: list[str], max_: int = 5) -> str:
        return "\n".join(translations[:max_])

    @staticmethod
    def _format_examples(examples: list[str], max_: int = 5) -> str:
        orig = examples[: max_ * 2 : 2]
        trans = examples[1 : max_ * 2 : 2]
        return "\n\n".join(map("\n".join, zip(orig, trans)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This program translates words using context.reverso.net"
    )
    parser.add_argument("from_lang")
    parser.add_argument("to_lang")
    parser.add_argument("word")
    args = parser.parse_args()

    translator = Translator()
    print(results := translator.translate(args.from_lang, args.to_lang, args.word))
    save_translation(results, args.word)
