import json
import os
import sys
from typing import Type


class Character:
    name: str
    species: str
    gender: str

    snack: str
    weapon: str
    tool: str
    extra_items: list[str]

    difficulty: str
    lives: int

    def __init__(self, **kwargs):
        if kwargs:
            self.__dict__.update(kwargs)
        else:
            print("Create your character:")
            self.name = input("1- Name ")
            self.species = input("2- Species ")
            self.gender = input("3- Gender ")

            print("Pack your bag for the journey:")
            self.snack = input("1- Favourite Snack ")
            self.weapon = input("2- A weapon for the journey ")
            self.tool = input("3- A traversal tool ")
        self.extra_items = []

    def __str__(self):
        return "\n".join(
            [
                f"Your character: {self.name}, {self.species}, {self.gender}",
                f"Your inventory: {self.snack}, {self.weapon}, {self.tool}",
                f"Difficulty: {self.difficulty}",
                f"Number of lives: {self.lives}",
            ]
        )

    def increase_lives(self) -> str:
        self.lives += 1
        return f"You gained an extra life! Lives remaining: {self.lives}"

    def decrease_lives(self) -> str:
        self.lives -= 1
        return f"You died! Lives remaining: {self.lives}"

    def add_item(self, item: str) -> str:
        self.extra_items.append(item)
        return f"A new item has been added to your inventory: {item}"

    def remove_item(self, item: str) -> str:
        self.extra_items.remove(item)
        return f"An item has been removed from your inventory: {item}"

    def show_inventory(self) -> None:
        print("Inventory:", self.snack, self.weapon, self.tool)

    def show_traits(self) -> None:
        print("Your character:", self.name, self.species, self.gender)
        print("Lives remaining:", self.lives)


