class HonestCalculator:
    messages = [
        "Enter an equation",
        "Do you even know what numbers are? Stay focused!",
        "Yes ... an interesting math operation. You've slept through all classes, haven't you?",
        "Yeah... division by zero. Smart move...",
        "Do you want to store the result? (y / n):",
        "Do you want to continue calculations? (y / n):",
        " ... lazy",
        " ... very lazy",
        " ... very, very lazy",
        "You are",
        "Are you sure? It is only one digit! (y / n)",
        "Don't be silly! It's just one number! Add to the memory? (y / n)",
        "Last chance! Do you really want to embarrass yourself? (y / n)",
    ]

    x: float
    y: float
    op: str
    res: float
    mem: float

    def __init__(self):
        self.mem = 0

    def start(self):
        while True:
            if self.get_input():
                self.check()

                if self.op == "/" and self.y == 0:
                    print(self.messages[3])
                    continue
                self.calculate()

                self.update_memory()

                answer = print(self.messages[5])
                while answer not in ("y", "n"):
                    answer = input()

                if answer == "n":
                    break

    def get_input(self):
        print(self.messages[0])

        x, self.op, y = input().split()

        if x == "M":
            x = self.mem
        if y == "M":
            y = self.mem

        try:
            self.x, self.y = float(x), float(y)
        except ValueError:
            return print(self.messages[1])

        if self.op not in "+-*/":
            return print(self.messages[2])

        return True

    def calculate(self):
        if self.op == "+":
            self.res = self.x + self.y
        elif self.op == "-":
            self.res = self.x - self.y
        elif self.op == "*":
            self.res = self.x * self.y
        elif self.op == "/":
            self.res = self.x / self.y

        print(self.res)

    def check(self):
        msg = ""
        if self.is_one_digit(self.x) and self.is_one_digit(self.y):
            msg = "".join([msg, self.messages[6]])
        if (self.x == 1 or self.y == 1) and self.op == "*":
            msg = "".join([msg, self.messages[7]])
        if (self.x == 0 or self.y == 0) and self.op in "*+-":
            msg = "".join([msg, self.messages[8]])

        if msg:
            print("".join([self.messages[9], msg]))

    def update_memory(self):
        print(self.messages[4])

        answer = input()
        while answer != "n":
            if answer == "y":
                if self.is_one_digit(self.res):
                    msg_index = 10
                    while msg_index < 13:
                        print(self.messages[msg_index])

                        answer = input()
                        if answer == "y":
                            msg_index += 1
                        elif answer == "n":
                            return

                self.mem = self.res
                return

    @staticmethod
    def is_one_digit(n: float):
        return -10 < n < 10 and n.is_integer()


if __name__ == "__main__":
    HonestCalculator().start()
