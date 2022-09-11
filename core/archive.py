
import os
from datetime import datetime


class Archive(object):

    def __init__(self):
        self.buffer = []
        self.filename = 'run_1.dat'
        self.fp = None
        self.enabled = False
        self.log_file=None
        self.log_filename=None
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
        if self.log_file:
            self.log_file.close()
        self.stop()
    
    def write_log(self, line:str):
        if self.log_file:
            line= f'[{datetime.now().isoformat()}] {line}\n'
            self.log_file.write(line)
        

    def create_log_file(self):
        now = datetime.now()
        date_time = now.strftime('%Y%m%d_%H%M')
        filename = f'daq_{date_time}.log'
        self.log_filename=os.path.join(self.folder, filename)
        self.log_file=open(self.log_filename, 'w')

    def dump(self, force_dump=False, create_new=True):
        if not self.fp:
            return
        if force_dump:
            if len(self.buffer) == 0:
                self.fp.close()
                return
        for item in self.buffer:
            stream = item[0]+','
            if isinstance(item[1], list):
                stream += ','.join([str(x) for x in item[1]])
            else:
                stream += str(item[1])
            self.file_size_written += len(stream)
            self.fp.write(stream)
            self.fp.write('\n')
        self.buffer = []
        self.current_buffer_size = 0
        if self.file_size_written > self.max_file_size or force_dump:
            self.fp.close()

            self.fp = None
            if create_new:
                self.create_new_file()

    def append(self, data):
        if self.enabled and self.fp:
            now = datetime.now().isoformat()
            item = (now, data)
            self.buffer.append(item)
            self.current_buffer_size += 1
            if self.current_buffer_size > self.buffer_size:
                self.dump()

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
        self.current_buffer_size = 0
        self.buffer_size = buffer_size
        if self.create_new_file():
            self.enabled = True
            return self.filename
        return None

    def stop(self):
        self.dump(force_dump=True, create_new=False)
        self.current_buffer_size = 0
        self.enabled = False
        self.fp = None

    def truncate(self):
        if self.enabled and self.fp and self.current_buffer_size > 0:
            self.dump(force_dump=True, create_new=True)
            self.current_buffer_size = 0
            return self.filename

        return False

    def create_new_file(self):
        self.filename = self.get_filename(self.folder, self.prefix)
        try:
            self.fp = open(self.filename, 'w')
            self.file_size_written = 0
            return True
        except Exception as e:
            return False
