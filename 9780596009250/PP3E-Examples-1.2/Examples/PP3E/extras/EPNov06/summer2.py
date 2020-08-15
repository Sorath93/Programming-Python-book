import sys
tots = {}
for line in open(sys.argv[1]):
    cols = line.split(',')
    nums = [float(x) for x in cols]
    for (i, x) in enumerate(nums):
        tots[i] = tots.get(i, 0) + x

for key in sorted(tots):
    print key, '=', tots[key]
