import thread, Queue, time
dataQueue = Queue.Queue()    # infinite size

def producer(id):
    for i in range(5):
        time.sleep(0.1)
        print 'put'
        dataQueue.put('producer %d:%d' % (id, i))
    
def consumer(root):
    try:
        print 'get'
        data = dataQueue.get(block=False)
    except Queue.Empty:
        pass
    else:
        root.insert('end', 'consumer got: %s\n' % str(data))
        root.see('end')
    root.after(250, lambda: consumer(root))    # 4 times per sec

def makethreads():
    for i in range(4):
        thread.start_new_thread(producer, (i,))

# main Gui thread: spawn batch of worker threads on each mouse click
import ScrolledText
root = ScrolledText.ScrolledText()
root.pack()
root.bind('<Button-1>', lambda event: makethreads())
consumer(root)                       # start queue check loop in main thread
root.mainloop()                      # popup window, enter tk event loop
