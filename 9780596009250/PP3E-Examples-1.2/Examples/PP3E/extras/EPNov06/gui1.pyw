from Tkinter import *
import random
fontsize = 25
colors = ['blue', 'red', 'green', 'orange', 'yellow', 'brown']

def reply():
    popup = Toplevel()
    popup.title('POPUP')
    color = random.choice(colors)
    Label(popup, text='Brian', fg=color).pack()
    L.config(fg=color)

def timer():
    L.config(fg=random.choice(colors))
    main.after(100, timer)

def grow():
    global fontsize
    L.config(font=('arial', fontsize, 'italic'))
    fontsize += 5
    main.after(100, grow)
    
main = Tk()
main.title('GUI1')
L = Label(main, text='Spam', font=('arial', fontsize, 'italic'), fg='green', bg='black')
L.pack(side=TOP, expand=YES, fill=BOTH)
Button(text='press', command=reply).pack(side=BOTTOM, fill=X)
Button(text='timer', command=timer).pack(side=BOTTOM, fill=X)
Button(text='close', command=main.quit).pack(side=BOTTOM, fill=X)
Button(text='grow',  command=grow).pack(side=BOTTOM, fill=X)
main.mainloop()
