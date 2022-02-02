import os
import sys

import colorama
import requests
from bs4 import BeautifulSoup


def is_url(url: str) -> bool:
    return "." in url


def url_to_filename(url: str) -> str:
    return url.rsplit(".", 1)[0].split("//")[-1].replace(".", "_")


class Browser:
    COMMANDS: set[str] = {"back", "exit"}
    TAGS: set[str] = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ul", "ol", "li"}

    cmd_history: list[str]
    tabs_dir: str
    user_agent: str

    def __init__(self, tabs_dir: str):
        self.cmd_history = []
        self.tabs_dir = tabs_dir
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

        if not os.path.exists(tabs_dir):
            os.makedirs(tabs_dir)

    def start(self) -> None:
        while True:
            self.cmd(input())
            print()

    def cmd(self, query: str, remember_history: bool = True) -> None:
        if query in Browser.COMMANDS:
            if query == "back":
                try:
                    self.cmd(self.cmd_history.pop(-2), remember_history=False)
                except IndexError:
                    print("Note: History is empty")
                finally:
                    return
            elif query == "exit":
                sys.exit()

        if is_url(query):
            try:
                contents = self._parse_contents(self.request_contents(query))
            except requests.exceptions.ConnectionError:
                print("Error: Incorrect URL")
            else:
                print(contents)
                self.save_contents(query, contents)
        else:
            try:
                contents = self.retrieve_contents(query)
            except FileNotFoundError:
                print("Error: Incorrect URL")
            else:
                print(contents)

        if remember_history:
            self.cmd_history.append(query)

    def request_contents(self, url: str) -> str:
        url = url if url.startswith("http") else f"https://{url}"
        return requests.get(url, headers={"User-Agent": self.user_agent}).text

    def retrieve_contents(self, url: str) -> str:
        path = os.path.join(self.tabs_dir, url_to_filename(url))
        with open(path) as f:
            return f.read()

    def save_contents(self, url: str, contents: str) -> None:
        path = os.path.join(self.tabs_dir, url_to_filename(url))
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(contents)

    @staticmethod
    def _parse_contents(contents: str) -> str:
        soup = BeautifulSoup(contents, "html.parser")
        return "\n".join(
            f"{colorama.Fore.BLUE}{tag.text.strip()}{colorama.Style.RESET_ALL}"
            if tag.name == "a"
            else tag.text.strip()
            for tag in soup.find_all(Browser.TAGS)
        )


if __name__ == "__main__":
    colorama.init(autoreset=True)

    if len(sys.argv) != 2:
        raise ValueError("Wrong number of arguments. Did you specify the tabs folder?")
    else:
        b = Browser(sys.argv[1])

    b.start()
