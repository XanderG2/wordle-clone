# The python version
import os
import random
import time
import sys
from enum import StrEnum
from collections import Counter
from dataclasses import dataclass


class PlayStatusCode(StrEnum):
    """
    The Enum for the status code returned from `play()`
    """
    NORMAL = "normal"
    GIVE_UP = "give up"
    WON = "won"


class Result(StrEnum):
    """
    The Enum for the correct/wrong/place of a letter
    """
    CORRECT = "C"
    WRONG_PLACE = "W"
    WRONG = "X"


@dataclass
class LetterRequest:
    """
    Return type of `request_letters()`. Contains `letters`,
    `valid_words` and `dev`
    """
    letters: int
    valid_words: list[str]
    dev: bool


@dataclass
class GameConfig:
    """
    Configuration for whole game
    """
    min_letters: int
    max_letters: int
    colors: bool


@dataclass
class RoundConfig:
    """
    Configuration for specific round
    """
    dev: bool
    letters: int


WORD_FILE = "allWords.txt"      # Default word file

CORRECT_ANSI = "\033[42m"       # Green background
WRONG_PLACE_ANSI = "\033[43m"   # Yellow background
WRONG_ANSI = "\033[40m"         # Black background
RESET_ANSI = "\033[0m"          # Reset colour
COLOR_KEY = {
    Result.CORRECT: CORRECT_ANSI,
    Result.WRONG_PLACE: WRONG_PLACE_ANSI,
    Result.WRONG: WRONG_ANSI
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


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for PyInstaller EXE

    :param relative_path: The relative path to the words file
    """
    if getattr(sys, 'frozen', False):
        # temporary folder for PyInstaller
        base_path: str = sys._MEIPASS  # type: ignore
    else:
        base_path: str = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


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
    if os.path.exists(resource_path(default_file_path)):
        return resource_path(default_file_path)

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
        words: list[str],
        config: GameConfig
) -> LetterRequest:
    """
    Ask user for amount of letters in word, will also determin dev mode
      on/off

    :param words: The words in the words file
    :type words: list[str]
    :param config: Info about the game configuration
    :type config: GameConfig
    :return: Instance of `LetterRequest` dataclass containing
      `letters`, `valid_words`, and `dev`.
    :rtype: LetterRequest
    """
    while True:
        letters_input: str = input(
            "Please enter the amount of letters in the word you would like "
            f"to guess ({config.min_letters}-{config.max_letters}):\n> "
        )
        if letters_input == "dev":
            print("Dev mode activated.")
            letters: int = int(input(
                "Please enter the amount of letters in the word you would"
                " like to guess:\n> "
            ))
            return LetterRequest(letters=letters, valid_words=[], dev=True)

        if not letters_input.isdigit():
            print("Please put a number.")
            continue

        letters: int = int(letters_input)

        if letters < config.min_letters or letters > config.max_letters:
            print(
                f"Please enter a value between {config.min_letters} and "
                f"{config.max_letters}."
            )
            continue

        valid_words: list[str] = [x for x in words
                                  if len(x) == letters]

        if len(valid_words) == 0:
            print(f"There are no words {letters} letters long")
            continue

        return LetterRequest(letters=letters,
                             valid_words=valid_words,
                             dev=False
                             )


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


def format_letter(result: Result, letter: str) -> str:
    """
    Format a letter with background colour according to the
    correct/wrong/place indicator

    :param result: The correct/wrong/place of the letter
    :type result: Result
    :param letter: The letter that is being formatted
    :type letter: str
    :return: The formatted letter
    :rtype: str
    """
    return COLOR_KEY[result] + letter + RESET_ANSI


def play(
        game_config: GameConfig,
        round_config: RoundConfig,
        word: str,
        valid_words: list[str],
) -> PlayStatusCode:
    """
    The main part of the game. Returns status code 0-2.
    - 0: Everything is normal, the user has not won or given up.
    - 1: The user has given up.
    - 2: The user has won.

    :param game_config: Info about the game configuration
    :type game_config: GameConfig
    :param round_config: Info about the round configuration
    :type round_config: RoundConfig
    :param word: The word the user is trying to guess
    :type word: str
    :param valid_words: The guessable words
    :type valid_words: list[str]
    :return: Status code
    :rtype: PlayStatusCode
    """
    guess, giveup = validate_guess(
        round_config.letters,
        valid_words,
        round_config.dev
    )

    if giveup:
        return PlayStatusCode.GIVE_UP

    truth: list[Result] = [Result.WRONG] * round_config.letters
    corrects: int = 0

    # useful for yellow marking
    # if word has only 1 of a letter only mark it once, etc.
    num_of_letters: Counter = Counter(word)

    for i, letter in enumerate(guess):
        if word[i] == letter:
            truth[i] = Result.CORRECT
            corrects += 1
            num_of_letters[letter] -= 1

    for i, letter in enumerate(guess):
        if truth[i] is Result.CORRECT:
            continue

        if (letter in word and num_of_letters[letter] > 0):
            truth[i] = Result.WRONG_PLACE
            num_of_letters[letter] -= 1

    if game_config.colors:
        toPrint: list[str] = [""] * len(truth)
        for i, letter in enumerate(guess):
            result = truth[i]
            toPrint[i] = format_letter(result, letter)

        clear_line()
        print("".join(toPrint))
    else:
        print("".join(truth))

    if corrects == round_config.letters:
        return PlayStatusCode.WON

    return PlayStatusCode.NORMAL


def main():
    file_path: str = get_word_file_path(WORD_FILE)
    words: list[str] = get_words(file_path)

    max_letters: int = max(len(word) for word in words)
    min_letters: int = min(len(word) for word in words)
    min_letters = 3 if max_letters > 3 else min_letters

    colors: bool = input(CORRECT_ANSI + "Can you see the background color? (y"
                         "/n)" + RESET_ANSI + "\n> ").lower() in ["y", "yes"]

    clear()

    game_config: GameConfig = GameConfig(
        max_letters=max_letters,
        min_letters=min_letters,
        colors=colors
    )

    playing: bool = True
    while playing:
        lettersInfo: LetterRequest = request_letters(words, game_config)
        valid_words: list[str] = lettersInfo.valid_words
        round_config: RoundConfig = RoundConfig(
            letters=lettersInfo.letters,
            dev=lettersInfo.dev
        )
        clear()
        print("--------- Python Wordle ---------")
        print(f"Selected letters: {round_config.letters}")
        if round_config.dev:
            print("Dev mode")
        print("Type 'giveup' to give up.")
        if not game_config.colors:
            print("C = Correct place   W = Wrong place   X = Not in word")
        print("\n")

        word: str = input(
            "Word: ") if round_config.dev else random.choice(valid_words)
        status: PlayStatusCode = PlayStatusCode.NORMAL

        while status is PlayStatusCode.NORMAL:
            status = play(game_config, round_config, word, valid_words)

        if status is PlayStatusCode.GIVE_UP:
            print("Word was:", word)
        else:
            print("Well done!")

        playing = input("Again? (y/n)\n> ") in ["y", "yes"]
        clear()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("Goodbye!")
        raise SystemExit(0)
