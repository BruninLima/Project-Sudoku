### Solver ###
# Bruno Ramos Lima Netto

import numpy as np
from solver_funcs import *

class Backtracking:
    def __init__(self, initial_state, next_states, is_final_state) -> None:
        self.initial_state = initial_state
        self.next_states = next_states
        self.is_final_state = is_final_state
    
    def solve(self):
        return sef.__solve(self.is_final_state, [])

    def __solve(self, state, visited):
        if self.is_final_state(state):
            return [state]
        else:
            for s in self.next_states(state, visited):
                result = self.__solve(s, visited)
                if result != None:
                    return [state] + result
            return None


def sudoku_starter(board):
    'adapting to the guess_list variable'
    backups         = [] #sudokus backup
    branch          = [] # branch of the guessing tree 
    sudoku_board    = np.empty((9,9), dtype = int) # empty sudoku 9x9 boara
    
     
    sudoku_board[:] = board[:]  #here we copy the board list
    moves           = num_moves(sudoku_board)  # counts the number of zeroes
    guess_list      = available_moves(sudoku_board) #list with all the possible moves
    singles         = check_singles(guess_list)
    for single in singles:
        q,r = divmod(single[1],9)
        if sudoku_board[q][r] == 0:
            move               = [single[0]]
            sudoku_board[q][r] = move[0]
            moves             -= 1
            guess_list         = refresh_guess_list(move,q,r,guess_list)
    move,q,r        = next_move(guess_list) # next right move
    while moves: # while there are moves to be made we make'em
        l = len(move)
        if l > 1:
            return sudoku_solver(sudoku_board,moves,guess_list,branch,backups)
        if l == 1:
            sudoku_board[q][r] =  move[0]
            moves             -=  1
            guess_list         =  refresh_guess_list(move,q,r,guess_list)
            move,q,r           =  next_move(guess_list)
    return sudoku_board

def sudoku_solver(sudoku_board,moves,guess_list,branch,backups):
    'solves the sudoku by trying to guess from the list with least possible guesses'
    while moves > 0:
        move,q,r          = next_move(guess_list)
        if not move:
            backups       = backups[:-1]
            branch        = branch[:-1]
            sudoku_board  = backups[-1][0]
            guess_list    = backups[-1][1]
            moves         = num_moves(sudoku_board)
        elif move == 1:
            sudoku_board[q][r] = move[0]
            guess_list         = refresh_guess_list(move,q,r,guess_list)
            moves             -= 1
        else:
            guess            = next_branch(branch,move,q,r)
            if not guess:
                k = (branch.index([q,r]))
                sudoku_board = backups[k-1][0]
                guess_list   = backups[k-1][1]
                backups      = backups[:k]
                branch       = branch[:k]
                moves        = num_moves(sudoku_board)
            else:
                backups.append([sudoku_board.copy(),copy_GL(guess_list)])
                sudoku_board[q][r] = guess[0]
                moves             -= 1
                branch            += [[q,r]]
                guess_list         = refresh_guess_list(guess,q,r,guess_list)
    return sudoku_board