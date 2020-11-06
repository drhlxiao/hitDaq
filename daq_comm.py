import socket
import sys
from io import BytesIO
import random
import time
import config
import matplotlib.pyplot as plt

from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QObject

cmd_write = 0xFF
cmd_read  = 0x00

addr_sram       = 0x60
addr_sram_inc   = 0x61
addr_sram_burst = 0x6F
burst_length    = 1024
addr_row        = 0x62
addr_column     = 0x63
addr_status     = 0x02
status_bits = ["spi_master_busy       ",
        "i2c_master_busy       ",
        "i2c_master_timeout    ",
        "any heater on         ",
        "any trigger on        ",
        "tca_ctrl              ",
        "cal_inv               ",
        "trigger drs sequencer ",
        "enable drs sequencer  ",
        "denable from sequencer",
        "dwrite from sequencer ",
        "denable from register ",
        "dwrite from register  ",
        "wsrout                ",
        "srout                 ",
        "plllck                "]


class DaqComm(QObject):
    error_sig= pyqtSignal(str)
    info_sig= pyqtSignal(str)
    warning_sig= pyqtSignal(str)

    def __init__(self):
        super(DaqComm, self).__init__()
        self.address = '10.42.0.130'
        self.port = 1002
        self.server_address = None
        self.s=None
        self.hw_ready=False
    def connect_host(self,address,port):
        self.address=address
        self.port = port
        self.hw_ready=False
        server_address = (address, port)
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect(server_address)
            self.hw_ready=True
            return True
        except Exception as e:
            self.error(str(e))
        return False
    def close_all(self):
        self.s.close()
    def error(self,msg):
        self.error_sig.emit(msg)
    def info(self,msg):
        self.info_sig.emit(msg)
    def warn(self,msg):
        self.warning_sig.emit(msg)

    def connect_signal_slots(self, slots):
        self.error_sig.connect(slots['error'])
        self.info_sig.connect(slots['info'])
        self.warning_sig.connect(slots['warning'])

    def read(self,register):  
        a = (cmd_read & 0xF0) + ((register >> 4) & 0x0F)
        b = ((register << 4) & 0xF0) + (cmd_read & 0x0F)
        message = [a, b, 0xFF, 0xFF, 0xFF, 0xFF]
        try:
            self.s.sendall(bytes(message))
            amount_received = 0
            amount_expected = len(message)
            data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
            while amount_received < amount_expected:
                data[amount_received] = self.s.recv(1)
                amount_received += 1
            value = int.from_bytes(data[4], byteorder='big') * 256 + int.from_bytes(data[5], byteorder='big')
            return value
        except Exception as e:
            self.error(str(e))
        return None

    def read_burst(self, register):  
        a = (cmd_read & 0xF0) + ((register >> 4) & 0x0F)
        b = ((register << 4) & 0xF0) + (cmd_read & 0x0F)
        message = [a, b, 0xFF, 0xFF]
        data = [0x00, 0x00, 0x00, 0x00]
        for word in range(burst_length):
            message.append(0xFF)
            message.append(0xFF)
            data.append(0x00)
            data.append(0x00)
        try:
            self.s.sendall(bytes(message))
            amount_received = 0
            amount_expected = len(message)
            while amount_received < amount_expected:
                data[amount_received] = self.s.recv(1)
                amount_received += 1
            value = []
            for word in range(burst_length):
                value.append( int.from_bytes(data[4+(word*2)], byteorder='big') * 256 + int.from_bytes(data[5+(word*2)], byteorder='big') )
              #print("Word %s = %s" %(word, hex(value[word])))
            return value
        except Exception as e:
            self.error(str(e))
        return None

    def read_samples(self,event, channel):
        address = ((event & 0x1FF) << 13) + ((channel & 0x07) << 10)
        #print("%s" %(hex(address)))
        value = self.get_sram_burst(address)
        return value


    def read_register(self,register):  
        value = self.read(register)
        return value

    def status(self):
        value = self.read(addr_status)
        if value:
            self.info("register: %s read = %s" %(hex(addr_status), hex(value)))
            for bit in range(16):
                self.info(f'\t{status_bits[bit]}:{((value >> bit) & 1) == 1}')
            return
        self.info(f"status for {addr_status}: None")



    def decode_temp(self,readout):
        if (readout & 0x8000):
            decoded = ((0x7FFF - (readout & 0x7FFF) + 1) * 0.0078125) * (-1)
        else:
            decoded = readout * 0.0078125
        return decoded

    def get_temperatures(self):
        t1 = self.read(0x21)
        t2 = self.read(0x22)
        tt1 = self.decode_temp(t1)
        tt2 = self.decode_temp(t2)
        msg=[]
        msg.append("temperature 0x90: %s = %sC" %(hex(t1), str(tt1)))
        msg.append("temperature 0x92: %s = %sC" %(hex(t2), str(tt2)))
        return msg
    def read_all_registers(self):
        return [self.read_register(register)  for register in range(0x100)]
    def read_all_registers_silent(self):
        for register in range(0x100):
            value = self.read(register)
            if (value != 0xbaad):
                self.info("register: %s read = %s" %(hex(register), hex(value)))  

    def write(self,register, value):  
        a = (cmd_write & 0xF0) + ((register >> 4) & 0x0F)
        b = ((register << 4) & 0xF0) + (cmd_write & 0x0F)
        c = (value & 0xFF00) >> 8
        d = (value & 0x00FF)
        message = [a, b, c, d, 0xFF, 0xFF]
        try:
            self.s.sendall(bytes(message))
            amount_received = 0
            amount_expected = len(message)
            data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
            while amount_received < amount_expected:
                data[amount_received] = self.s.recv(1)
                amount_received += 1
        except Exception as e:
            self.error(str(e))

    def write_register(self,register, value):  
        self.write(register, value)
        self.info("register: %s written = %s" %(hex(register), hex(value)))

    def read_sram(self,address):
        row = (address & 0x7FF)
        column = (address & 0x3FF800) >> 11
        self.write(addr_row, row)
        self.write(addr_column, column)
        value = self.read(addr_sram)
        self.info("SRAM: %s read = %s" %(hex(address), hex(value)))

    def read_sram_burst(self,address):
        row = (address & 0x7FF)
        column = (address & 0x3FF800) >> 11
        self.write(addr_row, row)
        self.write(addr_column, column)
        value = self.read_burst(addr_sram_burst)
        return value

    def get_sram_burst(self,address):
        row = (address & 0x7FF)
        column = (address & 0x3FF800) >> 11
        self.write(addr_row, row)
        self.write(addr_column, column)
        value = self.read_burst(addr_sram_burst)
        return value
    def read_sram_one_by_one(self,address, size):
        row = (address & 0x7FF)
        column = (address & 0x3FF800) >> 11
        self.write(addr_row, row)
        self.write(addr_column, column)
        for a in range(size):
            self.read_sram_inc()

    def read_sram_silent(self, address):
        row = (address & 0x7FF)
        column = (address & 0x3FF800) >> 11
        self.write(addr_row, row)
        self.write(addr_column, column)
        value = self.read(addr_sram)
        return value
    def read_sram_inc_silent(self):
        value = self.read(addr_sram_inc)
        return value

    def read_sram_inc(self):
        row = self.read(addr_row)
        column = self.read(addr_column)
        address = (column << 11) + row
        value = self.read(addr_sram_inc)
        self.info("SRAM: %s read = %s" %(hex(address), hex(value)))
        return value

    def write_sram(self,address, value):
        row = (address & 0x7FF)
        column = (address & 0x3FF800) >> 11
        self.write(addr_row, row)
        self.write(addr_column, column)
        self.write(addr_sram, value)
        self.info("SRAM: %s written = %s" %(hex(address), hex(value)))

    def write_sram_silent(self,address, value):
        row = (address & 0x7FF)
        column = (address & 0x3FF800) >> 11
        self.write(addr_row, row)
        self.write(addr_column, column)
        self.write(addr_sram, value)

    def memory_test(self):
        memory = []
        for a in range(10):
            memory.append(random.randint(0, 0x10000))
        self.write_sram_silent(a, memory[a])
        self.read_sram_silent(0)
        for a in range(10):
            value = self.read_sram_inc_silent()
        if (value != memory[a]):
            self.info("ERROR! address: %s written: %s read: %s" %(hex(a), hex(memory[a]), hex(value)))
        self.info("Memory test done")

    def memory_dump(self,address_start, address_stop):
        self.read_sram_silent(address_start)
        values = []
        start = time.time()
        for a in range(address_start, address_stop):
            values.append(self.read_sram_inc_silent())
        end = time.time()
        self.info("SRAM: from %s to %s:" %(hex(address_start), hex(address_stop)))
        for a in range(address_start, address_stop):
            self.info(values[a])
        self.info("... in %d seconds" %(end - start))

    def list_event(self,event):
        return [self.read_samples(event, i) for i in range (8)]

    #self.info(channel)
        #self.info(len(y))
        #self.info(y)


    def plot_channel(self,event, channel):
        y = self.read_samples(event, channel)
        x = [*range(0,len(y),1)]
        plt.figure() 
        plt.plot(x, y, 'r.')
        plt.xlabel('sample') 
        plt.ylabel('value') 
        plt.title('event: ' + str(event) + ' channel: ' + str(channel)) 
        plt.show() 

    def is_connected(self):
        if self.s:
            return True
        return False
    def is_initialized(self):
        return self.hw_ready


    def init_daq(self):
        if not self.is_connected:
            self.error('hw not ready, connect first')
            return False
        sequences=config.config['hw_init_sequences']
        try:
            for seq in sequences:
                self.info(seq[0])
                values=seq[2]
                if seq[3]=='hex':
                    values=[int(x) for x in seq[2]]
                if seq[1] == 'r':
                    res=self.read_register(values[0])
                    if res:
                        msg="register: %s read = %s" %(hex(values[0]), hex(res))  
                        self.info(msg)
                elif seq[1] == 'w':
                    self.write_register(values[0],values[1])
                elif seq[1] == 's':
                    self.status()
            self.hw_ready=True
            return True
        except Exception as e:
            raise Exception
            self.hw_ready=False
            self.error(str(e))
        return False


