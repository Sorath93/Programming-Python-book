total = 0
for line in open('data.txt'):
    cols = line.split(',')
    total += int(cols[1])
print total

cols = [line.split(',')[1] for line in open('data.txt')]
print sum(int(x) for x in cols)

