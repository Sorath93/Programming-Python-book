import sys
filename = sys.argv[1]
totals   = {}

for line in open(filename):
    cols = line.split(',')
    nums = [int(x) for x in cols]
    for (ix, num) in enumerate(nums):
        totals[ix] = totals.get(ix, 0) + num
        
for key in sorted(totals):
    print key, '=', totals[key]





##    for (ix, num) in enumerate(nums):
##        if not totals.has_key(ix):
##            totals[ix] = num
##        else:
##            totals[ix] += num

    
##    for i in range(len(nums)):
##        if not totals.has_key(i):
##            totals[i] = nums[i]
##        else:
##            totals[i] += nums[i]
    
    
    
