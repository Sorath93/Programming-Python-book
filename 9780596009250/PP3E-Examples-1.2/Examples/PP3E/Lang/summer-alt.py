def summer(numCols, fileName):
    sums = [0] * numCols
    for line in open(fileName):                     # use file iterators
        cols = line.split(',')                      # assume comma-delimited
        nums = [int(x) for x in cols]               # use limited converter
        both = zip(sums, nums)                      # avoid nexted for loop
        sums = [x + y for (x, y) in both]
    return sums
