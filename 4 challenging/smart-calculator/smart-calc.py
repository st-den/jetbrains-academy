import sys
import operator

PRIORITY = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
OPERATOR = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "^": operator.pow,
}


def _is_valid_identifier(identifier: str) -> bool:
    return identifier.isalpha()


def _is_valid_operand(value: str) -> bool:
    return value.isdigit() or _is_valid_identifier(value)


def _infix_to_postfix(tokens: list[str]) -> list[str]:
    postfix, stack = [], []
    for token in tokens:
        if token not in (*PRIORITY, "(", ")"):
            postfix.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack[-1] != "(":
                postfix.append(stack.pop())
            stack.pop()
        elif not stack or stack[-1] == "(":
            stack.append(token)
        else:
            if PRIORITY[token] <= PRIORITY[stack[-1]]:
                postfix.append(stack.pop())
            stack.append(token)
    while stack:
        postfix.append(stack.pop())
    return postfix


def _parse_expr(expr: str) -> list[str]:
    if "//" in expr or "**" in expr or expr.count("(") != expr.count(")"):
        raise ArithmeticError
    return expr.replace("(", " ( ").replace(")", " ) ").split()


def _execute_command(command: str) -> None:
    match command:
        case "/help":
            print("The program calculates blah blah")
        case "/exit":
            print("Bye!")
            sys.exit()
        case _:
            print("Unknown command")


class SmartCalculator:
    memory = dict()

    def process_input(self) -> None:
        if not (inp := input()):
            return

        if inp.startswith("/"):
            _execute_command(inp)
        else:
            try:
                if "=" in inp:
                    self._execute_assignment(inp)
                else:
                    try:
                        print(
                            self._calculate_postfix(_infix_to_postfix(_parse_expr(inp)))
                        )
                    except ArithmeticError:
                        print("Invalid expression")
            except ValueError:
                print("Invalid identifier")
            except KeyError:
                print("Unknown variable")
            except TypeError:
                print("Invalid assignment")

    def _execute_assignment(self, inp: str) -> None:
        args = inp.replace("=", " ", 1).split()
        if not _is_valid_identifier(args[0]):
            raise ValueError
        elif _is_valid_identifier(args[1]) and args[1] not in self.memory:
            raise KeyError
        elif len(args) != 2 or not _is_valid_operand(args[1]):
            raise TypeError
        self.memory[args[0]] = self._parse_identifier(args[1])

    def _calculate_postfix(self, tokens: list[str]) -> int:
        stack = []
        for token in tokens:
            if _is_valid_operand(token):
                stack.append(self._parse_identifier(token))
            elif token in OPERATOR:
                if token in ("-", "/", "^"):
                    x, y = stack.pop(), stack.pop()
                    stack.append(OPERATOR[token](y, x))
                else:
                    stack.append(OPERATOR[token](stack.pop(), stack.pop()))
        return int(stack.pop())

    def _parse_identifier(self, identifier: str) -> int:
        try:
            return int(identifier)
        except ValueError:
            if _is_valid_identifier(identifier):
                return int(self.memory[identifier])
            raise ValueError


def main():
    calc = SmartCalculator()
    while True:
        calc.process_input()


if __name__ == "__main__":
    main()
