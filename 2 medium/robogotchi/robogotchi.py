from typing import Union
import random


class Game:
    def __init__(self):
        self.wins, self.losses, self.draws = 0, 0, 0

        while self.play():
            pass
        else:
            self.show_stats()

    def play(self) -> bool:
        pass

    def win(self):
        print("You won!")
        self.wins += 1

    def loss(self):
        print("The robot won!")
        self.losses += 1

    def draw(self):
        print("It's a draw!")
        self.draws += 1

    def show_stats(self):
        print(
            f"You won: {self.wins},",
            f"The robot won: {self.losses},",
            f"Draws: {self.draws}.",
            sep="\n",
        )


class Numbers(Game):
    MIN_NUM = 0
    MAX_NUM = 1_000_000

    def play(self) -> bool:
        goal = random.randint(self.MIN_NUM, self.MAX_NUM)
        robot = random.randint(self.MIN_NUM, self.MAX_NUM)

        raw_input = input("\nWhat is your number? ")
        print()

        if raw_input == "exit game":
            return False
        else:
            validated_input = self._validate_input(raw_input)
            if type(validated_input) is int:
                print(f"The robot entered the number {robot}.")
                print(f"The goal number is {goal}. ")
                self._check(goal, robot, validated_input)
            return True

    def _validate_input(self, raw_input: str) -> Union[int, None]:
        try:
            number = int(raw_input)
        except ValueError:
            return print("A string is not a valid input!")
        else:
            if number > self.MAX_NUM:
                return print("Invalid input! The number can't be bigger than 1000000")
            elif number < self.MIN_NUM:
                return print("The number can't be negative!")
            return number

    def _check(self, goal: int, robot: int, human: int):
        robot_diff, human_diff = abs(goal - robot), abs(goal - human)
        if robot_diff > human_diff:
            self.win()
        elif robot_diff < human_diff:
            self.loss()
        else:
            self.draw()


class RockPaperScissors(Game):
    win_combinations = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper",
    }
    moves = list(win_combinations)

    def play(self) -> bool:
        move = input("\nWhat is your move? ").lower()

        while move not in self.moves:
            if move == "exit game":
                print()
                return False
            move = input(
                "No such option! Try again!\n\nWhat is your move? ",
            ).lower()
        else:
            robot = random.choice(self.moves)
            print(f"Robot chose {robot} ")
            self._check(move, robot)
            return True

    def _check(self, human, robot):
        if human == robot:
            self.draw()
        elif self.win_combinations[human] == robot:
            self.win()
        else:
            self.loss()


