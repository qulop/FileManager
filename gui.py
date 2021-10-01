import os
import sys
import time
import shutil
import getpass
from tkinter import *
import transfer
from tkinter import messagebox

def a(event):
    x = event.x
    y = event.y
    print(x, y)


def add_extensions(evet=None):
    frame = Frame(root, width=400, height=300)
    frame.place(x=0, y=0)

    def delete():
        frame.destroy()

    def test2():
        a = Toplevel()
        a.geometry('200x150+700+340')
        a.title('create')

        b = Button(a, text='close', command=a.destroy).place(x=13, y=16)

    b = Button(frame, text='file', command=test2).place(x=13, y=45)
    close = Button(frame, text='close', command=delete).place(x=13, y=13)


def add_type_extension():
    window = Toplevel()
    window.config(bg='#adad85')
    window.geometry('400x125+700+300')
    window.resizable(width=False, height=False)
    window.title('фото')

    main_label = Label(window, text='Запишите расширения через пробел: ', bg='#adad85')
    main_label.place(x=53, y=5)
    
    save = Button(window, text='Сохранить', highlightthickness=0, bd=0, bg='#999966',
                  activebackground='#b8b894')
    save.place(x=70, y=90)
    cancel = Button(window, text='Отменить', highlightthickness=0, bd=0, bg='#999966', activebackground='#b8b894',
                    command=lambda: window.destroy()).place(x=230, y=90)

    enter = Text(window, width=48, height=3, bg='#c2c2a3', highlightthickness=0, bd=0).place(x=7, y=30)
    window.bind('<Button-1>', a)

class App:
    def __init__(self):
        self.win = Tk()
        self.win.title('*app name*')
        self.win.geometry('400x300+700+300')



# def special_file():
#     pass
#
# def help():
#     pass
#
# user = getpass.getuser()

# шапка------------------------------
root = Tk()
root['bg'] = '#ffffff'
root.title('GUI для Менеджера файлов')
root.resizable(width=False, height=False)
root.geometry('400x300+700+300')
# -----------------------------------


# меню------------------------------
mainmenu = Menu(root)
root.config(menu=mainmenu)

file_manage = Menu(mainmenu, tearoff=0)
file_manage.add_command(label='Добавить расширения (Ctrl+E)', command=add_extensions)
file_manage.add_command(label='Специальные файлы/папки (Ctrl+D)')
file_manage.add_command(label='Прочие насройки (Ctrl+S)')

mainmenu.add_cascade(label='управление', menu=file_manage)
mainmenu.add_command(label='справка')
# -----------------------------------

# def on():
#     if status == 0:
#         status2['text'] = '(вкл)'
#         but['text'] = 'выключить'
#         f['file'] = 'icons/active.png'
#
#     else:
#         status2['text'] = '(выкл)'
#         but['text'] = 'включить'


def window():
    def delete():
        frame.destroy()

    frame = Frame(root, width=120, height=300, bg='#543450')
    frame.place(x=0, y=0)

    close = Button(frame, text='close', command=delete).place(x=13, y=13)

# основной фрейм----------------------------
af = 'off'
on = PhotoImage(file='icons/switch-on.png')
off = PhotoImage(file='icons/switch-off.png')
active = PhotoImage(file='icons/active.png')
notactive = PhotoImage(file='icons/notactive.png')
def aa():
    global af
    if af == 'off':
        on_off.configure(image=on)
        on_off.place(x=250, y=245)
        lab['image'] = active
        second_status['text'] = '(вкл)'
        af = 'o'
    else:
        on_off.configure(image=off)
        on_off.place(x=250, y=237)
        lab['image'] = notactive
        second_status['text'] = '(выкл)'
        af = 'off'

status = Label(root, text='Текущее состояние: ', bg='#ffffff'); status.place(x=10, y=265)
second_status = Label(root, text='(выкл)', bg='#ffffff'); second_status.place(x=185, y=265)
lab = Label(root, image=notactive, bg='#ffffff')
lab.place(x=162, y=266)
on_off = Button(root, image=off, highlightthickness=0, bd=0, command=add_type_extension, bg='#ffffff')
on_off.place(x=250, y=237)    #  x=240 y=259

log_field = Text(width=400, height=15, state=DISABLED)
log_field.place(x=0, y=0)
# ----------------------------------------

# root.protocol("WM_DELETE_WINDOW", close)
root.bind('<Button-1>', a)
root.bind('<Control-e>', add_extensions)

root.mainloop()
