from Tkinter import *
import random
colors = ['blue', 'red', 'green', 'yellow', 'orange']
fontsize = 25

def reply():
    popup = Toplevel()
    popup.title('Popup Window')
    color = random.choice(colors)
    Label(popup, text='Popup!', bg=color).pack()
    lab.config(fg=color)

def timer():
    global fontsize
    fontsize += 2
    lab.config(font=('Courier', fontsize, 'italic'))
    main.after(250, timer)
               
main = Tk()
lab = Label(main, text='Spam', font=('Courier', fontsize, 'italic'))
lab.pack(side=TOP, expand=YES, fill=BOTH)
Button(main, text='press', command=reply).pack(side=BOTTOM, fill=X)
main.title('GUI1')
main.after(250, timer)
main.mainloop()
