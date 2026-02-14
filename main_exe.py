# The one in the .EXE
import os, random, time, sys

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

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller EXE"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS # type: ignore # temporary folder for PyInstaller
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def clear() -> None:
    """
    Clear the whole console
    """
    os.system('cls' if os.name=='nt' else 'clear')

def clearLine(n: int = 1) -> None:
    """
    Clear the last `n` lines from the console
    
    :param n: Amount of lines to clear
    :type n: int
    """
    print("\033[1A\033[2K\r"*n, end="")

def getWords(filePath: str) -> list[str]:
    """
    Read words from word file
    
    :param filePath: Word file location
    :type filePath: str
    :return: List of words read from word file
    :rtype: list[str]
    """
    with open(filePath, "r") as file:
        words: list[str] = [word.strip() for word in file]
    
    if len(words) == 0:
        raise SystemExit("No words in word file.")

    return words


def requestLetters(maxLetters: int, minLetters: int, words: list[str]) -> tuple[int, list[str], bool]:
    """
    Ask user for amount of letters in word, will also determin dev mode on/off
    
    :param maxLetters: The length of the longest word in the words file
    :type maxLetters: int
    :param minLetters: The length of the shortest word in the words file
    :type minLetters: int
    :param words: The words in the words file
    :type words: list[str]
    :return: Amount of letters in word, valid words list, developer mode
    :rtype: tuple[int, list[str], bool]
    """
    while True:
        lettersInput: str = input(f"Please enter the amount of letters in the word you would like to guess ({3 if minLetters <3 else minLetters}-{maxLetters}):\n> ")
        if lettersInput != "dev":
            if lettersInput.isdigit():
                letters: int = int(lettersInput)

                if 2 > letters or maxLetters < letters:
                    print(f"Please enter a value between {3 if minLetters <3 else minLetters} and {maxLetters}.")
                    continue

                validWords: list[str] = [x.strip() for x in words if len(x.strip()) == letters]

                if len(validWords) == 0:
                    print(f"There are no words {letters} letters long")
                    continue

                return letters, validWords, False
            
            else:
                print("Please put a number.")
            
        else:
            print("Dev mode activated.")
            letters: int = int(input("Please enter the amount of letters in the word you would like to guess:\n> "))
            return letters, [], True

def validateGuess(letters: int, validWords: list[str], dev: bool) -> tuple[str, bool]:
    """
    Get user's guess, and ensure it is valid. If it is not valid, ask until it is. Will also tell if user has given up.
    
    :param letters: The amount of letters in the word the user is trying to guess
    :type letters: int
    :param validWords: The guessable words
    :type validWords: list[str]
    :param dev: Whether the user is in dev mode or not
    :type dev: bool
    :return: Guess, and give up status
    :rtype: tuple[str, bool]
    """
    while True:
        guess: str = input().strip()

        if guess == "giveup":
            return guess, True
        
        if len(guess) != letters:
            print("Please guess the correct amount of letters!")
            time.sleep(0.75)
            clearLine(2)
            continue
        
        if guess not in validWords and not dev:
            print("Please guess an existing word!")
            time.sleep(0.75)
            clearLine(2)
            continue

        return guess, False

def formatLetter(result: str, letter: str) -> str:
    """
    Format a letter with background colour according to the correct/wrong/place indicator
    
    :param result: `"C"`/`"W"`/`"X"` depending on correct/wrong/place in word
    :type result: str
    :param letter: The letter that is being formatted
    :type letter: str
    :return: The formatted letter
    :rtype: str
    """
    return NONCOLOR_KEY[result] + letter + RESET

def play(colors: bool, letters: int, word: str, validWords: list[str], dev: bool) -> int:
    """
    The main part of the game. Returns status code 0-2.
    - 0: Everything is normal, the user has not won or given up.
    - 1: The user has given up.
    - 2: The user has won.
    
    :param colors: Whether the user's console can render background colors.
    :type colors: bool
    :param letters: Amount of letters in word
    :type letters: int
    :param word: The word the user is trying to guess
    :type word: str
    :param validWords: The guessable words
    :type validWords: list[str]
    :param dev: Whether the user is in dev mode or not
    :type dev: bool
    :return: Status code
    :rtype: int
    """
    guess, giveup = validateGuess(letters, validWords, dev)

    if giveup:
        return 1

    truth: list[str] = [""] * letters
    corrects: int = 0
    numOfLetters: dict[str, int] = {letter: word.count(letter) for letter in set(word)} # useful for yellow marking (if word has only 1 of a letter only mark it once, etc.)

    for i, letter in enumerate(guess):
        if word[i] == letter:
            truth[i] = "C"
            corrects += 1
            numOfLetters[letter] -= 1

    for i, letter in enumerate(guess): 
        if letter in word and numOfLetters[letter] > 0 and not word[i] == letter:
            truth[i] = "W"
            numOfLetters[letter] -= 1
        elif word[i] != letter:
            truth[i] = "X"

    if colors:
        for i, letter in enumerate(guess):
            result = truth[i]
            truth[i] = formatLetter(result, letter)

        clearLine()
        
    print("".join(truth))

    if corrects == letters:
        return 2

    return 0

def main():
    filePath: str = resource_path("allWords.txt")
    words: list[str] = getWords(filePath)

    maxLetters: int = max(len(word) for word in words)
    minLetters: int = min(len(word) for word in words)

    colors: bool = input(CORRECT + "Can you see the background color? (y/n)" + RESET + "\n> ").lower() in ["y", "yes"]

    clear()
    playing = True
    while playing:
        letters, validWords, dev = requestLetters(maxLetters, minLetters, words)

        clear()
        print("--------- Python Wordle ---------")
        print(f"Selected letters: {letters}")
        if dev:
            print("Dev mode")
        print("Type 'giveup' to give up.")
        if not colors:
            print("C = Correct place   W = Wrong place   X = Not in word")
        print("\n")

        word: str = input("Word: ") if dev else random.choice(validWords)
        giveup: bool = False
        status: int = 0

        while not status:
            status = play(colors, letters, word, validWords, dev)
            giveup = status == 1

        if giveup:
            print("Word was:", word)

        playing = input(f"{'Well done!\n' if not giveup else ''}Again? (y/n)\n> ") in ["y", "yes"]
        clear()

if __name__ == "__main__":
    main()