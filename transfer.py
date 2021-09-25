import os
import time
import shutil
import locale
import getpass
from google_trans_new import google_translator

language = locale.getdefaultlocale(); language = language[0][:2]
if language == 'be': language = 'ru'
else: language = 'en'
user = getpass.getuser()
LOGS = True

translator = google_translator()
translate_text = translator.translate('привет', lang_tgt='en')
print(translate_text)

_from = '/home/' + user + '/'
dirs = {
    'downloads': {
        'en': 'Downloads',
        'ru': 'Загрузки'
    },
    'images': {
        'en': 'Pictures',
        'ru': 'Изображения'
    },
    'videos': {
        'en': 'Videos',
        'ru': 'Видео'
    },
    'music': {
        'en': 'Music',
        'ru': 'Музыка'
    },
    'docks': {
        'en': 'Documents',
        'ru': 'Документы'
    },
}

ways = {
    'img': _from + dirs['images'][language] + '/',
    'vid': _from + dirs['videos'][language] + '/',
    'aud': _from + dirs['music'][language] + '/',
    'doc': _from + dirs['docks'][language] + '/',
    'arc': _from + dirs['docks'][language] + '/',
}

class Transfer:
    def __init__(self, *extensions):
        '''

        :param extensions:  All extensions. You must create a separate copy of class for every file type
        '''
        self.__extensions = extensions
        self.sp = False

    def add_special_moves(self, special_files: list, special_dirs: list):
        '''

        :param special_files:
        :param special_dirs:
        :return:
        '''
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

    def file_type(self, type: str):
        '''
        
        :param type:
        :return:
        '''
        self.__all_types = ['txt', 'doc', 'vid', 'img', 'aud', 'arh']
        if type not in self.__all_types:
            raise 'the file type, when you specified does not exist or is not supported by this version of the utility'
        self.type = type
        self.path = ways[self.type]

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

    def __move_special_files(self, file, _from,):
        for i in range(len(self.__special_files)):
            if file.find(self.__special_files[i]) != -1:
                to_ = self.path + self.__special_dirs[i] + '/' + file
                from_ = _from + file
                file_size = self.__calculate_size(from_)
                new_location = shutil.move(from_, to_)
                if LOGS:
                    log = 'new location: ' + new_location + '; size: ' + file_size + '; type: ' + self.type
                    file = open('logs.txt', 'a'); file.write(log+'\n\n')
                    file.close()
                print(new_location, file_size)
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
                    log = 'new location: ' + new_location + '; size: ' + file_size + '; type: ' + self.type
                    file = open('logs.txt', 'a'); file.write(log+'\n\n')
                    file.close()
                print(new_location, file_size)


class ManageAllFiles:
    def __init__(self, *args: Transfer):
        self.__all_types = args
        self.__from = _from + dirs['downloads'][language] + '/'

    def start_manage(self, files):
        for type in self.__all_types:
            type.move(files, self.__from)


_from = '/home/qlop/'



# for future gui app
img = ['*.png', '*.jpg', '*.ora']
aud = ['*.mp3', '*.aiff', '*.au']
vid = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.m4v']
doc = ['*.pdf', '*.docx', '*.doc']
text = ['*.txt']
# ----


images = Transfer('png', 'jpg', 'ora'); images.file_type('img')
images.add_special_moves(['minah'], ['chaesu'])

audio = Transfer('mp3', 'aiff', 'au'); audio.file_type('aud')
videos = Transfer('mp4', 'avi', 'mov', 'mkv', 'm4v'); videos.file_type('vid')
docs = Transfer('pdf', 'docx', 'doc', 'djvu'); docs.file_type('doc')


manager = ManageAllFiles(images, audio, videos, docs)

# while True:
#     for root, dirs, files in os.walk(f'/home/{user}/Загрузки'):
#         manager.start_manage(files)
#     time.sleep(1.5)
