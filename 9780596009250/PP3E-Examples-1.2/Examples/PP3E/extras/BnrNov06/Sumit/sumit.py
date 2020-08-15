import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'data.txt'
totals = []
for line in open(filename):
    cols = line.split(',')
    if not totals:
        totals = [0] * len(cols)
    elif len(totals) < len(cols):
        totals += [0] * (len(cols) - len(totals))
    nums = [float(x) for x in cols]
    for (i, x) in enumerate(nums):
        totals[i] += x

print ('%.2f ' * len(totals)) % tuple(totals)
