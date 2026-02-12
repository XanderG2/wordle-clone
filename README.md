# Wordle

Wordle-like game built using Python for the console.

## Info

This uses a very long list of words that I got from [dwyl/english-words/words_alpha.txt](https://github.com/dwyl/english-words) (Under Unilicense).

This uses regular wordle rules, with the ability to select length of word.
Includes a version for background colouring (using ANSI escape codes), and a version with plaintext. (for consoles that can't render background colours).
Built using PyInstaller.

- `main.py` is the python version, meant to be run as a python program. You can run either but this version is recommended for just python.
- `main_exe.py` is the version that is turned into the .exe file. It includes a different way of finding the word file, which is useful for the .exe, where it is bundled in.

## How to build

You can build this using PyInstaller.
On windows you can run `build.bat` which will run the command automatically, building it including the txt file.

The command is this: `py -m PyInstaller --onefile --add-data "allWords.txt;." main_exe.py`
