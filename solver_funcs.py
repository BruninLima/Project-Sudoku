### Solver Functions ###
# Bruno Ramos Lima Netto

def num_moves(sudoku):
    'returns the maximum number of moves to do on the current sudoku / Counting the zeroes(empty squares)'

    moves = 0
    for line in sudoku:
        moves += list(line).count(0)
    return moves

def all_moves():
    'generates a list with all the possible moves of every square of the board' 

    ans = [[1,2,3,4,5,6,7,8,9] for _ in range(81)]
    return ans

def available_moves(sudoku):
    'returns the available guess_list of each EMPTY square(zeroes)'

    guess_list = all_moves()
 
    for i in range(9):
        for j in range(9):
            if (not (sudoku[i][j])) == False:
                numago = sudoku[i][j]
                guess_list[(9*i + j)] = []
                
                for k in range(9):
                    if numago in guess_list[9*i +k]:
                        guess_list[(9*i + k)].remove(numago)  #remove da linha
                    if numago in guess_list[(9*k + j)]:
                        guess_list[(9*k + j)].remove(numago)  #remove da coluna
                        
                a,b = (i//3)*3,(j//3)*3
                
                for m in range(a,a+3):
                    for n in range(b,b+3):
                        if numago in guess_list[9*m+n]:
                            guess_list[(9*m+n)].remove(numago)
    return guess_list

def next_move(guess_list):
    'returns a list with the next guesses, and its indexes (q,r)'
    
    if sum(map(sum,guess_list)) == 0: # no more available guesses >.<
        return [],None,None
    minmoves = 10
    idxmin = None
    for (i,move) in enumerate(guess_list):
        l = len(move)
        if 0 < l and l < minmoves:
            idxmin = i
            minmoves = l
            if l == 1:
                break
    q,r = divmod(idxmin,9)
    return guess_list[idxmin],q,r


def next_branch(branch,move,q,r):

    'returns the next branch to try (left to right)'
    if move == 0:
        #print(move,q,r,'wut')
        return -1 # error code
    j = branch.count([q,r])
    if j >= len(move):
        return 0
    return [move[j]]  # starts from the start of the list

def refresh_guess_list(move,q,r,guess_list):
    'given a move on the [q][r] square, refreshes the guess_list'
    new_guess_list        = guess_list
    new_guess_list[9*q+r] = []
    k = 9*q
    l = 9*(q//3)*3 + (r//3)*3
    mmm = move[0]
    for i in range(9):
        if mmm in new_guess_list[r+9*i]:
            new_guess_list[r+9*i].remove(mmm)  # remove da coluna
        if mmm in new_guess_list[k+i]:
            new_guess_list[k+i].remove(mmm)   # remove da linha

    for m in range(3):
        for n in range(3):
            if mmm in new_guess_list[l + m+9*n ]:
                new_guess_list[l + m+9*n ].remove(mmm)

    return new_guess_list

def copy_GL(guess_list):
    return [l[:] for l in guess_list]

def check_line(n,guess_list):
    'returns the n_th line in the guess_list (n from 0 to 8)'
    nth_line = guess_list[n*9:9*(n+1)]
    idxs = range(9*n,9*(n+1))
    return nth_line,idxs

def check_col(n,guess_list):
    'returns the n_th column in the guess_list (n from 0 to 8)'
    col_idxs = [(l*9)+n for l in range(9)]
    nth_column  = [guess_list[i] for i in col_idxs]
    
    return nth_column,col_idxs

def check_box(n,guess_list):
    'returns the n_th box in the guess_list (n from 0 to 8)'
    #code gore  basically math to get the right indexes from the boxes
    if n < 3:
        nth_box = guess_list[n*3:(n+1)*3] + guess_list[n*3 + 9:(n+1)*3 + 9] + guess_list[n*3 + 18:(n+1)*3 + 18]
        idxs = [n*3,3*n+1,3*n+2,n*3 + 9,n*3 + 10,n*3 + 11,n*3 + 18,n*3 + 19,n*3 + 20]
    elif n < 6:
        nth_box = guess_list[27+(n%3)*3:27+(n%3+1)*3] + guess_list[36+(n%3)*3:36+(n%3+1)*3] + guess_list[45+(n%3)*3:45+(n%3+1)*3]
        idxs = [27+(n%3)*3,28+(n%3)*3,29+(n%3)*3,36+(n%3)*3,37+(n%3)*3,38+(n%3)*3,45+(n%3)*3,46+(n%3)*3,47+(n%3)*3]
    elif n >= 6:
        nth_box = guess_list[54+(n%3)*3:54+(n%3+1)*3] + guess_list[63+(n%3)*3:63+(n%3+1)*3] + guess_list[72+(n%3)*3:72+(n%3+1)*3]
        idxs = [54+(n%3)*3,55+(n%3)*3,56+(n%3)*3,63+(n%3)*3,64+(n%3)*3,65+(n%3)*3,72+(n%3)*3,73+(n%3)*3,74+(n%3)*3]
    return nth_box,idxs

def check_singles(guess_list):
    singles = []
    for i in range(9):
        i_box,box_idxs = check_box(i,guess_list)
        i_line,line_idxs = check_line(i,guess_list)
        i_col,col_idxs = check_col(i,guess_list)
        for j in range(1,10):
            if sum(i_box,[]).count(j) == 1:
                for a,square in enumerate(i_box):
                    if j in square:
                        if [[j,box_idxs[a]]] not in singles:
                            singles += [[j,box_idxs[a]]]
            if sum(i_line,[]).count(j) == 1:
                for a,square in enumerate(i_line):
                    if j in square:
                        if [[j,line_idxs[a]]] not in singles:
                            singles += [[j,line_idxs[a]]]

            if sum(i_col,[]).count(j) == 1:
                for a,square in enumerate(i_col):
                    if j in square:
                        if [[j,col_idxs[a]]] not in singles:
                            singles += [[j,col_idxs[a]]]
    return singles