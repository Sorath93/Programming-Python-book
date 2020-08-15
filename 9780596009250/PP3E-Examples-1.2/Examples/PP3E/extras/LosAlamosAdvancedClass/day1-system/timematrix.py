"""
time alternative matrix representationss
"""

import time
reps = 10000     # times to call test func
size = 1000      # size x size matrix

def timer(func, reps=reps, *args):
    """
    general timer function
    pass in func, reps?, args?
    """
    startTime = time.clock()
    for i in range(reps):
        func(*args)
    totTime = time.clock() - startTime
    return totTime, (totTime / reps)

def makeList():
    "make a test list matrix"
    row = range(size)
    mat = [row] * size
    return mat

def indexList(mat):
    for i in range(size):
        x = mat[i][i]

def makeDict():
    mat = {}
    for i in range(size):
        mat[(i, i)] = 1
    return mat

def indexDict(mat):
    for i in range(size):
        x = mat[(i, i)]

if __name__ == '__main__':
    mat = makeList()
    #for row in mat: print row
    print timer(indexList, mat)   

    mat = makeDict()
    #for key in sorted(mat): print key, '=>', mat[key] 
    print timer(indexDict, mat)
    
    
    
