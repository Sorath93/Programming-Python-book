##########################################################################
# thread basics: start 10 copies of a function running in parallel; 
# uses time.sleep so that the main thread doesn't die too early--this 
# kills all other threads on both Windows and Linux; stdout is shared:
# thread outputs may be intermixed in this version occasionally.
##########################################################################
     
import thread, time
     
def counter(myId, count):                    # this function runs in threads
    for i in range(count): 
        #time.sleep(1)
        print '[%s] => %s' % (myId, i)
     
for i in range(10):                          # spawn 10 threads
    thread.start_new(counter, (i, 3))        # each thread loops 3 times
     
time.sleep(4)
print 'Main thread exiting.'                 # don't exit too early  
