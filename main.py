# The python version
import os
import random
import time

WORD_FILE = "allWords.txt"
CORRECT = "\033[42m"       # Green background
WRONG_PLACE = "\033[43m"   # Yellow background
WRONG = "\033[40m"         # Black background
RESET = "\033[0m"          # Reset colour
NONCOLOR_KEY = {
    "C": CORRECT,
    "W": WRONG_PLACE,
    "X": WRONG
}


def clear() -> None:
    """
    Clear the whole console
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def clear_line(n: int = 1) -> None:
    """
    Clear the last `n` lines from the console

    :param n: Amount of lines to clear
    :type n: int
    """
    print("\033[1A\033[2K\r"*n, end="")


def get_words(file_path: str) -> list[str]:
    """
    Read words from word file

    :param file_path: Word file location
    :type file_path: str
    :return: List of words read from word file
    :rtype: list[str]
    """
    with open(file_path, "r") as file:
        words: list[str] = [word.strip() for word in file]

    if len(words) == 0:
        raise SystemExit("No words in word file.")

    return words


def get_word_file_path(default_file_path: str) -> str:
    """
    Get the file_path of the words file

    :param default_file_path: The default file path this should assume
        exists, if it doesnt exist, it will ask the user to select a
        different .txt file.
    :type default_file_path: str
    :return: file_path of words file
    :rtype: str
    """
    if os.path.exists(default_file_path):
        return default_file_path

    print(f"No word file found. The default words file name is {WORD_FILE}")

    path = "."
    files = [f for f in os.listdir(path)
             if f.endswith(".txt")
             and os.path.isfile(os.path.join(path, f))
             ]

    print("All text files found in current directory:")
    for i, file in enumerate(files):
        print(f"{i}. {file}")

    file = input("If your word file is one of these, please enter the "
                 "number, if it is not, please put it into the current "
                 "folder and retry (press enter).\n> ")
    if file.isdigit():
        file = int(file)
        if not 0 <= file < len(files):
            raise SystemExit("Please type a number in the list.")
    elif file.strip() != "":
        raise SystemExit("Please type a number in the list.")
    else:
        raise SystemExit("Please add word file to directory.")

    return files[file]


def request_letters(
        max_letters: int,
        min_letters: int,
        words: list[str]
) -> tuple[int, list[str], bool]:
    """
    Ask user for amount of letters in word, will also determin dev mode
      on/off

    :param max_letters: The length of the longest word in the words
      file
    :type max_letters: int
    :param min_letters: The length of the shortest word in the words
      file
    :type min_letters: int
    :param words: The words in the words file
    :type words: list[str]
    :return: Amount of letters in word, valid words list, developer
      mode
    :rtype: tuple[int, list[str], bool]
    """
    while True:
        letters_input: str = input(
            "Please enter the amount of letters in the word you would like "
            f"to guess ({min_letters}-{max_letters}):\n> "
        )
        if letters_input == "dev":
            print("Dev mode activated.")
            letters: int = int(input(
                "Please enter the amount of letters in the word you would"
                " like to guess:\n> "
            ))
            return letters, [], True

        if not letters_input.isdigit():
            print("Please put a number.")
            continue

        letters: int = int(letters_input)

        if letters < min_letters or letters > max_letters:
            print(
                f"Please enter a value between {min_letters} and "
                f"{max_letters}."
            )
            continue

        valid_words: list[str] = [x for x in words
                                  if len(x) == letters]

        if len(valid_words) == 0:
            print(f"There are no words {letters} letters long")
            continue

        return letters, valid_words, False


def validate_guess(
        letters: int,
        valid_words: list[str],
        dev: bool
) -> tuple[str, bool]:
    """
    Get user's guess, and ensure it is valid. If it is not valid, ask
    until it is. Will also tell if user has given up.

    :param letters: The amount of letters in the word the user is
      trying to guess
    :type letters: int
    :param valid_words: The guessable words
    :type valid_words: list[str]
    :param dev: Whether the user is in dev mode or not
    :type dev: bool
    :return: Guess, and give up status
    :rtype: tuple[str, bool]
    """
    while True:
        guess: str = input().strip().lower()

        if guess == "giveup":
            return guess, True

        if len(guess) != letters:
            print("Please guess the correct amount of letters!")
            time.sleep(0.75)
            clear_line(2)
            continue

        if guess not in valid_words and not dev:
            print("Please guess an existing word!")
            time.sleep(0.75)
            clear_line(2)
            continue

        return guess, False


def format_letter(result: str, letter: str) -> str:
    """
    Format a letter with background colour according to the
    correct/wrong/place indicator

    :param result: `"C"`/`"W"`/`"X"` depending on correct/wrong/place
      in word
    :type result: str
    :param letter: The letter that is being formatted
    :type letter: str
    :return: The formatted letter
    :rtype: str
    """
    return NONCOLOR_KEY[result] + letter + RESET


def play(
        colors: bool,
        letters: int,
        word: str,
        valid_words: list[str],
        dev: bool
) -> int:
    """
    The main part of the game. Returns status code 0-2.
    - 0: Everything is normal, the user has not won or given up.
    - 1: The user has given up.
    - 2: The user has won.

    :param colors: Whether the user's console can render background
      colors.
    :type colors: bool
    :param letters: Amount of letters in word
    :type letters: int
    :param word: The word the user is trying to guess
    :type word: str
    :param valid_words: The guessable words
    :type valid_words: list[str]
    :param dev: Whether the user is in dev mode or not
    :type dev: bool
    :return: Status code
    :rtype: int
    """
    guess, giveup = validate_guess(letters, valid_words, dev)

    if giveup:
        return 1

    truth: list[str] = [""] * letters
    corrects: int = 0
    # useful for yellow marking
    # if word has only 1 of a letter only mark it once, etc.
    num_of_letters: dict[str, int] = {
        letter: word.count(letter) for letter in set(word)
    }

    for i, letter in enumerate(guess):
        if word[i] == letter:
            truth[i] = "C"
            corrects += 1
            num_of_letters[letter] -= 1

    for i, letter in enumerate(guess):
        if (letter in word and num_of_letters[letter] > 0 and
                not word[i] == letter):
            truth[i] = "W"
            num_of_letters[letter] -= 1
        elif word[i] != letter:
            truth[i] = "X"

    if colors:
        for i, letter in enumerate(guess):
            result = truth[i]
            truth[i] = format_letter(result, letter)

        clear_line()

    print("".join(truth))

    if corrects == letters:
        return 2

    return 0


def main():
    file_path: str = get_word_file_path(WORD_FILE)
    words: list[str] = get_words(file_path)

    max_letters: int = max(len(word) for word in words)
    min_letters: int = min(len(word) for word in words)
    min_letters = 3 if max_letters > 3 else min_letters

    colors: bool = input(CORRECT + "Can you see the background color? (y/n)" +
                         RESET + "\n> ").lower() in ["y", "yes"]

    clear()
    playing = True
    while playing:
        letters, valid_words, dev = request_letters(
            max_letters, min_letters, words)

        clear()
        print("--------- Python Wordle ---------")
        print(f"Selected letters: {letters}")
        if dev:
            print("Dev mode")
        print("Type 'giveup' to give up.")
        if not colors:
            print("C = Correct place   W = Wrong place   X = Not in word")
        print("\n")

        word: str = input("Word: ") if dev else random.choice(valid_words)
        giveup: bool = False
        status: int = 0

        while not status:
            status = play(colors, letters, word, valid_words, dev)
            giveup = status == 1

        if giveup:
            print("Word was:", word)
        else:
            print("Well done!")
        playing = input("Again? (y/n)\n> ") in ["y", "yes"]
        clear()


if __name__ == "__main__":
    main()
