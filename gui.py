from tkinter import *
import copy

# шапка------------------------------
root = Tk()
root['bg'] = '#ffffff'
root.title('GUI для Менеджера файлов')
root.resizable(width=False, height=False)
root.geometry('400x300+700+300')
# -----------------------------------

def a(event):
    x = event.x
    y = event.y
    print(x, y)

down = PhotoImage(file='icons/down.png')
up = PhotoImage(file='icons/up.png')

extension=0
def add_extensions(event=None):
    def add_type_extension(title: str, ):
        window = Toplevel()
        window.config(bg='#adad85')
        window.geometry('400x125+700+300')
        window.resizable(width=False, height=False)
        window.title(title)

        main_label = Label(window, text='Запишите расширения через пробел: ', bg='#adad85')
        main_label.place(x=53, y=5)

        save = Button(window, text='Сохранить', highlightthickness=0, bd=0, bg='#999966',
                      activebackground='#b8b894')
        save.place(x=70, y=90)
        cancel = Button(window, text='Отменить', highlightthickness=0, bd=0, bg='#999966', activebackground='#b8b894',
                        command=lambda: window.destroy()).place(x=230, y=90)

        enter = Text(window, width=48, height=3, bg='#c2c2a3', highlightthickness=0, bd=0).place(x=7, y=30)
        window.bind('<Button-1>', a)
    extension_win = Canvas(root, width=400, height=300, bg='#ffffff')
    extension_win.place(x=0, y=0)
    ref_x = 40
    ref_y = 70

    def destroy(event=None):
        extension_win.destroy()
        for i in buttons:
            i.destroy()

    def fuck_me_please_in_the_ass_please():
        nonlocal ref_y, ref_x
        photo_more_info['image'] = up

    buttons = []
    stat = Label(extension_win, text='Все просматриваемые\nна данный момент расширения:', bg='#ffffff')
    stat.place(x=85, y=5)

    var1 = BooleanVar()
    var1.set(0)
    different_types = Checkbutton(extension_win, variable=var1, onvalue=1, offvalue=0,
                                  bg='#ffffff', highlightthickness=0)
    different_types.place(x=40, y=40)

    back = Button(text='Назад', bd=0, bg='#d9d9d9', command=destroy)
    back.place(x=10, y=5)
    buttons.append(back)

    photo_label = Label(extension_win, text='Расширения для фотографий:', bg='#ffffff').place(x=ref_x, y=ref_y)
    photo_text = Text(extension_win, height=1, width=16, highlightthickness=0).place(x=ref_x+220, y=ref_y+1)
    photo_more_info = Button(extension_win, image=down, bd=0, bg='#d9d9d9', command=fuck_me_please_in_the_ass_please)
    photo_more_info.place(x=ref_x+225, y=ref_y+35)
    photo_add = Button(text='Добавить расширение', bd=0, bg='#d9d9d9')
    photo_add.place(x=ref_x+20, y=ref_y+35)
    buttons.append(photo_add)

    video_label = Label(extension_win, text='Расширения для видео:', bg='#ffffff').place(x=ref_x, y=ref_y+80)
    video_text = Text(extension_win, height=1, width=22, highlightthickness=0).place(x=ref_x+174, y=ref_y+81)
    video_more_info = Button(extension_win, image=down,
                             highlightthickness=0, bd=0, bg='#ffffff', command=fuck_me_please_in_the_ass_please)
    video_more_info.place(x=ref_x+225, y=ref_y+115)

    root.bind('<Escape>', destroy)




class App:
    def __init__(self):
        self.win = Tk()
        self.win.title('*app name*')
        self.win.geometry('400x300+700+300')


def special_file():
    pass

def help():
    pass


# меню------------------------------
mainmenu = Menu(root)
root.config(menu=mainmenu)

file_manage = Menu(mainmenu, tearoff=0)
file_manage.add_command(label='Добавить расширения                    Ctrl+E', command=add_extensions)
file_manage.add_command(label='Специальные файлы/папки          Ctrl+D')
file_manage.add_command(label='Настройки                                         Ctrl+S')

mainmenu.add_cascade(label='управление', menu=file_manage)
mainmenu.add_command(label='справка')
# -----------------------------------

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


status = Label(root, text='Текущее состояние: ', bg='#ffffff')
status.place(x=10, y=265)

second_status = Label(root, text='(выкл)', bg='#ffffff')
second_status.place(x=185, y=265)

lab = Label(root, image=notactive, bg='#ffffff')
lab.place(x=162, y=266)

on_off = Button(root, image=off, highlightthickness=0, bd=0, bg='#ffffff')
on_off.place(x=250, y=237)

log_field = Text(width=400, height=15, state=DISABLED)
log_field.place(x=0, y=0)
# ----------------------------------------

# root.protocol("WM_DELETE_WINDOW", close)
root.bind('<Button-1>', a)
root.bind('<Control-e>', add_extensions)

root.mainloop()
