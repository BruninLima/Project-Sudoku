### Sudoku Reader ###
# Bruno Ramos Lima Netto

from time import clock 

def sudoku_reader(file):
    'reads the sudoku.txt file and separates each sudoku into a tensor'
    sudokuboards = []
    with open(file,'r') as f:
        ks = f.readlines()
        i        = 0
        sudoku_n = []
        for k in ks:
            i        += 1
            sudoku_n += [k]
            if i == 10:
                sudokuboards.append(sudoku_n[1:]) # Remove "Grid NN" line
                i        = 0 
                sudoku_n = []
        return sudokuboards
    
def sudoku_format(s):
    ans = []
    for iis in s:
        lis = iis[:-1]
        half_ans = []
        for i in lis:
            half_ans.append(int(i))
        ans.append(half_ans)
    return np.array(ans)

def puzzles(file):
    return list(map(sudoku_format,sudoku_reader(file)))