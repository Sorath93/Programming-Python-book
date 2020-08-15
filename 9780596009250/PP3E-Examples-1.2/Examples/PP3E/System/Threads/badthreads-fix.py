import thread, time
count = 0

def adder():
    global count
    lock.acquire()        # only one thread running this at a time
    count = count + 1     # concurrently update a shared global
    count = count + 1
    lock.release()

lock = thread.allocate_lock()
for i in range(100):
    thread.start_new(adder, ())   # start 100 update threads

time.sleep(5)
print count                       # prints 200 
