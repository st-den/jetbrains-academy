def show_board(board):
    print("-" * 9)
    for i in range(3):
        print("|", " ".join(board[i]), "|")
    print("-" * 9)


def check_board(board):
    finished = not any(x == "_" for y in board for x in y)
    win = _check_board_win(board)

    if win:
        print(f"{win} wins")
    elif finished:
        print("Draw")
    else:
        return True


def _check_board_win(board):
    variants = (
        (board[0][0], board[1][1], board[2][2]),
        (board[0][2], board[1][1], board[2][0]),
        (board[0][1], board[1][1], board[2][1]),
        (board[0][0], board[0][1], board[0][2]),
        (board[1][0], board[1][1], board[1][2]),
        (board[2][0], board[2][1], board[2][2]),
        (board[0][0], board[1][0], board[2][0]),
        (board[0][1], board[1][1], board[2][1]),
        (board[0][2], board[1][2], board[2][2]),
    )

    if any(v == ("X", "X", "X") for v in variants):
        return "X"
    elif any(v == ("O", "O", "O") for v in variants):
        return "O"

    return False


def main():
    board = [["_"] * 3 for i in range(3)]

    show_board(board)

    player = "X"

    while check_board(board):
        while True:
            coordinates = input("Enter coordinates: > ")

            if coordinates.replace(" ", "").isnumeric():
                x, y = [int(c) for c in coordinates.split()]

                if 0 < x < 4 and 0 < y < 4:
                    real_x, real_y = x - 1, 3 - y

                    if board[real_y][real_x] == "_":
                        board[real_y][real_x] = player

                        player = "O" if player == "X" else "X"
                        break
                    else:
                        print("This cell is occupied! Choose another one!")
                else:
                    print("Coordinates should be from 1 to 3!")
            else:
                print("You should enter numbers!")

        show_board(board)


if __name__ == "__main__":
    main()
