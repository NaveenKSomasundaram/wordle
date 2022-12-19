#!/usr/bin/env python
import sys, os, getopt
import math, random
from colorama import Fore, Style, init
import pickle
class Game:
    def __init__(self, fpath:str = "word_list.txt", gamelevel = 'normal', showAlphabet = False, countWrongGuess = False):
        self.score = 0
        self.word_list = self.load_words(resource_path(fpath))
        self.unused_words = list(range(len(self.word_list))) 
        self.guess_limit = 6
        self.num_letters = 5
        self.completed_rounds = 0
        self.guess_statistics = {}
        for i in range(1, self.guess_limit + 2):
            self.guess_statistics[i] = 0 #random.randint(0, 50)
            
        self.colors = {}
        self.colors['match'] = '\x1b[1;37;43m'
        self.colors['exact_match'] = '\x1b[1;37;42m'
        self.colors['no_match'] = '\x1b[1;30;47m'
        self.colors['default'] =  '\x1b[0m'

        self.streak = {}
        self.streak['current'] = 0
        self.streak['best'] = 0
        
        self.game_settings = {}
        self.game_settings['show_alphabet'] = showAlphabet
        self.game_settings['countWrongGuess'] = countWrongGuess
        self.game_settings['level'] = 'normal' # hard or normal
        
        self.version = 0.0
        
    def print_game_intro(self):
        """
        print_game_intro() displays game introduction and help
        """
        rowWidth = 100
        print("")
        game.print_wordle('WORDLE', [1, 0, -1, 1, -1, -1])
        print("")
        print(''.center(rowWidth, '-'))
        print("Guess the Word in " + str(self.guess_limit) + " tries.")
        print(" - Each guess must be a valid 5-letter word.") 
        print(" - Color of guess tiles will change to show how close the guess is to the word.") 
        
        print("Example ")
        print("If word is PLANE and guess is SPADE then it appears as")
        self.print_wordle("SPADE", [-1, 0, 1, -1, 1])
        print("")
        print("A and E are in the right position, P is in word but in the wrong position")
        print("")
        print("Use command line argumetn -k to display keyboard")
        print("Example ")
        print("If word is PLANE and guess is PILLS the keyboard shows")
        print("a b c d e f g h   j k [l] m n o [p] q r  t u v w x y z")
        print("i and s are removed as they are not present in word")
        print("l and p are shown in [] as they are present in word")
        print(''.center(rowWidth, '-'))
        
    def print_game_statistics(self):
    
        # Some print settings
        colWidth = 10 
        tableWidth =  (colWidth * 3) + 5
        
        print('') 
        print('GAME STATISTICS'.center(tableWidth, '*'))
        rounds_won = 0
        rounds_played = 0
        min_max_guess = 1
        for i in range(1, self.guess_limit + 2):
            rounds_played += self.guess_statistics[i]
            if i <= self.guess_limit:
                rounds_won += self.guess_statistics[i]
            if self.guess_statistics[i] > self.guess_statistics[min_max_guess]:
                min_max_guess = i
        
        
        print('Played'.center(colWidth) + 'Win %'.center(colWidth) +  'Max Streak'.center(colWidth))
        win_percentage = math.ceil(100 * (rounds_won / rounds_played))
        print(str(rounds_played).center(colWidth) + str(win_percentage).center(colWidth) + str(self.streak['best']).center(colWidth))
        
        print('')
        print('Guess Distribution'.center(tableWidth))
        rowLabelWidth = math.ceil(math.log10(self.guess_limit + 1) + 2)
        maxBars = tableWidth - 2 * rowLabelWidth 
        for i in range(1, self.guess_limit + 2):
            numBars = math.ceil(maxBars * (self.guess_statistics[i]/self.guess_statistics[min_max_guess]))
            barColor = self.colors['exact_match'] if (i == min_max_guess) else self.colors['no_match']
            
            rowLabel = (str(i) + '+' * (i == (self.guess_limit + 1))).ljust(rowLabelWidth)
            print(rowLabel + barColor +  ' '  * numBars  + self.colors['default']  + str(self.guess_statistics[i]))
        
        print(''.center(tableWidth, '*'))        
        return
          
    @staticmethod    
    def load_words(fpath):
        if not os.path.isfile(fpath):
            print('Error. Provide a valid file path for word list.')
            sys.exit()
        try:
            f = open(fpath)
            words = f.read().split('\n')
            words.pop(-1)
        except:
            print('Unable to load file ' + fpath)
            sys.exit()
        
        #self.word_list = words 
        
        if len(words) == 0:
            print("Word list is empty!")
            sys.exit()
        
        # TODO: check of words
        checked_words = []
        for w in words:
            if w.isalpha():
                if checked_words:
                    if len(checked_words[0]) == len(w):
                        checked_words.append(w)
                else:
                    checked_words.append(w)
            
       
        return words 
      
    @staticmethod
    def check_word(guess, curr_word):
        """
            check_word checks the guess against curr_word and returns status array.
            status is an array of length len(guess). 
            status[i] = 1 if guess[i] is present in curr_word at the same location
            status[i] = 0 if guess[i] is present in curr_word
            status[i] = -1 if guess[i] is not present in curr_word 
            
            Note:
                Look up wordle to see how status handles clashes 
        """
        if len(curr_word) != len(guess):
            print("length of guess and word to compare is not same!")
            sys.exit()
        
        # Convert to lower case for comparison
        curr_word = curr_word.lower()
        guess = guess.lower()
        
        n = len(curr_word)
        
        status = [-1] * n
        for i in range(n):
            if curr_word[i] == guess[i]:
                status[i] = 1

        for i in range(n):
            # Skip if letter is already found
            if status[i] == 1:
                continue
                
            for j in range(n):
                # Skip if letter is already used
                if status[j] != -1:
                    continue
                # Set to 0 if letter found in guess
                if curr_word[i] == guess[j]:
                    status[j] = 0 
                    break 
                 
        return status
    
    def print_wordle(self, word, status):
        """
        Function to print word in the wordle format where the letter color is determined by status.
        """
        word = word.upper()
        colors = {0: '\x1b[1;37;43m', 1: '\x1b[1;37;42m', -1 : '\x1b[1;37;40m'}
        for i in range(len(word)):
            if status[i] == 0:
                print(self.colors['match'] + ' ' + word[i] + ' ' + self.colors['default'], end = "")  
            elif status[i] == 1:
                print(self.colors['exact_match'] + ' ' + word[i] + ' ' + self.colors['default'], end = "") 
            else:
                print(self.colors['no_match'] + ' ' + word[i] + ' ' + self.colors['default'], end = "") 
        print(" ", end = "")   
        return
    
    def print_alphabet_status(self, status):
        """
        Function to print alphabet list a-z differentiated by status value
        status[i] represents the status of chr(97 + i)
        i.e. status[0] represents a, status[1] represents b and so on.
        status[i] = -1 implies chr(97 + i) is guessed and not in word
        status[i] =  0 implies chr(97 + i) is not guessed yet
        status[i] = +1 implies chr(97 + i) is guessed and present in word
        """
        if not self.game_settings['show_alphabet']:
            return
        for i in range(len(status)):
            # not guesed show lowercase
            if status[i] == 0: 
                print(self.colors['default'] + ' ' + chr(i + 97) + ' ' + self.colors['default'], end = "") 
            # gussed and present in word - show lowercase within []
            elif status[i] == 1: 
                print(self.colors['default'] + '[' + chr(i + 97) + ']' + self.colors['default'], end = "")                
            # guessed and not present - don't show letter
            else:
                print(self.colors['default'] + '   ' + self.colors['default'], end = "")
        print(self.colors['default'] + "  ", end = "")    
        return
    
    def round_end_message(self, num_guesses):
        """
        Returns string for round end message depending on number of guesses
        """
        if num_guesses > self.guess_limit:
            return random.choice(["Uh-oh! It was ", ":| ", "... ", "Gotcha! The word is "]) 
        if num_guesses == 1:
            return random.choice(["GODLIKE!", "SAVAGE!", "Feeling lucky?!"])
        if num_guesses in [2, 3]:
            return random.choice(["Excellent!", "Superb!", "Impeccable!", "G3N1U5"])
        if num_guesses == [4, 5]:
            return random.choice(["Way to go!", "Good job!", "Impressive"])
        else:
            return random.choice(["Phew!", ":)", "You made it!", "Living dangerously?!"])
    
    def run_round(self):
        """
        Function to run a worlde round
        """
        if len(self.unused_words) == 0:
            print("Word list completed!")
            sys.exit()
            
        ind = random.randint(0, len(self.unused_words))
        self.unused_words.pop(ind)
        curr_word = self.word_list[ind]
        curr_guess = "-" * self.num_letters
        guesses = []
        alphabet_status = [0] * 26
        status = self.check_word(curr_guess, curr_word)
        
        print('\nROUND #{}'.format(self.completed_rounds + 1))
        
        # Get guesses from user
        # i is the guess number
        for i in range(self.guess_limit):
            
            self.print_wordle(curr_guess, status)
            self.print_alphabet_status(alphabet_status)
            
            curr_guess = input('Guess ' + str(i + 1) + ':').lower()    
            while(curr_guess not in self.word_list):
                self.print_wordle("-" * self.num_letters, [-1] * self.num_letters)
                self.print_alphabet_status(alphabet_status)
                print('Invalid word. Try a new word!')
                self.print_wordle("-" * self.num_letters, [-1] * self.num_letters)
                if self.game_settings['show_alphabet']:
                    self.print_alphabet_status(alphabet_status)
                
                curr_guess = input('Guess ' + str(i + 1) + ':').lower()
                
            while(curr_guess in guesses):
                self.print_wordle("-" * self.num_letters, [-1] * self.num_letters)
                self.print_alphabet_status(alphabet_status)
                print('Already guessed word. Try a new word!')
                self.print_wordle("-" * self.num_letters, [-1] * self.num_letters)
                if self.game_settings['show_alphabet']:
                    self.print_alphabet_status(alphabet_status)
                
                curr_guess = input('Guess ' + str(i + 1) + ':').lower()
            
            status = self.check_word(curr_guess, curr_word)
            
            for jj in range(len(status)):
                if (alphabet_status[ord(curr_guess[jj]) - ord('a')]) != 1:
                    alphabet_status[ord(curr_guess[jj]) - ord('a')] = -1 if status[jj] == -1 else 1
                    
                    
            
            # Store guess in guesses
            guesses.append(curr_guess)
            
            # Exit if word is guessed
            if sum(status) == len(status):
                break
        
        self.print_wordle(curr_guess, status)
        if sum(status) == len(status):
            print(self.round_end_message(len(guesses)))
            self.score += 1
            self.guess_statistics[i + 1] += 1
            self.streak['current'] += 1
            self.streak['best'] = max(self.streak['best'], self.streak['current'])
        else:
            status = self.check_word(curr_word, curr_word)
            #print("")
            #self.print_wordle(curr_word, status)
            print(self.round_end_message(len(guesses) + 1) + curr_word)
            self.guess_statistics[i + 2] += 1
            self.streak['current'] = 0

        print('\nSCORE:', self.score)
        
        # Update rounds counter
        self.completed_rounds += 1
        return
      
