sums = {}
for line in open('data.txt'):
    cols = line.split(',')
    nums = [int(x) for x in cols]
    for (i, num)in enumerate(nums):
        sums[i] = sums.get(i, 0) + num

print sums


