filename = 'data.txt'
sums = {}
for line in open(filename):
    cols = line.split(',')
    nums = [float(x) for x in cols]
    for (i,num) in enumerate(nums):
        sums[i] = sums.get(i, 0) + nums[i]

for key in sorted(sums):
    print key, '=', sums[key]