def load_game(fPath):
    
    if os.path.exists(fPath):
        with open(fPath , 'rb') as f:
            game, meta_data = pickle.load(f)
            if not isinstance(game, Game):
                game = None
            else:
                inp = ''
                while(inp not in ['y', 'n']):
                    inp = input("Continue previous session? (y/n) ").lower()
                if inp == 'n':
                    game = None
    else:
        game = None
    return game 
 
def save_game(fPath, game):
    try:
        with open(fPath, 'wb') as f:
            meta_data = {}
            meta_data['game_version'] = game.version
        
            pickle.dump([game, meta_data], f, protocol=2)
        print('Session data saved successfully!')
    except:
        print('Session data could not be saved!')
        sys.exit()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    # From stack exchange https://stackoverflow.com/questions/51060894/adding-a-data-file-in-pyinstaller-using-the-onefile-option
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
 
if __name__ == "__main__":
    init(convert=True) # For color purpose
    
    # Argument parse
    args = sys.argv[1:]
    showAlphabet = False 
    for i in range(len(args)):
        if args[i] == '-k':
            showAlphabet = True 
    
    # Load previous state if possible
    savedfPath = 'savefile.dat'
    game = load_game(savedfPath)
    
    if game == None:
        game = Game(showAlphabet = showAlphabet)
    
    # Use current settings on the saved state
    game.game_settings['show_alphabet'] = showAlphabet
    game.print_game_intro()

    # TODO: Build handling of command arguments
    # TODO: Win / Loss message variations
    # TODO: Hard mode implementation - Not needed
    # TODO: User registration - replaced with load state
    
    
      
    continueRound = 'y'
    while(continueRound.lower() == 'y'):
        game.run_round()
        continueRound = ''
        while(continueRound not in ['y', 'n']):
            continueRound = input("Continue? (y/n) ")
        
    
    # print statistics
    game.print_game_statistics()
    
    # Save game
    save_game(savedfPath, game)
    
    while(input("Press any key to exit")):
        quit
        
