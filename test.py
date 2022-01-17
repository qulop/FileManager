from tkinter import *

def a():
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append('AmyClaraVika')
    root.update()
    root.destroy()

root = Tk()

b = Button(text='м', command=a)
b.pack()

root.mainloop()