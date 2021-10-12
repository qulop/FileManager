import os
import time
import shutil
import locale
import getpass
import fileinput
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
dirs = None

for line in open(language_file, 'r'):
    if eval(line)['Language'] == language:
        dirs = eval(line)

if not dirs:
    dirs = translation.translate(language)

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
    def __init__(self, type: str):
        '''
        :param type: File type. Available types: 'doc', 'vid', 'img', 'aud', 'arh'.
        '''

        self.__all_types = ['doc', 'vid', 'img', 'aud']
        if type not in self.__all_types:
            raise 'the file type, when you specified does not exist or is not supported by this version of the utility'
        self.img = ['png', 'jpg', 'ora']
        self.doc = ['pdf', 'docx', 'doc', 'djvu']
        self.vid = ['mp4', 'avi', 'mov', 'mkv', 'm4v']
        self.aud = ['mp3', 'aiff', 'au']
        self.arh = ['7z', 'jar', 'deb', 'rar', 'zip']

        ratios = {
            'img': self.img,
            'vid': self.vid,
            'aud': self.aud,
            'arh': self.arh,
            'doc': self.doc
        }

        self.__extensions = ratios[type]
        self.sp = False
        self.type = type
        self.path = ways[type]

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

    def __logs(self, new_loc, size):
        log = open('logs.log', 'r')
        total = eval(log.readline())
        total_moved_files = total['moved'] + 1
        total_size = total['size'] + size

        with fileinput.input(files='logs.log', inplace=True) as file:
            for line in file:
                if fileinput.lineno() == 1:
                    print("{'moved': %d, 'size': %.1f" % (total_moved_files, total_size))
                else:
                    print(line, end='')

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


# for future gui app
img = ['*.png', '*.jpg', '*.ora']
aud = ['*.mp3', '*.aiff', '*.au']
vid = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.m4v']
doc = ['*.pdf', '*.docx', '*.doc']
text = ['*.txt']
# ----

images = Transfer('img')
images.add_special_moves(['minah'], ['chaesu'])
audio = Transfer('aud')
videos = Transfer('vid')
docs = Transfer('doc')

manager = Manager(images, audio, videos, docs)


while True:
        for root, dirs, files in os.walk(f'/home/{user}/Загрузки'):
            manager.start_manage(files)
        time.sleep(1.5)
