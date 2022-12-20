# A COMMAND LINE IMPLEMENTATION OF WORDLE
#### Video Demo:  <https://www.youtube.com/watch?v=tm_stQP5Gtk>
#### Description: 
This is a command line version of wordle developed in Python.
You can play the game as a exe or run the python script.
#### Developer:
Naveen Somasundaram
#### Version: 
Pre-test, 2022 

## Quick Start
### Launching game
- Method 1: **Launch executable**
  - Open wordle.exe by double clicking
  - A terminal window containing the game pops
- Method 2: **Execute the py script**
  - Open command prompt and navigate to game directory
  - Run the python script. For example use the command python ./worlde.py
  - The game starts on your command prompt window

### Save and Load game
**Save** the session by responding with yes to the following question that appears at the end of game.
```
Save current session? (y/n) y
```
The game session is then saved to %APP_DATA%

**Load** the previous session by responding with yes to the following question that appears at the beginning of game.
```
Load previous session? (y/n) y
```
Note that the load question appears only if a valid session data is found in %APP_DATA%.

If you do not wish to load then respond with no as shown below. Which will clear the save data and launch new game.
```
Load previous session? (y/n) n
```
### Game objective
Guess the Word in 6 tries.
- Each guess must be a valid 5 letter word
- Color of the guess tiles will change to show how close the guess is to the word 

### Enabling keyboard
A keyboard to keep track of the guessed letters can be enabled
To do so launch the game with '-k' argument
```
./worlde.exe -k
```
Alternatively, if running the python script
```
python ./worlde.py -k
```
### Game Statistics
At the end of the game your statistics will be displayed where you can see *rounds played*, *win percentage* and *max streak*.

Addition to that *Guess Distribution*, which shows the number of words you have guessed with 1, 2, ... 6 guesses.
Words that weren't guessed are counted under 7+ guesses. 
Note that the bar corresponding to most frequent number of guesses is colored in green.

### Scoring
The scoring is simple.
- 1 point if word is guessed
- 0 if word is not guessed within 6 tries

## Implementation Details for CS50x
#### About the project
The project is basically a command line implementation of the popular game Wordle <https://www.nytimes.com/games/wordle>.
The motivation was to make a version that can be run on command line so it can be played easily between breaks at school/work or at times without internet access.
Considering ease of access, python was the obvious choice to implement the game.
#### Contents
The project contains the following files
- wordle.exe is the exectuable version
- wordle.py contains all the scripts 
- word_list.txt which contains the words 
##### Wordle.py
The is the only script file and contains
- ```class Game``` which has all the game impmentation
- helper functions ```load_game```, ```save_game```, ```resource_path``` to load, save and to locate %APP_DATA% respectively
- ```__main__``` launch script  
###### Intializing a game
The ```class Game``` implementation is intuitive. Initialize the game object for example, ```my_game = Game()```.
You may provide settings during initializtion. For example ```my_game = Game(showAlphabet = showAlphabet)```.
###### Running a round
To run a round call the method ```run_round``` on your object. For example,```my_game.run_round()```

  






