### Solver ###
# Bruno Ramos Lima Netto

import numpy as np
from solver_funcs import *

def sudoku_starter(board):
    'pre-processing, solves until we have to start guessing'
    backups         = []  #sudokus backup
    branch          = []  # branch of the guessing tree 
    sudoku_board    = np.empty((9,9), dtype = int) # empty sudoku 9x9 board 
    sudoku_board[:] = board[:] #here we copy the board list
    moves           = num_moves(sudoku_board) # counts the number of zeroes
    guess_list      = available_moves(sudoku_board) #list with all the possible moves
    move,q,r        = next_move(guess_list) # next right move
    while moves: # while there are moves to make
        l = len(move)
        if l > 1:
            singles = check_singles(guess_list)
            for single in singles:
                q,r = divmod(single[1],9)
                if sudoku_board[q][r] == 0:
                    move               = [single[0]]
                    sudoku_board[q][r] = move[0]
                    moves             -= 1
                    guess_list         = refresh_single_guess(move,q,r,guess_list)
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
        singles = check_singles(guess_list)
        if len(singles) > 0:
            for single in singles:
                q,r = divmod(single[1],9)
                if sudoku_board[q][r] == 0:
                    move               = [single[0]]
                    sudoku_board[q][r] = move[0]
                    moves             -= 1
                    guess_list         = refresh_single_guess(move,q,r,guess_list)
        if moves == 0:
            return sudoku_board
        move,q,r       = next_move(guess_list)
        if not move:
            # if no moves available -> backtrack to the last savepoint (move_list)
            backups       = backups[:-1]
            branch        = branch[:-1]
            sudoku_board  = backups[-1][0]
            guess_list    = backups[-1][1]
            moves         = num_moves(sudoku_board)
        elif len(move) == 1:
            sudoku_board[q][r] = move[0]
            moves             -= 1
            guess_list         = refresh_guess_list(move,q,r,guess_list)
        elif len(move) > 1:
            guess        = next_branch(branch,move,q,r)
            if not guess:
                k = (branch.index([q,r]))
                sudoku_board  = backups[k-1][0]
                guess_list    = backups[k-1][1]
                backups       = backups[:k]
                branch        = branch[:k]
                moves         = num_moves(sudoku_board)
            else:
                backups.append([sudoku_board.copy(),copy_GL(guess_list)])
                sudoku_board[q][r] = guess[0]
                moves             -= 1
                branch            += [[q,r]]
                guess_list         = refresh_guess_list(guess,q,r,guess_list)
    return sudoku_board