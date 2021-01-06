import random


class Game:
    def __init__(self, player):
        self.options = list()
        self.combinations = dict()

        self.player = player
        print("Hello,", self.player.name)

        self._set_options()
        print("Okay, let's start")

        while True:
            self._menu()

    def _set_options(self):
        self.options = input().split(",")
        if self.options == [""]:
            self.options = ["rock", "paper", "scissors"]

        self._set_combinations()

    def _menu(self):
        choice = input()

        if choice in self.options:
            self._play(choice)

        elif choice == "!rating":
            print("Your rating:", self.player.rating)

        elif choice == "!exit":
            print("Bye!")
            self.player.save()
            exit()

        else:
            print("Invalid input")

    def _set_combinations(self):
        for index, option in enumerate(self.options):
            interactions = self.options[index + 1 :] + self.options[:index]
            middle = len(interactions) // 2

            self.combinations[option] = {
                "win": interactions[middle:],
                "loss": interactions[:middle],
            }

    def _play(self, user_choice):
        comp_choice = random.choice(self.options)

        if comp_choice in self.combinations[user_choice]["win"]:
            print(f"Well done. The computer chose {comp_choice} and failed")
            self.player.rating += 100

        elif comp_choice == user_choice:
            print(f"There is a draw ({comp_choice})")
            self.player.rating += 50

        else:
            print(f"Sorry, but the computer chose {comp_choice}")


class Player:
    ratings = dict()

    def __init__(self, file_name):
        self.file_name = file_name
        self.name = input("Enter your name: ")
        self.rating = 0

        self._load()

    def _load(self):
        try:
            with open(self.file_name, "r") as f:
                for record in f.readlines():
                    name, rating = record.split()
                    self.ratings[name] = rating
        except FileNotFoundError:
            pass
        finally:
            self.rating = int(self.ratings.get(self.name, 0))

    def save(self):
        self.ratings[self.name] = self.rating
        with open(self.file_name, "w") as f:
            for name, rating in self.ratings.items():
                print(name, rating, file=f)
        pass


def main():
    Game(Player(file_name="rating.txt"))


if __name__ == "__main__":
    main()