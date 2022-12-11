import sys, os, getopt
import math, random
from colorama import Fore, Style, init

class Game:
    def __init__(self, fpath:str = "./word_list.txt", gamelevel = 'normal', showAlphabet = False, countWrongGuess = False):
        self.score = 0
        self.word_list = self.load_words(fpath)
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
    
    def print_game_statistics(self):
    
        # Some print settings
        colWidth = 10 
        tableWidth =  (colWidth * 3) + 5
        
        
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
            quit()
        try:
            f = open(fpath)
            words = f.read().split('\n')
            words.pop(-1)
        except:
            print('Unable to load file ' + fpath)
            quit()
        
        #self.word_list = words 
        
        if len(words) == 0:
            print("Word list is empty!")
            quit()
        
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
            quit()
        
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
        if not self.game_settings['show_alphabet']:
            return
        for i in range(len(status)):
            if status[i] == 0:
                print(self.colors['default'] + ' ' + chr(i + 97) + ' ' + self.colors['default'], end = "")
                #print(self.colors['no_match'] + ' ' + chr(i + 97) + ' ' + self.colors['no_match'], end = "")  
            elif status[i] == 1:
                #print(self.colors['exact_match'] + ' ' + chr(i + 97) + ' ' + self.colors['default'], end = "")
                print(self.colors['default'] + '[' + chr(i + 97) + ']' + self.colors['default'], end = "")                
            else:
                print(self.colors['default'] + '   ' + self.colors['default'], end = "")
        print(self.colors['default'] + "  ", end = "")    
        return
        
    def run_round(self):
        if len(self.unused_words) == 0:
            print("Word list completed!")
            quit()
            
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
            print('Win!')
            self.score += 1
            self.guess_statistics[i + 1] += 1
            self.streak['current'] += 1
            self.streak['best'] = max(self.streak['best'], self.streak['current'])
        else:
            status = self.check_word(curr_word, curr_word)
            print("")
            self.print_wordle(curr_word, status)
            print('Loss!')
            self.guess_statistics[i + 2] += 1
            self.streak['current'] = 0

        print('\nSCORE:', self.score)
        
        # Update rounds counter
        self.completed_rounds += 1
        return
          

if __name__ == "__main__":
    init(convert=True) # For color purpose
    
    args = sys.argv[1:]
    
    game = Game()
   
    game.print_wordle('WORDLE', [1, 0, -1, 1, -1, -1])
    print("")
    
    continueRound = True
    while(continueRound):
        game.run_round()
        continueRound = input("Continue? (Y/N)").lower() == "y"
    
    # print statistics
    
    game.print_game_statistics()
    
        
