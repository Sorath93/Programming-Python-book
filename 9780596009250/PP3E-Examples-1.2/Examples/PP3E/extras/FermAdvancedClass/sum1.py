import sys
filename = sys.argv[1]
answer = []

for line in open(filename):
    cols = line.split(',')
    nums = [float(x) for x in cols]
    if not answer:
        answer = [0] * len(cols)
    for (i, x) in enumerate(nums):
        answer[i] += x

    #answer = [x + y for (x, y) in zip(answer, nums)]

print ['%.2f' % x for x in answer]
    
