import os
import time
import shutil
import locale
import getpass
import translation

log_file = 'logs.log'
language_file = 'lang.conf'

logs = False; langs = False; confs = False
for i in range(2):
    try:
        log = open(log_file, 'r')
        logs = True; log.close()

        lang = open(language_file, 'r')
        langs = True; lang.close()

    except FileNotFoundError:
        if (not logs) or (not langs) or (not confs):
            if not logs:
                open(log_file, 'w+')
            else:
                open(language_file, 'w+')

language = locale.getdefaultlocale(); language = language[0][:2]
print(language)
dirs = None

for line in open(language_file, 'r'):
    if eval(line)['Language'] == language:
        dirs = eval(line)

if not dirs:
    dirs = translation.translate_to_other_lang(language)
print(dirs)

user = getpass.getuser()
LOGS = True


_from = '/home/' + user + '/'


ways = {
    'img': _from + dirs['Pictures'] + '/',
    'vid': _from + dirs['Videos'] + '/',
    'aud': _from + dirs['Music'] + '/',
    'doc': _from + dirs['Documents'] + '/',
}


class Transfer:
    def __init__(self, file_type: str):
        '''
        :param type: File type. Available types: 'doc', 'vid', 'img', 'aud', 'arh'.
        '''

        file = open('config.conf', 'r')

        for line in file.readlines():
            where_to_look = line[:line.find('=')]
            what_to_keep = line[line.find('=')+1:]

            if where_to_look == 'img':
                self.img = what_to_keep
            elif where_to_look == 'vid':
                self.vid = what_to_keep
            elif where_to_look == 'doc':
                self.doc = what_to_keep
            elif where_to_look == 'aud':
                self.aud = what_to_keep
            else:
                self.arh = what_to_keep

        ratios = {
            'img': self.img,
            'vid': self.vid,
            'aud': self.aud,
            'arh': self.arh,
            'doc': self.doc
        }

        self.__extensions = ratios[file_type]
        self.sp = False
        self.type = file_type
        self.path = ways[file_type]

    def add_special_moves(self, special_files: list, special_dirs: list):
        self.__special_files = special_files
        self.__special_dirs = special_dirs
        self.sp = True

        if len(self.__special_dirs) > 1 and (len(self.__special_files) != len(self.__special_dirs)):
            raise 'each special file must have own directory'

        for i in range(len(special_dirs)):
            try:
                os.mkdir(self.path + special_dirs[i])
            except FileExistsError:
                continue

    def __calculate_size(self, finally_path: str):
        file_size = os.stat(finally_path)
        file_size = file_size.st_size
        if file_size < 1000:
            postfix = 'B'
        elif file_size < 1000000:
            file_size = file_size * 0.001
            postfix = 'kB'
        elif file_size < 1000000000:
            file_size = file_size * 1.0E-6
            postfix = 'mB'
        return '{0:.1f} {1}'.format(file_size, postfix)

    def __convert_size(self, size: float, postfix: str = 'mb', current_postfix: str = 'gb') -> float:
        convert_to_mb = {
            'b': lambda x: x / 1e+6,
            'kb': lambda x: x / 1000,
            'mb': lambda x: x,
        }

        convert_to_gb = {
            'b': lambda x: x / 1e+9,
            'kb': lambda x: x / 1e+6,
            'mb': lambda x: x / 1000,
            'gb': lambda x: x
        }

        if current_postfix == 'mb':
            new_size = convert_to_mb[postfix](size)
        else:
            new_size = convert_to_gb[postfix](size)

        return new_size


    def __logs(self, new_loc, size):
        for line in open('config.conf', 'r').readlines():
            if line[:line.find('=')] == 'stats':
                old = line

        new = eval(old[old.find('=')+1:])
        total_files_size = new['size']
        postfix_for_current_file = size.split(' ')[1]
        postfix_for_moved_files = new['postfix']

        convert_size = self.__convert_size(float(size.split(' ')[0]),
                                 postfix_for_current_file.lower(),
                                 postfix_for_moved_files)

        total_files_size += convert_size
        if postfix_for_moved_files == 'mb' and total_files_size > 1000:
            total_files_size = self.__convert_size(total_files_size)
            new['postfix'] = 'gb'

        new['size'] = round(total_files_size, 2)
        new['moved'] += 1
        new = 'stats=' + str(new) + '\n'


        with open('config.conf', 'r') as file:
            data = file.read()
            data = data.replace(old, new)
        with open('config.conf', 'w') as file:
            file.write(data)

        log = 'new location: ' + new_loc + '; size: ' + size + '; type: ' + self.type
        file = open(log_file, 'a')
        file.write(log + '\n\n')
        file.close()

    def __move_special_files(self, file, _from,):
        for i in range(len(self.__special_files)):
            if file.find(self.__special_files[i]) != -1:
                to_ = self.path + self.__special_dirs[i] + '/' + file
                from_ = _from + file
                file_size = self.__calculate_size(from_)
                new_location = shutil.move(from_, to_)
                if LOGS:
                    self.__logs(new_location, file_size)
                return 1
        return -1

    def move(self, files: list,  _from):
        '''
        start manage for specific file(video/image/...)

        :param files: File list for further iteration
        :param _from: Start were will be seen specified file extensions
        :return: None
        '''

        for file in files:
            if file[file.find('.')+1:] in self.__extensions:
                if self.sp:
                    code = self.__move_special_files(file, _from)
                    if code == 1: continue

                to_ = self.path + file
                from_ = _from + file
                print(from_)
                file_size = self.__calculate_size(from_)
                new_location = shutil.move(from_, to_)
                if LOGS:
                    self.__logs(new_location, file_size)


class Manager:
    def __init__(self, *args: Transfer):
        self.__all_types = args
        self.__from = _from + dirs['Downloads'] + '/'

    def start_manage(self, files):
        for type in self.__all_types:
            type.move(files, self.__from)


class Create:
    def __init__(self, *extensions):
        self.new_type_extensions = extensions


class Utility:
    def __init__(self, manager: Manager):
        self.__manager = manager
        self.__break_mainloop = False

    def start(self, is_exit: int):
        while True:
            if is_exit == 0:
                break

            for root, dirs, files in os.walk(f'/home/{user}/Загрузки'):
                self.__manager.start_manage(files)
            time.sleep(1.5)

    def exit(self):
        self.__break_mainloop = False


images = Transfer('img')
images.add_special_moves(['minah', 'feet'], ['chaesu', 'feet'])
audio = Transfer('aud')
videos = Transfer('vid')
docs = Transfer('doc')

manager = Manager(images, audio, videos, docs)
stop_utility = False
go_to_downloads = dirs['Downloads']

while True:
    for root, dirs, files in os.walk(f'/home/{user}/{go_to_downloads}'):
        manager.start_manage(files)
    time.sleep(1.5)


def stop():
    global stop_utility

    stop_utility = True
