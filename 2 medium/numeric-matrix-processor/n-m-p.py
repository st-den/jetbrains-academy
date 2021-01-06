class IllegalDimensionsError(Exception):
    pass


class Matrix:
    def __init__(
        self,
        M=None,
        rows=None,
        cols=None,
        size_message="Enter matrix size: ",
        matrix_message="Enter matrix:",
    ):
        self.M, self.rows, self.cols = (
            ((M, len(M), len(M[0])) if not rows and not cols else (M, rows, cols))
            if M
            else self._get_matrix(size_message, matrix_message)
        )
        self.is_square = all(self.rows == len(row) for row in self.M)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            if self.rows == other.rows and self.cols == other.cols:
                return self.__class__(
                    [
                        list(map(sum, zip(self[row], other[row])))
                        for row in range(self.rows)
                    ]
                )
            else:
                raise IllegalDimensionsError()

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            if self.cols == other.rows:
                return self.__class__(
                    [
                        [
                            sum(self[row][i] * other[i][col] for i in range(self.cols))
                            for col in range(other.cols)
                        ]
                        for row in range(self.rows)
                    ],
                    self.rows,
                    other.cols,
                )
            else:
                raise IllegalDimensionsError()

        elif isinstance(other, int) or isinstance(other, float):
            return self.__class__(
                [[el * other for el in self[row]] for row in range(self.rows)],
                self.rows,
                self.cols,
            )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __getitem__(self, row):
        return self.M[row]

    def __len__(self):
        return len(self.M)

    def __repr__(self):
        return str(self.M)

    def __str__(self):
        M_truncated = [
            [str(int(el) if el.is_integer() else round(el, 3)) for el in row]
            for row in self.M
        ]
        width = len(max([el for row in M_truncated for el in row], key=len))

        return "\n".join(
            [" ".join([el.rjust(width) for el in row]) for row in M_truncated]
        )

    def determinant(self):
        if self.is_square:
            if self.rows == 2:
                return self[0][0] * self[1][1] - self[0][1] * self[1][0]
            elif self.rows == 1:
                return self[0][0]
            else:
                return sum(
                    (-1) ** (col)
                    * self[0][col]
                    * self.__class__.determinant(self._minor(0, col))
                    for col in range(self.cols)
                )
        else:
            raise IllegalDimensionsError()

    def inverse(self):
        C = self.__class__(
            [
                [
                    (-1) ** (row + col)
                    * (
                        self._minor(row, col).determinant()
                        if self.rows > 1
                        else self.determinant()
                    )
                    for col in range(self.cols)
                ]
                for row in range(self.rows)
            ]
        )
        M_det = sum(a * b for a, b in zip(self[0], C[0]))
        return (
            1 / M_det * C.transpose()
        )  # !NOTE: ZeroDivisionError must be handled externally

    def transpose(self, mode="main diagonal"):
        if mode == "main diagonal":
            return self.__class__([*(zip(*self))])
        elif mode == "side diagonal":
            return self.__class__(list(reversed([*(zip(*reversed(self)))])))
        elif mode == "vertical line":
            return self.__class__([list(reversed(row)) for row in self])
        elif mode == "horizontal line":
            return self.__class__(list(reversed(self)))

    def _get_matrix(self, size_message, matrix_message):
        rows, cols = map(int, input(size_message).split())
        print(matrix_message)
        M = [list(map(float, input().split())) for _ in range(rows)]

        return M, rows, cols

    def _minor(self, el_row, el_col):
        return self.__class__(
            [
                row[:el_col] + row[el_col + 1 :]
                for row in self[:el_row] + self[el_row + 1 :]
            ]
        )


def menu():
    result = print(
        "1. Add matrices",
        "2. Multiply matrix by a constant",
        "3. Multiply matrices",
        "4. Transpose matrix",
        "5. Calculate a determinant",
        "6. Inverse matrix",
        "0. Exit",
        sep="\n",
    )
    choice = int(input("Your choice: "))

    if choice == 1 or choice == 3:
        M1, M2 = Matrix(
            size_message="Enter size of first matrix: ",
            matrix_message="Enter first matrix:",
        ), Matrix(
            size_message="Enter size of second matrix: ",
            matrix_message="Enter second matrix:",
        )

        result = M1 + M2 if choice == 1 else M1 * M2

    elif choice == 2:
        result = Matrix() * float(input("Enter constant: "))

    elif choice == 4:
        print(
            "\n1. Main diagonal",
            "2. Side diagonal",
            "3. Vertical line",
            "4. Horizontal line",
            sep="\n",
        )
        mode = int(input("Your choice: "))

        result = Matrix().transpose(
            mode={
                1: "main diagonal",
                2: "side diagonal",
                3: "vertical line",
                4: "horizontal line",
            }[mode]
        )

    elif choice == 5:
        result = Matrix().determinant()
        if result.is_integer():
            result = int(result)

    elif choice == 6:
        result = Matrix().inverse()

    else:
        exit()

    print("The result is:", result, sep="\n")


def main():
    while True:
        try:
            menu()
        except IllegalDimensionsError:
            print("The operation cannot be performed.")
        except ZeroDivisionError:
            print("This matrix doesn't have an inverse.")
        print()


if __name__ == "__main__":
    main()
