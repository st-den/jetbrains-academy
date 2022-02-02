import random


class ExamApp:
    N_TASKS = 5
    RESULTS_PATH = "results.txt"
    DIFFICULTY_LEVELS = {
        "1": "1 - simple operations with numbers 2-9",
        "2": "2 - integral squares of 11-29",
    }

    def __init__(self):
        self.mark = 0
        self.difficulty = ""

    def start(self):
        self._choose_difficulty()
        self._do_exam()
        self._save_results()

    def _choose_difficulty(self):
        while True:
            print(
                "Which level do you want? Enter a number:",
                *self.DIFFICULTY_LEVELS.values(),
                sep="\n",
            )
            difficulty = input()
            if difficulty in self.DIFFICULTY_LEVELS.keys():
                self.difficulty = difficulty
                break
            print("Incorrect format.")

    def _do_exam(self):
        for _ in range(self.N_TASKS):
            task = self.generate_task(self.difficulty)
            if self.difficulty == "1":
                print(*task)
            elif self.difficulty == "2":
                print(task[0])
            self._do_task(task)
        print(f"Your mark is {self.mark}/{self.N_TASKS}. ", end="")

    def _do_task(self, task: tuple):
        while True:
            try:
                if int(input()) == self.calculate_task(*task):
                    self.mark += 1
                    print("Right!")
                else:
                    print("Wrong!")
                break
            except ValueError:
                print("Wrong format! Try again.")

    def _save_results(self):
        if input(
            "Would you like to save your result to the file? Enter yes or no.\n"
        ).lower() in ("y", "yes"):
            with open(self.RESULTS_PATH, "a+") as f:
                f.write(
                    "{}: {}/{} in level {} ({}).\n".format(
                        input("What is your name?\n"),
                        self.mark,
                        self.N_TASKS,
                        self.difficulty,
                        self.DIFFICULTY_LEVELS[self.difficulty].split(" - ", 1)[1],
                    )
                )
            print(f'The results are saved in "{self.RESULTS_PATH}".')

    @staticmethod
    def generate_task(difficulty: str) -> tuple:
        if difficulty == "1":
            x, y = (random.randint(2, 9) for _ in range(2))
            op = random.choice("+-*")
            return x, op, y
        elif difficulty == "2":
            return random.randint(11, 29), "**", 2
        raise ValueError

    @staticmethod
    def calculate_task(x: int, op: str, y: int) -> int:
        if op == "+":
            return x + y
        elif op == "-":
            return x - y
        elif op == "*":
            return x * y
        elif op == "**":
            return x ** y
        raise ValueError


if __name__ == "__main__":
    ExamApp().start()
