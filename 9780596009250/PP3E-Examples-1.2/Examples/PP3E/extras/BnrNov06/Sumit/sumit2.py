import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'data.txt'
totals = {}
for line in open(filename):
    cols = line.split(',')
    nums = [float(x) for x in cols]
    for (i, x) in enumerate(nums):
        totals[i] = totals.get(i, 0) + x
 
for key in sorted(totals):
    print '%s = %7.2f' % (key, totals[key])
