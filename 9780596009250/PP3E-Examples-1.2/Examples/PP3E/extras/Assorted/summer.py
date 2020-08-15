fname = 'data.txt'
sums = {}

for line in open(fname):
    cols = line.split()
    nums = map(int, cols)
    for (col, num) in enumerate(nums):
        sums[col] = sums.get(col, 0) + num

for col in sorted(sums):
    print col, '=>', sums[col]
    

    
