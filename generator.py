### Generator ### 
# Bruno Ramos Lima Netto

from copy import deepcopy
import numpy as np

normal_sudoku  =      [[8,0,0,0,0,0,0,0,0],
                       [0,0,3,6,0,0,0,0,0],
                       [0,7,0,0,9,0,2,0,0],
                       [0,5,0,0,0,7,0,0,0],
                       [0,0,0,0,4,5,7,0,0],
                       [0,0,0,1,0,0,0,3,0],
                       [0,0,1,0,0,0,0,6,8],
                       [0,0,8,5,0,0,0,1,0],
                       [0,9,0,0,0,0,4,0,0]]

normal_sol =          [[8,1,2,7,5,3,6,4,9],
                       [9,4,3,6,8,2,1,7,5],
                       [6,7,5,4,9,1,2,8,3],
                       [1,5,4,2,3,7,8,9,6],
                       [3,6,9,8,4,5,7,2,1],
                       [2,8,7,1,6,9,5,3,4],
                       [5,2,1,9,7,4,3,6,8],
                       [4,3,8,5,2,6,9,1,7],
                       [7,9,6,3,1,8,4,5,2]]

min_sudoku  =         [[0,0,0,0,1,7,0,0,6],
                       [0,0,0,0,4,0,0,0,0],
                       [3,0,0,0,0,0,0,0,0],
                       [0,1,0,0,0,0,7,0,0],
                       [0,0,0,2,0,0,0,5,0],
                       [0,0,0,0,0,0,0,2,0],
                       [2,0,0,5,0,0,4,0,0],
                       [5,0,8,3,0,0,0,0,0],
                       [0,0,0,0,0,0,1,0,0]]

min_sol =             [[8,2,5,9,1,7,3,4,6],
                       [1,6,7,8,4,3,5,9,2],
                       [3,9,4,6,5,2,8,1,7],
                       [6,1,2,4,9,5,7,3,8],
                       [4,8,3,2,7,6,9,5,1],
                       [7,5,9,1,3,8,6,2,4],
                       [2,7,1,5,8,9,4,6,3],
                       [5,4,8,3,6,1,2,7,9],
                       [9,3,6,7,2,4,1,8,5]]


null_sudoku  =        [[0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0]]

null_sol =            [[1,2,3,4,5,6,7,8,9],
                       [4,5,6,7,8,9,1,2,3],
                       [7,8,9,1,2,3,4,5,6],
                       [2,3,1,6,7,4,8,9,5],
                       [8,7,5,9,1,2,3,6,4],
                       [6,9,4,5,3,8,2,1,7],
                       [3,1,7,2,6,5,9,4,8],
                       [5,4,2,8,9,7,6,3,1],
                       [9,6,8,3,4,1,5,7,2]]



def unique_sudoku(sudoku):
    'returns whether the sudoku is unique, and the time it takes to solve doing [<-- , -->]'
    # 0 if false, 1 if true
    unique = 0
    
    def next_branch(branch,move,q,r):
        'returns the next branch to try'
        #usando o chute pelo final <--
        if move == 0:
            print(move,q,r,'wut')
            return -1 # error code
        j = branch.count([q,r])
        if j >= len(move):
            return 0
        return [move[-j-1]]
    
    t0_left = clock()
    n_ans1   = sudoku_starter(sudoku)
    tf_left = clock() - t0_left
    
    def next_branch(branch,move,q,r):
        'returns the next branch to try'
        #usando o chute pelo final -->
        if move == 0:
            #print(move,q,r,'wut')
            return -1 # error code
        j = branch.count([q,r])
        if j >= len(move):
            return 0
        return [move[j]]
    
    t0_right = clock()
    n_ans2  = sudoku_starter(sudoku)
    tf_right = clock() - t0_right
    
    if np.all(n_ans1[0] == n_ans2[0]):
        unique += 1
    else:
        unique += 0
        
    return [unique , [ tf_left,tf_right]]

def create_from_solution(n,board):
    'removes n ~random~ numbers from a given board'
    game = deepcopy(board)
    a = np.random.choice(81,n, replace = False)
    for i in a:
        m,n = divmod(i,9)
        game[m][n]= 0
    return game

def sudoku_creator(seed = 0):
    solved_boards = [min_sol,normal_sol,null_sol]
    game = solved_boards[seed]
    for n in range(65): 
        n_board = create_from_solution(1,game)
        if unique_sudoku(n_board)[0] == True:
            game = n_board
        else:
            break
    return game

def generator(seed = 0,maxiter = 5):
    minmoves = 0 
    minboard = []
    for k in range(maxiter):
        board = sudoku_creator(seed)
        moves = num_moves(board)
        if moves >= minmoves:
            minmoves = moves
            minboard = board
        if moves == 17:
        	return board, moves
    return minboard, minmoves