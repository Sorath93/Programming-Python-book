import thread, Queue, time
from ScrolledText import ScrolledText

class ThreadGui(ScrolledText):
    threadsPerClick = 4
    
    def __init__(self, parent=None):
        ScrolledText.__init__(self, parent)
        self.pack()
        self.dataQueue = Queue.Queue()              # infinite size
        self.bind('<Button-1>', self.makethreads)   # on left mouse click
        self.consumer()                             # queue loop in main thread

    def producer(self, id):
        for i in range(5):
            time.sleep(0.1)
            self.dataQueue.put('producer %d:%d' % (id, i))
        
    def consumer(self):
        try:
            data = self.dataQueue.get(block=False)
        except Queue.Empty:
            pass
        else:
            self.insert('end', 'consumer got: %s\n' % str(data))
            self.see('end')
        self.after(100, self.consumer)    # 10 times per sec

    def makethreads(self, event):
        for i in range(self.threadsPerClick):
            thread.start_new_thread(self.producer, (i,))

root = ThreadGui()
root.mainloop()       # popup window, enter tk event loop
