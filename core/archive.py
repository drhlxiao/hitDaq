
import os
from datetime import datetime


class Archive(object):

    def __init__(self):
        self.buffer = []
        self.filename = 'run_1.dat'
        self.fp = None
        self.enabled = False
        self.buffer_size = 4096
        self.folder='.'
        self.file_size_written = 0
        self.current_buffer_size = 0
        self.max_file_size = 4096*500

    def enable_archive(self, stat):
        self.enabled = stat

    def set_buffer_size(self, size):
        self.buffer_size = size

    def set_file_maxsize(self, size):
        self.max_file_size = size

    def is_running(self):
        return self.enabled

    def close(self):
        self.stop()
    


    def write_one(self, row, with_time=True):
        if not self.fp or not self.enabled:
            return
        if isinstance(row, list):
            stream = ','.join([str(x) for x in row])
        else:
            stream = str(row)
        
        line = datetime.now().isoformat() +','+ stream if with_time else stream
        try:
            self.fp.write(f'{line}\n')
        except IOError:
            self.erro('Error. Trying to write closed file')


    def current_filename(self):
        if self.enabled:
            return self.filename
        return ''

    def get_filename(self, folder, prefix):
        now = datetime.now()
        date_time = now.strftime('%Y%m%d_%H%M')
        filename = f'{prefix}{date_time}.dat'
        return os.path.join(folder, filename)

    def start(self, folder, prefix, buffer_size, max_file_size):

        self.folder = folder
        self.max_file_size = max_file_size
        self.file_size_written = 0
        self.prefix = prefix
        self.buffer_size = buffer_size
        if self.create_new_file():
            self.enabled = True
            return self.filename
        return None

    def stop(self):
        if self.fp:
            self.fp.close()


    def truncate(self):
        if self.enabled and self.fp:
            self.fp.close()
            self.current_file=self.filename
        self.create_new_file()
        return self.current_file 



        return False

    def create_new_file(self):
        self.filename = self.get_filename(self.folder, self.prefix)
        try:
            self.fp = open(self.filename, 'a')
            return self.filename
        except Exception as e:
            return None
