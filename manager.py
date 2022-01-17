import math
import time
import os.path as path
from tkinter import *
import tkinter.font as font
from threading import Thread
from PIL import Image
from PIL import ImageTk


root = Tk()

app_width = 600
app_height = 400

screen_height = root.winfo_screenwidth()
screen_width = root.winfo_screenheight()

center_by_y = (screen_height // 2) - 200
center_by_x_for_mf = (screen_width // 2) - 200  # mf - main frame
center_by_x_for_tlf = (screen_height // 2) - 74       # tlf - top level frame

geometry_for_main_frame = f'{app_width}x{app_height}+{center_by_y}+{center_by_x_for_mf}'
geometry_for_tl_frame = f'400x150+{center_by_y}+{center_by_x_for_tlf}'
geometry_for_tl_frame_sp_files = f'400x200+{center_by_y}-{center_by_x_for_tlf}'

if not path.exists('config.conf'):
    first_launch_configs = "stats={'moved': 0, 'size': 0, 'postfix': 'mb'}\n" \
        "img=['png', 'jpg', 'ora', 'jpeg']\n" \
        "vid=['mp4', 'avi', 'mov', 'mkv', 'm4v']\n" \
        "doc=['pdf', 'docx', 'doc', 'djvu', 'odt', 'pptx', 'rtf']\n" \
        "aud=['mp3', 'aiff', 'au']\n" \
        "arh=['7z', 'jar', 'deb', 'rar', 'zip']\n\n"\
        "special=[]"

    with open('config.conf', 'w+') as configs:
        configs.write(first_launch_configs)

if not path.exists('logs.log'):
    open('logs.log', 'w+')


# ?????????????????????????????????????????????
active = PhotoImage(file='icons/active.png')
not_active = PhotoImage(file='icons/not-active.png')
# ?????????????????????????????????????????????

main_bg = '#4d4d4d'
text_fg = '#b3b3b3'
button_bg = '#666666'
button_ab = '#8c8c8c'  # ab - (active background)
text_label_bg = button_bg


in_add_ext = False
in_special_files = False
in_settings = False

types_sort = BooleanVar()
types_sort.set(1)

stack_sort = BooleanVar()
stack_sort.set(0)

root['bg'] = main_bg
root.title('Aid')
root.geometry(geometry_for_main_frame)
root.resizable(width=False, height=False)


def place_widget_on_center(widget, center_by: str):
    if center_by not in ['x', 'y']:
        raise ValueError('bad argument -> center_by: Available parameters - x or y')

    root.update()
    widget_x_center = widget.winfo_width // 2


class FileInfoBtn:
    def __init__(self, root, file_name: str, file_info, file_image: Image = None):
        img = ['png', 'jpg', 'ora', 'jpeg', 'bmp', 'gif']

        self._root = root
        self._name = file_name[file_name.rfind("/")+1:]
        self._info = file_info

        if self._name[self._name.find('.')+1:] in img:
            self._image = Image.open(file_name)
        elif not file_image:
            self._image = Image.open("icons/preview_template.png")
        else:
            self._image = file_image

        self._image = ImageTk.PhotoImage(self._image)

        self._frame = Canvas(self._root, width=150, height=150, bg=main_bg, highlightthickness=1)

    @staticmethod
    def __scaling_image(image, scale_width=150):
        (width, height) = image.size
        divider = math.ceil(width / scale_width)

        return (width // divider, height // divider)

    def place(self, x, y):
        self._frame.place(x=x, y=y)
        self._frame.create_image(75, 60, image=self._image)
        self._frame.create_text(75, 130, text=self._name, justify='center')


class AddExtensions:
    def __init__(self, root):
        self.__root = root
        self.__frame = Canvas(self.__root, width=400, height=300, bg=main_bg)
        self.__frame.place(x=0, y=0)

    def destroy_frame(self):
        global in_add_ext
        in_add_ext = False

        for widget in self.__generated_widgets:
            widget.delete_widgets()

        for widget in self.__head_widgets:
            widget.destroy()

    def __sort_according_by_type(self):
        global types_sort
        lines = [j for i in self.__canvas_lines for j in i]
        val = types_sort.get()
        color = {
            0: 'red',
            1: '#00ff00'
        }

        for i in lines:
            self.__frame.itemconfig(i, fill=color[val])

        for button in self.__disable_or_enable_buttons:
            if val == 0:
                button.configure(state=DISABLED)
            else:
                button.configure(state=NORMAL)

    def add_content(self):
        # ----HEAD----
        self.__back_button = Button(text='Назад', bd=0, bg=button_bg, activebackground=button_bg,
                                    command=self._destroy_frame)
        self.__back_button.place(x=5, y=5)

        self.__caption_font_size = font.Font(size=12)
        self.__all_ext = Label(text='Все просматриваемые расширения:', bg=main_bg, font=self.__caption_font_size)
        self.__all_ext.place(x=50, y=45)
        self.__frame.create_line(0, 70, 400, 70, fill='#cccccc')  # create a underline 1

        self.__sort_by_types = Checkbutton(self.__frame, variable=types_sort, onvalue=1, offvalue=0,
                                    text='Сортровать файлы согласно их типам',
                                    bg=main_bg, activebackground=main_bg,
                                    highlightthickness=0,
                                    command=self.__sort_according_by_type)  # checkbox
        self.__sort_by_types.place(x=24, y=85)
        # ------------

        self._photo = AddContentToSettingsFrame(self.__frame, 'img', 0)
        self._photo.add_widget()

        self._video = AddContentToSettingsFrame(self.__frame, 'vid', 1)
        self._video.add_widget()

        self._documents = AddContentToSettingsFrame(self.__frame, 'doc', 2)
        self._documents.add_widget()

        self._audios = AddContentToSettingsFrame(self.__frame, 'aud', 3)
        self._audios.add_widget()

        self._archives = AddContentToSettingsFrame(self.__frame, 'arh', 4)
        self._archives.add_widget()

        self.__generated_widgets = [self._photo, self._video, self._documents,
                                    self._documents, self._audios, self._archives]

        self.__disable_or_enable_buttons = []
        for button in self.__generated_widgets:
            self.__disable_or_enable_buttons.append(button.add_extensions)

        self.__head_widgets = [self.__frame, self.__sort_by_types, self.__back_button, self.__all_ext]

        self.__coord_of_the_last_widget = self._archives._indent_by_y+65+80
        self._types_sort_line1 = self.__frame.create_line(14, 95, 14, self.__coord_of_the_last_widget)
        self._types_sort_line2 = self.__frame.create_line(14, 95, 24, 95)
        self._types_sort_line3 = self.__frame.create_line(14, self.__coord_of_the_last_widget, 24,
                                                       self.__coord_of_the_last_widget)
        self.__canvas_lines = [self._types_sort_line1, self._types_sort_line2, self._types_sort_line3]

        self.__sort_according_by_type()


class AddContentToSettingsFrame(AddExtensions):
    def __init__(self, root, type, num_of_string):
        super().__init__(root)
        self.__postfixes = {
            'img': 'фотографий',
            'vid': 'видеофайлов',
            'doc': 'документов',
            'arh': 'архивов',
            'aud': 'аудиофайлов'
        }

        # tl - top level (enc.)
        self.__tl_frame_titles = {
            'img': 'Фотографии',
            'vid': 'Видеофайлы',
            'doc': 'Докумменты',
            'arh': 'Архивы',
            'aud': 'Аудиофайлы'
        }
        self.__type = type
        self.__num_of_string = num_of_string
        self.__root = root
        self.__ref_y = 130

    def delete_widgets(self):
        for widget in self.__all_widgets:
            widget.destroy()

    @staticmethod
    def __is_empty(string: str):
        for i in string:
            print(i)
            if i != '':
                return False
        return True

    def __add_ext_for_spec_type(self):
        def save():
            extensions = enter_area.get(1.0, END)
            extensions = extensions.strip()
            extensions = extensions.split(' ')

            extensions_is_empty = self.__is_empty(extensions)

            if enter_area.get(1.0, END) == '\n' or extensions_is_empty:
                error_text = Label(tl_frame, text='Невозможно сохранить изменения: поле ввода пустое', bg=main_bg,
                                   fg='#990000')
                error_text.place(x=5, y=30)

                enter_area.place(y=50)
                enter_area.config(height=3)
                return

            for i in open('config.conf', 'r').readlines():
                if self.__type in i:
                    old_string = i
                    new_string = eval(i[i.find('=')+1:])
                    break

            for i in extensions:
                if i == '':
                    continue
                print(i)
                new_string.append(i)

            new_string = f'{self.__type}' + '=' + str(new_string) + '\n'

            with open('config.conf', 'r') as file:
                data = file.read()
                data = data.replace(old_string, new_string)
            with open('config.conf', 'w') as file:
                file.write(data)

            tl_frame.destroy()

        tl_frame = Toplevel()   # tl - Top Level
        tl_frame.config(bg=main_bg)   # bg='#adad85'
        tl_frame.geometry(geometry_for_tl_frame)
        tl_frame.resizable(width=False, height=False)
        tl_frame.title(self.__tl_frame_titles[self.__type])

        main_label = Label(tl_frame, text='Запишите расширения через пробел: ', bg=main_bg)
        main_label.place(x=60, y=5)

        save_button = Button(tl_frame, text='Сохранить', highlightthickness=0, bd=0, bg=button_bg,
                             activebackground=button_ab, command=save)  #  bg='#999966,  activebackground='#b8b894'
        save_button.place(x=70, y=110)
        cancel_button = Button(tl_frame, text='Отменить', highlightthickness=0, bd=0, bg=button_bg,
                               activebackground=button_ab, command=lambda: tl_frame.destroy()).place(x=230, y=110)

        enter_area = Text(tl_frame, width=48, height=4, bg=text_label_bg, highlightthickness=0, bd=0)   # '#c2c2a3'
        enter_area.place(x=7, y=35)

    def __insert_extensions(self):
        configure_file = open('config.conf', 'r')
        self.__text_field.configure(state=NORMAL)
        extensions = ''

        for line in configure_file:
            if line[:line.find('=')] == self.__type:
                extensions = eval(line[line.find('=')+1:])
                break
        for i in extensions:
            i = '*.' + i + '; '
            self.__text_field.insert(1.0, i)
        self.__text_field.configure(state=DISABLED)

    def __more_info(self):
        pass

    def add_widget(self):
        self._indent_by_y = self.__ref_y + (80 * self.__num_of_string)

        text_label = Label(self.__root, text=f'Расширения для {self.__postfixes[self.__type]}:', bg=main_bg)
        text_label.place(x=30, y=self._indent_by_y)

        root.update()
        text_x = 30 + text_label.winfo_width() + 5
        text_width = (400 - text_x - 2) // 8

        self.__text_field = Text(self.__root, height=1, width=text_width, highlightthickness=0, bg=main_bg,
                                 state=DISABLED)
        self.__insert_extensions()
        self.__text_field.place(x=text_x, y=self._indent_by_y)
        root.update()

        self.add_extensions = Button(self.__root, text='Добавить', activebackground=button_ab, bd=0,
                               bg=button_bg, command=self.__add_ext_for_spec_type)
        self.add_extensions.place(x=50, y=self._indent_by_y+30)

        more_info = Button(self.__root, text='Подробнее', activebackground=button_ab, bd=0, bg=button_bg)
        more_info.place(x=275, y=self._indent_by_y+30)

        self.__all_widgets = [text_label, self.__text_field, self.add_extensions, more_info]


class MainFrame:
    def __init__(self):
        self.main_frame = Canvas(root, width=app_width, height=app_height, bg=main_bg)
        self.main_frame.pack()
        self.__is_active = 0
        self.__recent_files = None

        self.__create_frame()

    def __frame_bottom(self):
        status = Label(self.main_frame, text='Текущее состояние: ', bg=main_bg)
        status.place(x=10, y=app_height-35)   # 265

        self.on_or_off = Label(self.main_frame, text='(выкл)', bg=main_bg)
        self.on_or_off.place(x=185, y=app_height-35)

        self.indicator = self.main_frame.create_image(170, app_height-24, image=not_active)
        # Label(self.main_frame, image=not_active, bg=main_bg)

        self.launch_button = Button(self.main_frame, text='Включить', bd=0, bg=main_bg,
                                    activebackground=button_ab)
        self.launch_button.place(x=250, y=app_height-39)  # 261

    def insert_moved_files_statistics(self):
        statistic = open('config.conf', 'r')
        statistic = str(statistic.readlines())
        statistic = eval(statistic[statistic.find('=')+1: statistic.find('}')+1])
        ru_postfixes = {
            'mb': 'Мб',
            'gb': 'Гб'
        }

        files = statistic['moved']
        size = statistic['size']
        postfix = ru_postfixes[statistic['postfix']]

        self.__quantity_of_moved_files['text'] = f'Всего премещено файлов: {files}'
        self.__totalen_bruh['text'] = f'Общий размер всех файлов: {size} {postfix}'

        lines = []
        index = 0
        for line in open('logs.log', 'r').readlines():
            index += 1
            if index == 10:
                break

            lines.append(line)

        last_changes_list = []
        for line in lines:
            if line != '\n':
                last_changes_list.append(line.rstrip())

        for key, event in enumerate(last_changes_list):
            meta_event = last_changes_list[key]
            meta_event = meta_event[meta_event.find('/'): meta_event.find(';')]
            if len(meta_event) > 47:
                meta_event = meta_event[:47] + '...'
            last_changes_list[key] = meta_event

        self.__log_field.config(state=NORMAL)

        last_changes = ''
        for i in last_changes_list:
            last_changes += i + '\n\n'

        if last_changes != self.__recent_files:
            self.__log_field.insert(0.0, last_changes)
            self.__recent_files = last_changes

    def __create_frame(self):
        self.__frame_bottom()

        self.__quantity_of_moved_files = Label(self.main_frame, bg=main_bg)
        self.__quantity_of_moved_files.place(x=100, y=10)

        self.__totalen_bruh = Label(self.main_frame, bg=main_bg)
        self.__totalen_bruh.place(x=75, y=40)

        Label(self.main_frame, text='Последние изменения:', bg=main_bg).place(x=115, y=75)

        self.main_frame.create_line(0, 67, 400, 67, fill='#cccccc')

        self.__log_field = Text(self.main_frame, width=400, height=9, state=NORMAL, highlightthickness=0, bg=main_bg)
        self.__log_field.place(x=1, y=100)
        self.insert_moved_files_statistics()


class SpecialFiles:
    def __init__(self, root):
        self.is_empty = True
        for component in open('config.conf', 'r').readlines():
            if component[:component.find('=')] == 'special':
                lists = eval(component[component.find('=') + 1:])
                break
        if lists:
            self.is_empty = False

        self.__root = root

    def _destroy_frame(self):
        pass

    def add_content(self):
        if self.is_empty:
            font_size = font.Font(size=12)
            not_found = Label(image=nothing_found, bg=main_bg)
            not_found.place(x=130, y=100)
            not_found_text = Label(text='Тут ничего нет!', bg=main_bg, font=font_size)
            not_found_text.place(x=70, y=240)
            add_button = Button(text='добавить?', bd=0, font=font_size,
                                bg=main_bg, activebackground=button_ab, command=self.__add_files)
            add_button.place(x=210, y=237)
            return

    def __add_files(self):
        tl_frame = Toplevel()  # tl - Top Level
        tl_frame.config(bg=main_bg)
        tl_frame.geometry(geometry_for_tl_frame_sp_files)
        tl_frame.resizable(width=False, height=False)
        tl_frame.title('Добавление новой конфигурации')

        config_name_label = Label(tl_frame, text='Название конфигурации:', bg=main_bg).place(x=15, y=15)
        config_name = Entry(tl_frame, width=23, bg=text_label_bg, bd=0)
        config_name.place(x=200, y=15)

        special_names_label = Label(tl_frame, text='Укажите специальные имена:', bg=main_bg).place(x=15, y=75)

    def __print(self):
        current_y = 100
        a = []
        def pp():
            nonlocal current_y
            l = Label(text=str(current_y))
            l.place(x=30, y=current_y)
            a.append(l)
            print(a)
            current_y += 30

        def dest():
            nonlocal current_y
            current_y = 100
            for i in a:
                i.destroy()
        button = Button(text='add', command=pp)
        button.place(x=30, y=70)

        button = Button(text='destr', command=dest)
        button.place(x=120, y=70)


def get_cursor_cords(event):
    print(f'X: {event.x}; Y: {event.y}')


def add_extensions(event=None):
    # global in_add_ext
    # if in_add_ext or in_special_files or in_settings:
    #     return
    # else:
    #     in_add_ext = True
    #
    # # ----CREATE A NEW FRAME----
    # extension_frame = Canvas(width=400, height=300, bg=main_bg)
    # extension_frame.place(x=0, y=0)
    # # --------------------------
    #
    # def destroy(event=None):
    #     global in_add_ext
    #     in_add_ext = False
    #     to_destroy_wid.delete()
    #     to_destroy_head.delete()
    #
    # def checkbox_type_sort():
    #     global types_sort
    #     lin = [j for i in lines for j in i]
    #     val = types_sort.get()
    #     color = {
    #         0: 'red',
    #         1: '#00ff00'
    #     }
    #
    #     for i in lin:
    #         extension_frame.itemconfig(i, fill=color[val])
    #
    #     for i in disabled:
    #         if val == 0:
    #             i.configure(state=DISABLED)
    #         else:
    #             i.configure(state=NORMAL)
    #
    #
    # back_button = Button(text='Назад', bd=0, bg=button_bg, activebackground=button_bg, command=destroy)
    # back_button.place(x=5, y=5)
    #
    # # ----HEAD----
    # caption_font_size = font.Font(size=12)
    # all_ext = Label(text='Все просматриваемые расширения:', bg=main_bg, font=caption_font_size)
    # all_ext.place(x=50, y=45)
    # extension_frame.create_line(0, 70, 400, 70, fill='#cccccc')     # create a underline 1
    #
    # sort_by_types = Checkbutton(extension_frame, variable=types_sort, onvalue=1, offvalue=0,
    #                               text='Сортровать файлы согласно их типам',
    #                               bg=main_bg, activebackground=main_bg,
    #                             highlightthickness=0, command=checkbox_type_sort)    # checkbox
    # sort_by_types.place(x=24, y=85)
    # # ------------
    #
    # photo = AddTypeWidget(extension_frame, 'img', 0)
    # photo.add_widget()
    #
    # video = AddTypeWidget(extension_frame, 'vid', 1)
    # video.add_widget()
    #
    # documents = AddTypeWidget(extension_frame, 'doc', 2)
    # documents.add_widget()
    #
    # audios = AddTypeWidget(extension_frame, 'aud', 3)
    # audios.add_widget()
    #
    # archives = AddTypeWidget(extension_frame, 'arh', 4)
    # archives.add_widget()
    #
    # last_label_y_cord = archives.indent_by_y+65+80   # need to calculate lines width and height
    #
    # to_destroy_wid = DeleteWidgets(photo, video, documents, audios, archives)
    # to_destroy_head = Destroy(extension_frame, back_button, all_ext)
    #
    # disabled = [photo.add_extensions, video.add_extensions]
    #
    # types_sort_line1 = extension_frame.create_line(14, 95, 14, last_label_y_cord)
    # types_sort_line2 = extension_frame.create_line(14, 95, 24, 95)
    # types_sort_line3 = extension_frame.create_line(14, last_label_y_cord, 24, last_label_y_cord)
    #
    # lines = []
    # lines.append([types_sort_line1, types_sort_line2,  types_sort_line3])
    #
    # checkbox_type_sort()
    # checkbox_stack_sort()
    global in_add_ext
    if in_add_ext or in_special_files or in_settings:
        return
    else:
        in_add_ext = True

    frame = AddExtensions(root)
    frame.add_content()

    root.bind('<Escape>', frame.destroy_frame)


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

        frame.delete()

    ref_x = 30; ref_y = 105

    back_button = Button(text='Назад', bd=0, bg=button_bg, activebackground=button_bg, command=destroy)
    back_button.place(x=5, y=5)
    #
    caption_font_size = font.Font(size=12)
    spec_files_head = Label(text='Особые файлы и папки:', bg=main_bg, font=caption_font_size)
    spec_files_head.place(x=97, y=45)


    fr = SpecialFiles()

    # spec_files = Label(text='Специальные имена:', bg=main_bg);  spec_files.place(x=ref_x, y=ref_y)
    # spec_files_text = Text(sp_file_frame, height=1, width=25, highlightthickness=0, bg=text_label_bg)
    # spec_files_text.place(x=ref_x+160, y=ref_y)
    # add_spec_files = Button(text='Добавить', activebackground=button_ab, bd=0, bg=button_bg)
    # add_spec_files.place(x=ref_x+20, y=ref_y+30)
    #
    #
    # spec_dirs = Label(text='Специальные директории:', bg=main_bg);   spec_dirs.place(x=ref_x, y=ref_y+90)
    # spec_dirs_text = Text(sp_file_frame, height=1, width=20, highlightthickness=0, bg=text_label_bg)
    # spec_dirs_text.place(x=ref_x+200, y=ref_y+90)
    # add_spec_dirs = Button(text='Добавить', activebackground=button_ab, bd=0, bg=button_bg)
    # add_spec_dirs.place(x=ref_x+20, y=ref_y+120)
    #
    # frame.add_widgets(back_button, spec_files_head, add_spec_files, spec_files_head, spec_files, spec_dirs,
    #                   add_spec_dirs)

    root.bind('<Escape>', destroy)


def settings(event=None):
    global in_settings
    if in_settings or in_special_files or in_add_ext:
        return
    else:
        in_settings = True

    # ----CREATE A NEW FRAME----
    settings_frame = Frame(root, width=400, height=300, bg=main_bg)
    settings_frame.place(x=0, y=0)
    frame = Destroy(settings_frame)
    # --------------------------

    def destroy(event=None):
        global in_settings
        in_settings = False

        frame.destroy()

    back_button = Button(text='Назад', bd=0, bg=button_bg, activebackground=button_bg, command=destroy)
    back_button.place(x=5, y=5)

    caption_font_size = font.Font(size=12)
    setngs_lab = Label(text='Настройки утилиты:', bg=main_bg, font=caption_font_size)
    setngs_lab.place(x=114, y=40)

    frame.add_widgets(back_button, setngs_lab)
    root.bind('<Escape>', destroy)


def update_main_frame():
    while True:
        main_frame.insert_moved_files_statistics()
        time.sleep(3)


# ----MENU CREATE----
menu = Menu(root, bg='#404040')
root.config(menu=menu)

# options = Menu(menu, tearoff=0, bg=main_bg, activebackground=button_ab)
# options.add_command(label='Добавить расширения                    Ctrl+E', command=add_extensions)
# options.add_command(label='Специальные файлы/папки          Ctrl+D', command=special_files)
# options.add_command(label='Настройки                                         Ctrl+S', command=settings)

# menu.add_cascade(label='Настройки', menu=options, activebackground=button_ab)
# menu.add_cascade(label='Справка', command=help, activebackground=button_ab)

menu.add_command(label='Настройки', activebackground=button_ab, command=add_extensions)
menu.add_command(label='Справка', activebackground=button_ab, command=help)
# -------------------

# log_field = Text(width=400, height=15, state=NORMAL, bg=main_bg)
# log_field.place(x=0, y=0)

# def insert_text_on_main_screen():
#     total_moved = None
#     for line in open('config.conf', 'r').readlines():
#         if line[:line.find('=')] == 'total_moved':
#             total_moved = line[line.find('=')+1:]
#
#     total_moved = '\t' + '   Всего перемещено файлов: ' + total_moved
#     log_field.insert(1.0, total_moved)


# ----MAIN FRAME----
# status = Label(root, text='Текущее состояние: ', bg=main_bg)
# status.place(x=10, y=265)
#
# on_or_off = Label(root, text='(выкл)', bg=main_bg)
# on_or_off.place(x=185, y=265)
#
# indicator = Label(root, image=notactive, bg=main_bg)
# indicator.place(x=162, y=266)
#
# launch_button = Button(root, image=off, highlightthickness=0, bd=1, relief=SUNKEN,
#                        bg=main_bg, activebackground=button_ab)
# launch_button.place(x=250, y=237)
#
# log_field.config(command=insert_text_on_main_screen())
# ------------------

# main_frame = MainFrame()
a = FileInfoBtn(root, 'a', [])
a.place(x=10, y=10)


# ----KEYS BIND----
root.bind('<Control-e>', add_extensions)
# root.bind('<Control-d>', special_files)
# root.bind('<Control-s>', settings)
root.bind('<Button-1>', get_cursor_cords)
# -----------------

Thread(target=update_main_frame).start()
root.mainloop()
# root.protocol("WM_DELETE_WINDOW", close)
