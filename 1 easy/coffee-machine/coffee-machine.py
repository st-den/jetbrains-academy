class CoffeeMachine:
    buy_menu = {
        1: {
            "consumables": {"water": 250, "milk": 0, "beans": 16, "cups": 1},
            "money": 4,
        },
        2: {
            "consumables": {"water": 350, "milk": 75, "beans": 20, "cups": 1},
            "money": 7,
        },
        3: {
            "consumables": {"water": 200, "milk": 100, "beans": 12, "cups": 1},
            "money": 6,
        },
    }

    def __init__(self, water, milk, beans, cups, money):
        self.inventory = {
            "consumables": {"water": water, "milk": milk, "beans": beans, "cups": cups},
            "money": money,
        }

    def menu(self):
        while True:
            action = input("Write action (buy, fill, take, remaining, exit):\n")
            print()
            if action == "buy":
                self._buy()
            elif action == "fill":
                self._fill()
            elif action == "take":
                self._take()
            elif action == "remaining":
                self._show_status()
            elif action == "exit":
                exit()
            print()

    def _buy(self):
        choice = input(
            "What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n"
        )

        if choice == "back":
            return
        else:
            choice = int(choice)

        for k, v in self.buy_menu[choice]["consumables"].items():
            if self.inventory["consumables"][k] < v:
                print(f"Sorry, not enough {k}!")
                return

        print("I have enough resources, making you a coffee!")

        self.inventory["consumables"].update(
            (k, self.inventory["consumables"][k] - v)
            for k, v in self.buy_menu[choice]["consumables"].items()
        )
        self.inventory["money"] += self.buy_menu[choice]["money"]

    def _fill(self):
        self.inventory["consumables"]["water"] += int(
            input("Write how many ml of water do you want to add:\n")
        )
        self.inventory["consumables"]["milk"] += int(
            input("Write how many ml of milk do you want to add:\n")
        )
        self.inventory["consumables"]["beans"] += int(
            input("Write how many grams of coffee beans do you want to add:\n")
        )
        self.inventory["consumables"]["cups"] += int(
            input("Write how many disposable cups of coffee do you want to add:\n")
        )

    def _take(self):
        print(f"I gave you ${self.inventory['money']}")
        self.inventory["money"] = 0

    def _show_status(self):
        print(
            f"The coffee machine has:",
            f"{self.inventory['consumables']['water']} of water",
            f"{self.inventory['consumables']['milk']} of milk",
            f"{self.inventory['consumables']['beans']} of coffee beans",
            f"{self.inventory['consumables']['cups']} of disposable cups",
            f"{self.inventory['money']} of money",
            sep="\n",
        )


def main():
    CoffeeMachine(400, 540, 120, 9, 550).menu()


if __name__ == "__main__":
    main()