import random
from string import ascii_lowercase


def reveal_word(word, reveal):
    return "".join([letter if letter in reveal else "-" for letter in word])


def validate_guess(guess):
    if len(guess) != 1:
        print("Please, input a single letter")
        return False

    elif guess not in ascii_lowercase:
        print("Please, enter a lowercase English letter")
        return False

    return True


def play(words):
    word = random.choice(words)
    guesses = set()

    lives = 8
    while lives > 0:
        print()

        revealed_word = reveal_word(word, guesses)
        print(revealed_word)

        if word == revealed_word:
            print(f"You guessed the word {word}!\nYou survived!\n")
            break

        guess = input("Input a letter: ")
        if not validate_guess(guess):
            continue

        if guess in guesses:
            print("You've already guessed this letter")
            continue
        elif guess not in word:
            print("No such letter in the word")
            lives -= 1

        guesses.add(guess)
    else:
        print("You lost!\n")


def main():
    words = "python", "java", "kotlin", "javascript"

    print("H A N G M A N")

    while True:
        answer = input('Type "play" to play the game, "exit" to quit: ')

        if answer == "play":
            play(words)
        elif answer == "exit":
            exit()

        continue


if __name__ == "__main__":
    main()
