import thread, Queue, os
from Tkinter import Tk
from PP3E.Gui.Tools.guiStreams import GuiOutput
stdoutQueue = Queue.Queue()                        # infinite size

def producer(input):
    while True:
        line = input.readline()                    # ok to block: child thread
        stdoutQueue.put(line)                      # empty at end-of-file
        if not line: break
    
def consumer(output, root, term='<end>'):
    try:
        line = stdoutQueue.get(block=False)        # main thread: check queue
    except Queue.Empty:                            # 4 times/sec, okay of empty
        pass
    else:
        if not line:                               # stop loop at end-of-file
            output.write(term)                     # else display next line
            return
        output.write(line)
    root.after(250, lambda: consumer(output, root, term))

def redirectedGuiShellCmd(command, root):
    input  = os.popen(command, 'r')                # start non-gui program
    output = GuiOutput(root)
    thread.start_new_thread(producer, (input,))    # start reader thread
    consumer(output, root)

if __name__ == '__main__':
    win = Tk()
    redirectedGuiShellCmd('python -u pipes-nongui.py', win)
    win.mainloop()
