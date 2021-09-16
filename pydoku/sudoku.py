### Refactoring Project Sudoku ###
###        Brunin Lima         ###

### Code Structure:
#   
#   Main Python Files:
# 1. Generator.py     --> Generating a sudoku // Some fluff
# 2. solver_funcs.py  --> Solver Aux Functions
# 3. solver.py        --> Pre-solve + Solve
# 4. sudoku_reader.py --> Reading/Formatting a sudoku
#
#
### TODO: Code Restructure
# 
# Sudoku Class 
# Bool Tensor idea implementation  
# Read/Create a sudoku object
# Solver/Backtrack


###
# A little bit of data scturcture
# A sudoku is a 9x9 board. Each slot can have one of the numbers[0,...9]
# We can create a 10x9x9 bool tensor   - opt 1
# We can create a 10x81 int ajd. list. - opt 2

### Imports
import numpy as np

def sort_dict(dictionary):
    sorted_dict = {k:dictionary[k] for k in sorted(dictionary, key=lambda k: len(dictionary[k]), reverse=False) if len(dictionary[k]) > 0}
    return sorted_dict

def get_blocked_idxs(idxs):
    " Returns a set of all the blocked indexes from the given indexes " 
    blocked_idxs = set()

    for idx in idxs:

        q,r = divmod(idx, 9) # idx for the columns/lines
        a,b = (q//3)*3, (r//3)*3  # idx for the 3x3 block

        for k in range(9):

            row = 9*q + k
            col = 9*k + r
            
            blocked_idxs.add(row) # blocked lines
            blocked_idxs.add(col) # blocked columns  
        
        for m in range(a, a+3):
            for n in range(b, b+3):
                
                sqr = 9*m + n
                blocked_idxs.add(sqr)
                
    return blocked_idxs

def get_blocked_dict():

    blkd_dict = {}
    for i in range(81):
        blkd_dict[i] = get_blocked_idxs([i])
    return blkd_dict

def get_possible_moves(blkd_dict, idxs):

    """ Aux function that verifies in a board,
     every move available for a given idx """

    # first case: adj_list:

    possible_moves_num = set()
            
    for cell in range(81):
        if not(any(cell in st for st in [blkd_dict[idx] for idx in idxs])):
            possible_moves_num.add(cell) 

    return possible_moves_num

class Sudoku:
    """  Sudoku can be stored as adj_list or bool_mat"""
    def __init__(self, sudoku, kind, verbose = False):
    
        self.storage = kind 
        self.verbose = verbose

        if self.storage == "adj_list":   
            self.board = {i:set() for i in range(10)}
            for x,row in enumerate(sudoku):
                for y,num in enumerate(row):
                    self.board[num].add(9*x + y)    
            self.num_moves = len(self.board[0])

        if self.storage == "bool_mat":
            self.board = np.zeros((10,9,9), dtype = bool)
            for x,row in enumerate(sudoku):
                for y,num in enumerate(row):
                    self.board[num][x][y] = True    

            self.num_moves = self.board.sum()   
        self.blocked_dict = get_blocked_dict()
        self.avail_moves = self.available_moves()
        
    def available_moves(self):

        avail_moves = {i:set() for i in range(81)}
        
        if self.storage == "adj_list":
            for num in range(1, 10):
                for mv in get_possible_moves(self.blocked_dict, self.board[num]):
                    if mv in self.board[0]: 
                        avail_moves[mv].add(num)
                        
            return sort_dict(avail_moves)
        #TODO
        if self.storage == "bool_mat": # 9x27 sums, sum(col), sum(line) .. <= 1
            cols, lines, sqrs = 9,9,9
            for num in range(1, 10):
                for col in cols:                
                    cs = np.sum(self.board[col], axis = 1) # choose the right axis (exp.)
                    avail_moves[col] = bool(cs) 
                for line in lines:
                    ls = np.sum(self.board[line], axis = 1) # choose the right axis (exp.)
                    avail_moves[col] = bool(ls)
                for sqr in sqrs:
                    ss = np.sum(self.board[sqr], axis = 1) # choose the right axis (exp.)
                    avail_moves[ss] = bool(ss)

            return sort_dict(avail_moves)
         
    def update_avail_moves(self, idx, num):
        
        for mv in self.blocked_dict[idx]:
            if (mv in self.board[0]) and (num in self.avail_moves[mv]):      
                self.avail_moves[mv].remove(num)
        self.avail_moves = sort_dict(self.avail_moves)

    def make_move(self, idx, num):
        """ Make move function... Should we verify? or meh"""
        
        self.num_moves -= 1
        self.update_avail_moves(idx, num)   
        if self.storage == "adj_list":
            self.board[num].add(idx)
            self.board[0].remove(idx)
        if self.storage == "bool_mat":
            idx_x, idx_y = divmod(idx, 9)
            self.board[0][idx_x][idx_y] = False
            self.board[num][idx_x][idx_y] = True
        
    def next_move(self): 
        """ Function responsible for the next moves of the sudoku. 
        
        It has 3 possible cases for the next moves:

            - There are no available moves
            - If there are single moves
            - If there are moves, and no single moves. """

        stack = self.avail_moves.keys()
        
        #1st case
        if len(stack) == 0:
            if self.verbose == True:
                print(" Warning, no possible moves for the current sudoku")
            return False
        #2nd case
        key = stack.pop()
        
        while len(self.avail_moves[key]) == 1:
    
            if self.verbose == True:
                print(" Theres a obvious move at tile {}".format(key))
            
            self.make_move(self, key, self.avail_moves[key].pop())
            stack = self.avail_moves.keys()
            if len(stack) == 0:
                return False
            else:
                key = stack.pop
        
        #3rd case
        PossibleGuesses = [[key, len(self.avail_moves[key])]]
        curr_len = len(self.avail_moves[key])

        for i in stack:
            tmp_key = i
            tmp_len = len(self.avail_moves[tmp_key])
            if tmp_len > curr_len:
                break
            else:
                PossibleGuesses.append([tmp_key, self.avail_moves[tmp_key]])                

        if self.verbose == True:
            print(" There are no obvious moves, we need to start guessing...")
            print(" ")
            print(" Possible Guesses are:", PossibleGuesses)

        return PossibleGuesses

    def get_visual_board(self):

        visual_board  = np.zeros(81)
        if self.storage == "adj_list":
            for i in range(10):
                for idx in self.board[i]:
                    visual_board[idx] = i
        return visual_board.reshape((9,9))


def Solver(sudoku):

    """  Returns a solution to the sudoku 
    
        Input must be a Sudoku object  """
    
    # Implement the backtracking mechanism

    # Backup to go back if mistake
    # While no mistakes: we push the next_move
    # ...
    # The backup should be stored in backups a dictionary ?
    # How big can backup be? and what should it save?
    # List of last moves?
    # Diff list probably.

    backups = []




    while sudoku.num_moves > 0:
        # A better test for mistakes might be len(self.avail_moves < num_moves[number of zeroes])
        # since it guarantees a mistake has been made.

        ## Two different cases:

        guesses_list = sudoku.next_move()
        
        if len(sudoku.avail_moves < sudoku.num_moves):
            # GO BACK TO CHECKPOINT --> BACKTRACK
        
            sudoku = "last backup"
            offset = 1
            nextmove = sudoku.next_move[offset]

        move = sudoku.next_move()
        # Available Moves --> Make a Good Guess

        move = "Define Next Branch, based on current branch and move"

    # No Available Moves and No Zeroes --> DONE :)

    return sudoku