class Robot:
    def __init__(self):
        self.name = input("How will you call your robot? ")

        self._battery, self._overheat, self._skills, self._boredom, self._rust = (
            100,
            0,
            0,
            0,
            0,
        )
        self._rust_events = {
            0: None,
            10: f"Oh no, {self.name} stepped into a puddle!",
            30: f"Oh, {self.name} encountered a sprinkler!",
            50: f"Guess what! {self.name} fell into the pool!",
        }
        self._interactions = {
            "exit": self._exit,
            "info": self._info,
            "work": self._work,
            "play": self._play,
            "oil": self._oil,
            "recharge": self._recharge,
            "sleep": self._sleep,
            "learn": self._learn,
        }
        self._games = {"numbers": Numbers, "rock-paper-scissors": RockPaperScissors}

        while True:
            self.action()

    def action(self):
        choice = None
        while choice not in self._interactions:
            if choice:
                print("\nInvalid input! Try again!")

            print(
                f"\nAvailable interactions with {self.name}: ",
                "exit – Exit",
                "info – Check the vitals",
                "work – Work",
                "play – Play",
                "oil – Oil",
                "recharge – Recharge",
                "sleep – Sleep mode",
                "learn – Learn skills",
                sep="\n",
            )

            choice = input("\nChoose: ")
        else:
            print()
            if self.boredom == 100 and choice != "play":
                return print(
                    f"{self.name} is too bored! {self.name} needs to have fun!"
                )
            elif self.battery == 0 and choice != "recharge":
                return print(
                    f"The level of the battery is 0, {self.name} needs recharging!"
                )
            self._interactions[choice]()

    def _exit(self):
        print("Game over")
        exit()

    def _info(self):
        print(
            f"{self.name}'s stats are: ",
            f"battery is {self.battery},",
            f"overheat is {self.overheat},",
            f"skill level is {self.skills},",
            f"boredom is {self.boredom},",
            f"rust is {self.rust}.",
            sep="\n",
        )

    def _work(self):
        if self.skills < 50:
            print(f"{self.name} has got to learn before working!")
        else:
            rust = self._rust_event()
            self.boredom += 10
            self.overheat += 10
            self.battery -= 10
            self.rust += rust
            print(f"\n{self.name} did well!")

    def _play(self):
        choice = input("Which game would you like to play? ").lower()

        while choice not in self._games:
            choice = input(
                "\nPlease choose a valid option: Numbers or Rock-paper-scissors? "
            ).lower()
        else:
            self._games[choice]()
            print()
            rust = self._rust_event()
            self.overheat += 10
            self.boredom -= 20  #!
            self.rust += rust
            if self.boredom == 0:
                print(f"\n{self.name} is in a great mood!")

    def _oil(self):
        if self.rust == 0:
            print(f"{self.name} is fine, no need to oil!")
        else:
            self.rust -= 20
            print(f"\n{self.name} is less rusty!")

    def _recharge(self):
        if self.battery == 100:
            print(f"{self.name} is charged!")
        else:
            self.overheat -= 5  #!
            self.battery += 10
            self.boredom += 5
            print(f"\n{self.name} is recharged!")

    def _sleep(self):
        self.overheat -= 20  #!
        if self.overheat == 0:
            print(f"{self.name} is cool!")
        else:
            print(f"\n{self.name} cooled off!")

    def _learn(self):
        if self.skills == 100:
            print(f"There's nothing for {self.name} to learn!")
        else:
            self.skills += 10
            self.overheat += 10
            self.battery -= 10
            self.boredom += 5
            print(f"\n{self.name} has become smarter!")

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, new_level):
        print(
            f"{self.name}'s level of the battery was {self._battery}. Now it is {new_level}."
        )
        self._battery = new_level

    @property
    def overheat(self):
        return self._overheat

    @overheat.setter
    def overheat(self, new_level):
        if new_level > 99:
            print(
                f"The level of overheat reached 100, {self.name} has blown up! Game over. Try again?"
            )
            exit()
        else:
            new_level = new_level if new_level > 0 else 0
            if new_level != self._overheat:
                print(
                    f"{self.name}'s level of overheat was {self._overheat}. Now it is {new_level}."
                )
                self._overheat = new_level

    @property
    def skills(self):
        return self._skills

    @skills.setter
    def skills(self, new_level):
        new_level = new_level if new_level > 0 else 0
        print(
            f"{self.name}'s level of skill was {self._skills}. Now it is {new_level}."
        )
        self._skills = new_level

    @property
    def boredom(self):
        return self._boredom

    @boredom.setter
    def boredom(self, new_level):
        new_level = new_level if new_level > 0 else 0
        if new_level != self._boredom:
            print(
                f"{self.name}'s level of boredom was {self._boredom}. Now it is {new_level}."
            )
            self._boredom = new_level

    @property
    def rust(self):
        return self._rust

    @rust.setter
    def rust(self, new_level):
        if new_level > 99:
            print(f"{self.name} is too rusty! Game over. Try again?")
            exit()
        else:
            new_level = new_level if new_level > 0 else 0
            if new_level != self._rust:
                print(
                    f"{self.name}'s level of rust was {self._rust}. Now it is {new_level}."
                )
                self._rust = new_level

    def _rust_event(self) -> bool:
        rust = random.choice(list(self._rust_events))
        if rust:
            print(self._rust_events[rust], end="\n\n")
        return rust


def main():
    Robot()


if __name__ == "__main__":
    main()
