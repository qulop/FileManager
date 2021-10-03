from tkinter import *

root = Tk()

active = PhotoImage(file='icons/active.png')
notactive = PhotoImage(file='icons/notactive.png')
on = PhotoImage(file='icons/switch-on.png')
off = PhotoImage(file='icons/switch-off.png')
up = PhotoImage(file='icons/up.png')
down = PhotoImage(file='icons/down.png')

main_bg = '#4d4d4d'
text_fg = '#b3b3b3'
button_bg = '#666666'
button_ab = button_bg  # ab - (active background)
text_label_bg = button_bg


def get_cursor_cords(event):
    print(f'X: {event.x}; Y: {event.y}')


def add_extensions(event=None):
    # ----CREATE A NEW FRAME----
    extension_frame = Canvas(root, width=400, height=300, bg=main_bg)
    extension_frame.place(x=0, y=0)
    # --------------------------

    def add_ext_for_spec_type():
        pass

    def destroy(event=None):
        extension_frame.destroy()
        for widget in widgets:
            widget.destroy()

    widgets = []    # создаем массив ссылок на виджеты для возможности их(виджеты) стереть в случае выхода из фрейма
    ref_x = 30; ref_y = 130
    type_sort_lines_color = 'red'

    back_button = Button(text='Назад', bd=0, bg=button_bg, activebackground=button_bg, command=destroy)
    back_button.place(x=5, y=5)
    widgets.append(back_button)

    Label(text='Все просматриваемые расширения:', bg=main_bg).place(x=74, y=45)
    extension_frame.create_line(0, 70, 400, 70, fill='#cccccc')     # create a underline 1

    bool_var = BooleanVar()
    bool_var.set(1)
    sort_by_types = Checkbutton(extension_frame, variable=bool_var, onvalue=1, offvalue=0,
                                  text='Сортровать файлы по их типам(фото/видео/...)',
                                  bg=main_bg, activebackground=main_bg, highlightthickness=0)       # checkbox
    sort_by_types.place(x=ref_x-6, y=85)

    # ----PHOTOS----
    Label(text='Расширения для фотографий:', bg=main_bg).place(x=ref_x, y=ref_y)
    photo_text_field = Text(extension_frame, height=1, width=18, highlightthickness=0, bg=main_bg)
    photo_text_field.place(x=ref_x+220, y=ref_y)
    photo_add_new_ext = Button(text='Добавить', activebackground=button_ab, bd=0,
                               bg=button_bg).place(x=ref_x+20, y=ref_y+30)
    photo_more_info = Button(image=down, activebackground=button_ab, bd=1, relief=SUNKEN, bg=main_bg)
    photo_more_info.place(x=ref_x+180, y=ref_y+30)

    last_label_x_cord = ref_x
    last_label_y_cord = ref_y+65    # need to calculate lines width and height

    types_sort_line1 = extension_frame.create_line(14, 95, 14, last_label_y_cord, fill=type_sort_lines_color)
    types_sort_line2 = extension_frame.create_line(14, 95, 24, 95, fill=type_sort_lines_color)
    types_sort_line3 = extension_frame.create_line(14, last_label_y_cord, 24, last_label_y_cord,
                                                   fill=type_sort_lines_color)



    root.bind('<Escape>', destroy)


def special_files(event=None):
    pass


def settings(event=None):
    pass


def help():
    pass


# ----HEAD----
root['bg'] = main_bg
root.title('File manager')
root.geometry('400x300+700+300')
# -------------

# ----MENU CREATE----
menu = Menu(root, bg='#404040')
root.config(menu=menu)

options = Menu(menu, tearoff=0, bg=main_bg, activebackground=button_ab)
options.add_command(label='Добавить расширения                    Ctrl+E', command=add_extensions)
options.add_command(label='Специальные файлы/папки          Ctrl+D')
options.add_command(label='Настройки                                         Ctrl+S')

menu.add_cascade(label='Управление', menu=options, activebackground=button_ab)
menu.add_cascade(label='Справка', command=help, activebackground=button_ab)
# -------------------


# ----MAIN FRAME----
status = Label(root, text='Текущее состояние: ', bg=main_bg)
status.place(x=10, y=265)

on_or_off = Label(root, text='(выкл)', bg=main_bg)
on_or_off.place(x=185, y=265)

indicator = Label(root, image=notactive, bg=main_bg)
indicator.place(x=162, y=266)

launch_button = Button(root, image=off, highlightthickness=0, bd=1, relief=SUNKEN,
                       bg=main_bg, activebackground=button_ab)
launch_button.place(x=250, y=237)

log_field = Text(width=400, height=15, state=DISABLED, bg=main_bg)
log_field.place(x=0, y=0)
# ------------------

# ----KEYS BIND----
root.bind('<Control-e>', add_extensions)
root.bind('<Button-1>', get_cursor_cords)
# -----------------

root.mainloop()
