from tkinter import *
import tkinter.font as font
import os.path as file

file = file.exists('settings.conf')
if not file:
    first_launch = {
    'type_sort': True,
    'heap_sort': False,
    'autoload': True,
    'logs': True
}
    with open('settings.conf', 'w+') as settings:
        settings.write(str(first_launch))

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
button_ab = '#8c8c8c'  # ab - (active background)
text_label_bg = button_bg


in_add_ext = False
in_special_files = False
in_settings = False


class Destroy:
    def __init__(self, frame):
        self.frame = frame

    def add_widgets(self, *widgets):
        self.widgets = widgets

    def destroy(self):
        for widget in self.widgets:
            widget.destroy()
        self.frame.destroy()


def get_cursor_cords(event):
    print(f'X: {event.x}; Y: {event.y}')


def add_extensions(event=None):
    global in_add_ext
    if in_add_ext or in_special_files or in_settings:
        return
    else:
        in_add_ext = True

    # ----CREATE A NEW FRAME----
    extension_frame = Canvas(root, width=400, height=300, bg=main_bg)
    extension_frame.place(x=0, y=0)
    frame = Destroy(extension_frame)
    # --------------------------

    def add_ext_for_spec_type():
        tl_frame = Toplevel()   # tl - Top Level
        tl_frame.config(bg=main_bg)   # bg='#adad85'
        tl_frame.geometry('400x125+700+380')
        tl_frame.resizable(width=False, height=False)
        tl_frame.title('Photos')

        main_label = Label(tl_frame, text='Запишите расширения через пробел: ', bg=main_bg)
        main_label.place(x=53, y=5)

        save_button = Button(tl_frame, text='Сохранить', highlightthickness=0, bd=0, bg=button_bg,      #  bg='#999966,  activebackground='#b8b894'
                      activebackground=button_ab);      save_button.place(x=70, y=90)
        cancel_button = Button(tl_frame, text='Отменить', highlightthickness=0, bd=0, bg=button_bg, activebackground=button_ab,
                        command=lambda: tl_frame.destroy()).place(x=230, y=90)

        enter_area = Text(tl_frame, width=48, height=3, bg=text_label_bg, highlightthickness=0, bd=0)   # '#c2c2a3'
        enter_area.place(x=7, y=30)

    def destroy(event=None):
        global in_add_ext
        in_add_ext = False
        frame.destroy()

    ref_x = 30; ref_y = 130
    type_sort_lines_color = 'red'

    back_button = Button(text='Назад', bd=0, bg=button_bg, activebackground=button_bg, command=destroy)
    back_button.place(x=5, y=5)

    # ----HEAD----
    caption_font_size = font.Font(size=12)
    all_ext = Label(text='Все просматриваемые расширения:', bg=main_bg, font=caption_font_size)
    all_ext.place(x=50, y=45)
    extension_frame.create_line(0, 70, 400, 70, fill='#cccccc')     # create a underline 1

    bool_var = BooleanVar()
    bool_var.set(1)
    sort_by_types = Checkbutton(extension_frame, variable=bool_var, onvalue=1, offvalue=0,
                                  text='Сортровать файлы по их типам',
                                  bg=main_bg, activebackground=main_bg, highlightthickness=0)       # checkbox
    sort_by_types.place(x=ref_x-6, y=85)
    # ------------

    # ----PHOTOS----
    photo_ext = Label(text='Расширения для фотографий:', bg=main_bg);   photo_ext.place(x=ref_x, y=ref_y)
    photo_text_field = Text(extension_frame, height=1, width=18, highlightthickness=0, bg=main_bg)
    photo_text_field.place(x=ref_x+220, y=ref_y)
    photo_add_new_ext = Button(text='Добавить', activebackground=button_ab, bd=0,
                               bg=button_bg, command=add_ext_for_spec_type)
    photo_add_new_ext.place(x=ref_x+20, y=ref_y+30)
    # photo_more_info = Button(image=down, activebackground=button_ab, bd=1, relief=SUNKEN, bg=main_bg)
    # photo_more_info.place(x=ref_x+180, y=ref_y+30)
    # --------------

    # ----VIDEOS----
    video_ext = Label(text='Расширения для видеофайлов:', bg=main_bg);   video_ext.place(x=ref_x, y=ref_y+80)
    video_text_field = Text(extension_frame, height=1, width=17, highlightthickness=0, bg=main_bg)
    video_text_field.place(x=ref_x+225, y=ref_y+80)
    video_add_new_ext = Button(text='Добавить', activebackground=button_ab, bd=0,
                               bg=button_bg, command=add_ext_for_spec_type)
    video_add_new_ext.place(x=ref_x+20, y=ref_y+110)
    # video_more_info = Button(image=down, activebackground=button_ab, bd=1, relief=SUNKEN, bg=main_bg)
    # video_more_info.place(x=ref_x+180, y=ref_y+30)

    last_label_x_cord = ref_x
    last_label_y_cord = ref_y+65+80   # need to calculate lines width and height

    frame.add_widgets(all_ext, photo_ext, photo_add_new_ext, back_button, video_ext, video_add_new_ext)

    types_sort_line1 = extension_frame.create_line(14, 95, 14, last_label_y_cord, fill=type_sort_lines_color)
    types_sort_line2 = extension_frame.create_line(14, 95, 24, 95, fill=type_sort_lines_color)
    types_sort_line3 = extension_frame.create_line(14, last_label_y_cord, 24, last_label_y_cord,
                                                   fill=type_sort_lines_color)

    root.bind('<Escape>', destroy)


