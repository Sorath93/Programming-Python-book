import sys
filename = sys.argv[1]
answer = {}

for line in open(filename):
    cols = line.split(',')
    nums = [float(x) for x in cols]
    for (i, x) in enumerate(nums):
        answer[i] = answer.get(i, 0) + x

for key in sorted(answer):
    print key, '=>', '%.2f' % answer[key]
    
