##############################################################################
# system-wide thread interface utilities for GUIs;
# single thread queue and checker timmer loop shared by all windows;
# never blocks GUI - just spawns and verifies operations and quits;
# worker threads can overlap with main thread, and other workers;
#
# using a queue of callback functions and arguments is more useful than a 
# simple data queue if there can be many kinds of threads running at the 
# same time - each kind may have different implied exit actions
#
# because GUI API is not completely thread-safe, instead of calling GUI 
# update callbacks directly after thread exit, place them on a shared queue,
# to be run from a timer loop in the main thread, not a child thread; this
# also makes GUI update points less random and unpredictable;
#
# assumes threaded action raises an exception on failure, and has a 'progress'
# callback argument if it supports progress updates;  also assumes that queue
# will contain callback functions for use in a GUI app: requires a widget in
# order to schedule and 'after' event loop callbacks;
##############################################################################

# run even if no threads
try:                                     # raise ImportError to
    import thread                        # run with gui blocking
except ImportError:                      # if threads not available 
    class fakeThread:
        def start_new_thread(self, func, args):
            func(*args)
    thread = fakeThread()

import Queue, sys
threadQueue = Queue.Queue(maxsize=0)              # infinite size


def threadChecker(widget, delayMsecs=100):        # 10x per second
    """
    in main thread: periodically check thread completions queue;
    do implied GUI actions on queue in this main GUI thread;
    one consumer (GUI), multiple producers (load,del,send);
    a simple list may suffice: list.append/pop are atomic;
    one action at a time here: a loop may block GUI temporarily;
    """
    try:
        (callback, args) = threadQueue.get(block=False)
    except Queue.Empty:
        pass
    else:
        callback(*args)
    widget.after(delayMsecs, lambda: threadChecker(widget))


def threaded(action, args, context, onExit, onFail, onProgress):
    """
    in a new thread: run action, manage thread queue puts;
    calls added to queue here are dispatched in main thread;
    run action with args now, later run on* calls with context;
    allows action to be ignorant of use as a thread here;
    passing callbacks into thread directly may update GUI in
    thread - passed func in shared memory but called in thread;
    progress callback just adds callback to queue with passed args;
    don't update counters here: not finished till taken off queue
    """
    try:
        if not onProgress:           # wait for action in this thread
            action(*args)            # assume raises exception if fails
        else:
            progress = (lambda *any: threadQueue.put((onProgress, any+context)))
            action(progress=progress, *args)
    except:
        threadQueue.put((onFail, (sys.exc_info(),)+context))
    else:
        threadQueue.put((onExit, context))

def startThread(action, args, context, onExit, onFail, onProgress=None):
    thread.start_new_thread(
        threaded, (action, args, context, onExit, onFail, onProgress)) 


class ThreadCounter:
    """
    a thread-safe counter or flag
    """
    def __init__(self):
        self.count = 0
        self.mutex = thread.allocate_lock()     # or use Threading.semaphore
    def incr(self):
        self.mutex.acquire()
        self.count += 1
        self.mutex.release()
    def decr(self):
        self.mutex.acquire()
        self.count -= 1
        self.mutex.release()
    def __len__(self): return self.count        # True/False if used as a flag


if __name__ == '__main__':                      # self-test code when run
    import time, ScrolledText
    
    def threadaction(id, reps, progress):       # what the thread does
        for i in range(reps):
            time.sleep(1)
            if progress: progress(i)            # progress callback: queued
        if id % 2 == 1: raise Exception         # odd numbered: fail

    def mainaction(i):                          # code that spawns thread
        myname = 'thread-%s' % i
        startThread(
            action     = threadaction, 
            args       = (i, 3),
            context    = (myname,), 
            onExit     = threadexit, 
            onFail     = threadfail, 
            onProgress = threadprogress)

    # thread callbacks: dispatched off queue in main thread
    def threadexit(myname):
        root.insert('end', '%s\texit\n' % myname)
        root.see('end')
    def threadfail(exc_info, myname):
        root.insert('end', '%s\tfail\t%s\n' % (myname, exc_info[0]))
        root.see('end')
    def threadprogress(count, myname):
        root.insert('end', '%s\tprog\t%s\n' % (myname, count))
        root.see('end')
        root.update()   # works here: run in main thread

    # make enclosing GUI 
    # spawn batch of worker threads on each mouse click: may overlap
    root = ScrolledText.ScrolledText()
    root.pack()
    threadChecker(root)                 # start thread loop in main thread
    root.bind('<Button-1>', lambda event: map(mainaction, range(6)))
    root.mainloop()                     # popup window, enter tk event loop
