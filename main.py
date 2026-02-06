try:
    with open("allWords.txt", "r") as f:
        words = f.readlines()
except FileNotFoundError:
    exit("No word file found, please ensure you have downloaded the whole project.")


