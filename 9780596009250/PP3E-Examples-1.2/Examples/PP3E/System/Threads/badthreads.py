import thread, time
count = 0

def adder():     
    global count     
    count = count + 1     # concurrently update a shared global     
    count = count + 1     # thread swapped out in the middle of this

for i in range(100):     
    thread.start_new(adder, ())   # start 100 update threads

time.sleep(5)
print count