def special_files(event=None):
    global in_special_files
    if in_add_ext or in_special_files or in_settings:
        return
    else:
        in_special_files = True

    # ----CREATE A NEW FRAME----
    sp_file_frame = Frame(root, width=400, height=300, bg=main_bg)
    sp_file_frame.place(x=0, y=0)
    frame = Destroy(sp_file_frame)
    # --------------------------

    def destroy(event=None):
        global in_special_files
        in_special_files = False

        frame.destroy()

    ref_x = 30; ref_y = 105

    back_button = Button(text='Назад', bd=0, bg=button_bg, activebackground=button_bg, command=destroy)
    back_button.place(x=5, y=5)

    caption_font_size = font.Font(size=12)
    spec_files_head = Label(text='Особые файлы и папки:', bg=main_bg, font=caption_font_size)
    spec_files_head.place(x=97, y=45)

    spec_files = Label(text='Специальные имена:', bg=main_bg);  spec_files.place(x=ref_x, y=ref_y)
    add_spec_files = Button(text='Добавить', activebackground=button_ab, bd=0, bg=button_bg)
    add_spec_files.place(x=ref_x+20, y=ref_y+30)

    spec_dirs = Label(text='Специальные директории:', bg=main_bg);   spec_dirs.place(x=ref_x, y=ref_y+90)
    add_spec_dirs = Button(text='Добавить', activebackground=button_ab, bd=0, bg=button_bg)
    add_spec_dirs.place(x=ref_x+20, y=ref_y+120)

    frame.add_widgets(back_button, spec_files_head, add_spec_files, spec_files_head, spec_files, spec_dirs,
                      add_spec_dirs)


    root.bind('<Escape>', destroy)


def settings(event=None):
    print('here2')
    global in_settings
    if in_settings:
        return
    else:
        in_settings = True

    def destroy(event=None):
        global in_settings
        in_settings = False

    # root.bind('<Escape>', destroy)


def help():
    pass


# ----HEAD----
root['bg'] = main_bg
root.title('File manager')
root.geometry('400x300+700+300')
root.resizable(width=False, height=False)
# -------------

# ----MENU CREATE----
menu = Menu(root, bg='#404040')
root.config(menu=menu)

options = Menu(menu, tearoff=0, bg=main_bg, activebackground=button_ab)
options.add_command(label='Добавить расширения                    Ctrl+E', command=add_extensions)
options.add_command(label='Специальные файлы/папки          Ctrl+D', command=special_files)
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
root.bind('<Control-d>', special_files)
# root.bind('<Control-s>', settings)
root.bind('<Button-1>', get_cursor_cords)
# -----------------

root.mainloop()
