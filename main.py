# The python version
import os, random, time

clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
clearLine = lambda: print("\033[1A\033[2K\r", end="")

clear()

try:
    with open("allWords.txt", "r") as f:
        words = f.readlines()
except FileNotFoundError:
    exit("No word file found, please ensure you have downloaded the whole project.")

maxLetters = max(map(len, words))

dev = False

while True:
    try:
        letters = input("Please enter the amount of letters in the word you would like to guess:\n> ")
        validWords = []
        if letters != "dev":
            letters = int(letters)
            if not 2 < letters <= maxLetters:
                print(f"Please enter a value between 3 and {maxLetters}.")
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


CORRECT = "\033[42m"       # Green background
WRONG_PLACE = "\033[43m"   # Yellow background
WRONG = "\033[40m"         # Black background
RESET = "\033[0m"          # Reset colour

colors = input(CORRECT + "Can you see the background color? (y/n)" + RESET + "\n> ").lower() in ["y", "yes"]

clear()

while True:
    print("--------- Python Wordle ---------")
    print(f"Selected letters: {letters}")
    print("Dev mode\n" if dev else "")
    word = input("Word: ") if dev else random.choice(validWords)
    while True: # Main game loop
        while True:
            guess = input().strip()
            if len(guess) != letters:
                print("Please guess the correct amount of letters!")
                time.sleep(2)
                clearLine()
                clearLine()
                continue
            if guess not in validWords and not dev:
                print("Please guess an existing word!")
                time.sleep(2)
                clearLine()
                clearLine()
                continue
            break
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
                    truth[i] = "✅"
                    corrects += 1
                    lets[x] -= 1
            for i, x in enumerate(guess): 
                if x in word and lets[x] > 0 and not word[i] == x:
                    truth[i] = "🟨"
                    lets[x] -= 1
                elif not word[i] == x:
                    truth[i] = "❌"
            print("".join(truth))
        if corrects == letters:
            break
    again = input("Well done!\nAgain? (y/n)\n> ") in ["y", "yes"]
    clear()
    if not again:
        break
