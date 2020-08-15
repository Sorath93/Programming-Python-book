import sys
tots = False
for line in open(sys.argv[1]):
    cols = line.split(',')
    nums = [float(x) for x in cols]
    if not tots:
        tots = [0] * len(cols)
    for (i, x) in enumerate(nums):
        tots[i] += x

print ('%.2f ' * len(tots)) % tuple(tots)
   
    
    
