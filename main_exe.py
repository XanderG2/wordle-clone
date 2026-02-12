# The one in the .EXE
import os, random, time, sys

clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
clearLine = lambda: print("\033[1A\033[2K\r", end="")

clear()


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller EXE"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

with open(resource_path("allWords.txt"), "r") as f:
    words = [x.strip() for x in f.readlines()]

maxLetters = max(map(len, words))
minLetters = min(map(len, words))

dev = False


CORRECT = "\033[42m"       # Green background
WRONG_PLACE = "\033[43m"   # Yellow background
WRONG = "\033[40m"         # Black background
RESET = "\033[0m"          # Reset colour

colors = input(CORRECT + "Can you see the background color? (y/n)" + RESET + "\n> ").lower() in ["y", "yes"]

clear()

while True:
    while True:
        try:
            letters = input(f"Please enter the amount of letters in the word you would like to guess ({3 if minLetters <3 else minLetters}-{maxLetters}):\n> ")
            validWords = []
            if letters != "dev":
                dev = False
                letters = int(letters)
                if not 2 < letters <= maxLetters:
                    print(f"Please enter a value between {3 if minLetters <3 else minLetters} and {maxLetters}.")
                    continue
                validWords = [x.strip() for x in words if len(x.strip()) == letters]
                if len(validWords) == 0:
                    print(f"There are no words {letters} letters long")
            else:
                print("Dev mode activated.")
                dev = True
                letters = int(input("Please enter the amount of letters in the word you would like to guess:\n> "))
            break
        except ValueError:
            print("Please put a number.")
    clear()
    print("--------- Wordle ---------")
    print(f"Selected letters: {letters}")
    print("Dev mode\n" if dev else "", end="")
    print("Type \"giveup\" to give up.")
    print("C = Correct place   W = Wrong place   X = Not in word" if not colors else "", end="\n\n")
    word = input("Word: ") if dev else random.choice(validWords)
    giveup = False
    while True: # Main game loop
        while True:
            guess = input().strip()
            if guess == "giveup":
                giveup = True
            elif len(guess) != letters:
                print("Please guess the correct amount of letters!")
                time.sleep(2)
                clearLine()
                clearLine()
                continue
            elif guess not in validWords and not dev:
                print("Please guess an existing word!")
                time.sleep(2)
                clearLine()
                clearLine()
                continue
            break
        if giveup: break
        if colors:
            clearLine()
            truth = ["" for i in range(letters)]
            corrects = 0
            lets = {w: a for w, a in zip(word, [word.count(x) for x in word])} # word: appearences // useful for yellow marking (if word has only 1 of a
            for i, x in enumerate(guess):                                                                                       # letter only mark it once, etc.)
                if word[i] == x:
                    truth[i] = CORRECT + x + RESET
                    corrects += 1
                    lets[x] -= 1
            for i, x in enumerate(guess): 
                if x in word and lets[x] > 0 and not word[i] == x:
                    truth[i] = WRONG_PLACE + x + RESET
                    lets[x] -= 1
                elif not word[i] == x:
                    truth[i] = WRONG + x + RESET
            print("".join(truth))
        else:
            truth = ["" for i in range(letters)]
            corrects = 0
            lets = {w: a for w, a in zip(word, [word.count(x) for x in word])} # word: appearences // useful for yellow marking (if word has only 1 of a
            for i, x in enumerate(guess):                                                                                       # letter only mark it once, etc.)
                if word[i] == x:
                    truth[i] = "C"
                    corrects += 1
                    lets[x] -= 1
            for i, x in enumerate(guess): 
                if x in word and lets[x] > 0 and not word[i] == x:
                    truth[i] = "W"
                    lets[x] -= 1
                elif not word[i] == x:
                    truth[i] = "X"
            print("".join(truth))
        if corrects == letters:
            break
    if giveup: print("Word was:", word)
    again = input(f"{'Well done!\n' if not giveup else ''}Again? (y/n)\n> ") in ["y", "yes"]
    clear()
    if not again:
        break