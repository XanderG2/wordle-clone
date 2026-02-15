# Wordle

Wordle-like game built using Python for the console.

## Info

This uses a very long list of words that I got from [dwyl/english-words/words_alpha.txt](https://github.com/dwyl/english-words) (Under Unilicense).

This uses regular wordle rules, with the ability to select length of word.
Includes a version for background colouring (using ANSI escape codes), and a version with plaintext. (for consoles that can't render background colours).
Built using PyInstaller.

## How to build

You can build this using PyInstaller.
On windows you can run `build.bat` which will run the command automatically, building it including the txt file.

The command is this: `py -m PyInstaller --onefile --add-data "allWords.txt;." main_exe.py`