class Game:
    _CHARACTER: Type[Character] = Character
    _GAME_TITLE: str = "Text Based Adventure Game"
    _DIFFICULTY_TO_LIVES: dict[str, int] = {"easy": 5, "medium": 3, "hard": 1}

    _plot: dict
    _saves_path: str

    player: Character
    username: str
    lvl: int = 1
    scene: int = 0

    def __init__(self, plot_path: str, saves_path: str = os.path.join("game", "saves")):
        self._saves_path = saves_path
        with open(plot_path) as f:
            # * title: story -> lvlN -> title
            # * scene: story -> lvlN -> scenes -> sceneN
            # * choice: choices -> lvlN -> sceneN -> choiceN
            # * outcome: outcomes -> lvlN -> sceneN -> outcomeN [-> optionN]
            self._plot = json.load(f)

        while True:
            if hasattr(self, "player"):
                while self.player.lives > 0:
                    if self.scene == 0:
                        print("\n", self._get_title(), sep="")
                        self.scene = 1
                    self._progress()
                else:
                    print("You've run out of lives! Game over!\n")
                    del self.player
            else:
                self.menu()

    def menu(self) -> None:
        print(f"***Welcome to the {self._GAME_TITLE}***\n")
        print(
            "1- Press key '1' or type 'start' to start a new game",
            "2- Press key '2' or type 'load' to load your progress",
            "3- Press key '3' or type 'quit' to quit the game",
            sep="\n",
        )

        while True:
            match input().lower():
                case "1" | "start":
                    print("Starting a new game...")
                    self._create_player()
                case "2" | "load":
                    self._load_player()
                case "3" | "quit":
                    self._quit(force=True)
                case _:
                    print("Unknown input! Please enter a valid one.")
                    continue
            break

    def _progress(self) -> None:
        try:
            print("\n", self._get_scene().strip(), sep="")
        except KeyError:
            self._quit(force=True)

        print("\nWhat will you do? Type the number of the option or type '/h' to show help.\n")

        choices = self._get_choices()
        for i, choice in enumerate(choices, start=1):
            print(f"{i}- {choice.strip()}")

        while True:
            match choice := input():
                case "1" | "2" | "3":
                    self._process_outcome(self._get_outcome(choice))
                case "/c":
                    self.player.show_traits()
                case "/i":
                    self.player.show_inventory()
                case "/q":
                    self._quit()
                case "/h":
                    self._show_help()
                case _:
                    print("Unknown input! Please enter a valid one.")
                    continue
            break

    def _create_player(self) -> None:
        print("Enter a user name to save your progress or type '/b' to go back", end=" ")
        while True:
            match choice := input():
                case "":
                    print("Unknown input! Please enter a valid one.")
                    continue
                case "/b":
                    print("Going back to menu...\n")
                case _:
                    player = self._CHARACTER()
                    player.difficulty = self._choose_difficulty()
                    player.lives = self._DIFFICULTY_TO_LIVES[player.difficulty]

                    self.username = choice
                    self.player = player

                    print("Good luck on your journey!")
                    print(player)
            break

    def _load_player(self) -> None:
        usernames: None | list[str] = None
        try:
            usernames = [os.path.splitext(f)[0] for f in os.listdir(self._saves_path)]
        except OSError:
            print("No save data found!")

        if usernames:
            print("Choose your user name from the list:")
            print(*usernames, sep="\n")

            username = input("Type your user name: ")
            if username and username in usernames:
                print("Loading your progress...")
                save_path = os.path.join(self._saves_path, username + ".json")
                with open(save_path, "r") as f:
                    data = json.load(f)

                self.username = username
                self.player = self._CHARACTER(
                    **data["char_attrs"]
                    | data["inventory"]
                    | {"difficulty": data["difficulty"]}
                    | {"lives" : data["lives"]}
                )
                self.lvl = data["level"]
            else:
                print("No save data found!")

    def _save_player(self) -> None:
        os.makedirs(self._saves_path, exist_ok=True)
        save_path = os.path.join(self._saves_path, self.username + ".json")
        with open(save_path, "w") as f:
            json.dump(
                {
                    "char_attrs": {
                        "name": self.player.name,
                        "species": self.player.species,
                        "gender": self.player.gender,
                    },
                    "inventory": {
                        "snack": self.player.snack,
                        "weapon": self.player.weapon,
                        "tool": self.player.tool,
                    },
                    "difficulty": self.player.difficulty,
                    "lives": self.player.lives,
                    "level": self.lvl,
                },
                f
            )

    def _choose_difficulty(self) -> str:
        print("Choose your difficulty:", "1- Easy", "2- Medium", "3- Hard", sep="\n")
        while True:
            match input().lower():
                case "1" | "easy":
                    return "easy"
                case "2" | "medium":
                    return "medium"
                case "3" | "hard":
                    return "hard"
                case _:
                    print("Unknown input! Please enter a valid one.")

    def _get_title(self) -> str:
        lvl = f"lvl{self.lvl}"
        return self._plot["story"][lvl]["title"]

    def _get_scene(self) -> str:
        lvl, scene = f"lvl{self.lvl}", f"scene{self.scene}"
        return self._plot["story"][lvl]["scenes"][scene]

    def _get_choices(self) -> list[str]:
        lvl, scene = f"lvl{self.lvl}", f"scene{self.scene}"
        return [*self._plot["choices"][lvl][scene].values()]

    def _get_outcome(self, choice: str) -> str | list[str]:
        lvl, scene, outcome = f"lvl{self.lvl}", f"scene{self.scene}", f"outcome{choice}"
        outcome = self._plot["outcomes"][lvl][scene][outcome]
        return outcome if isinstance(outcome, str) else [*outcome.values()]

    def _process_outcome(self, outcome: str | list[str]) -> None:
        if isinstance(outcome, str):
            effects_start_idx, effects_end_idx = outcome.rfind("("), outcome.rfind(")")
            effects = outcome[effects_start_idx : effects_end_idx + 1]

            state_updates = self._process_effects(effects.strip("()"))
            outcome = self._replace_placeholders(outcome[: effects_start_idx - 1])

            print(outcome)
            for update in state_updates:
                print(update)
        elif isinstance(outcome, list):
            try:
                return self._process_outcome(outcome[0])
            except ValueError:
                return self._process_outcome(outcome[1])

    def _process_effects(self, effects: str) -> list[str]:
        state_updates: list[str] = []

        for effect in effects.split(" and "):
            match effect:
                case "life+1":
                    state_updates.append(self.player.increase_lives())
                case "life-1":
                    state_updates.append(self.player.decrease_lives())
                    self.scene = 0
                case effect if "inventory" in effect:
                    item = effect[effect.find("'") + 1 : effect.rfind("'")]

                    if "+" in effect:
                        state_updates.append(self.player.add_item(item))
                    elif "-" in effect:
                        state_updates.append(self.player.remove_item(item))
                case "move":
                    self.scene += 1
                case "save":
                    self.lvl += 1
                    self.scene = 0
                    self._save_player()
                case "game_won":
                    self.scene = -1
                    state_updates.append("Congratulations! You beat the game!")

        return state_updates

    def _replace_placeholders(self, outcome: str) -> str:
        placeholders = {
            "{snack}": self.player.snack,
            "{weapon}": self.player.weapon,
            "{tool}": self.player.tool,
        }

        for k, v in placeholders.items():
            outcome = outcome.replace(k, v)

        return outcome

    def _show_help(self) -> None:
        print(
            "Type the number of the option you want to choose.",
            "Commands you can use:",
            "/i => Shows inventory.",
            "/q => Exits the game.",
            "/c => Shows the character traits.",
            "/h => Shows help.",
            sep="\n",
        )

    def _quit(self, force=False) -> None:
        def real_quit():
            print("\nGoodbye!")
            sys.exit()

        if force:
            real_quit()

        print("You sure you want to quit the game? Y/N", end=" ")
        while True:
            match input().lower():
                case "y":
                    real_quit()
                case "n":
                    break
                case _:
                    print("Unknown input! Please enter a valid one.")


if __name__ == "__main__":
    Game(os.path.join("story", "story.json"))