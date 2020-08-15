import sys
filename = sys.argv[1]
for line in open(filename):
    cols = line.split(',')
    nums = [int(x) for x in cols]
    print sum(nums)
    
    
