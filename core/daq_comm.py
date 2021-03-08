import socket
import sys
from io import BytesIO
import random
import time
from core import config
from core import archive

from PyQt5 import QtWidgets, QtCore, QtGui

cmd_write = 0xFF
cmd_read = 0x00


cmd_write = 0xFF
cmd_read  = 0x00

################################################################################

addr_constant            = 0x00
addr_dummmy              = 0x01
addr_status              = 0x02
addr_triggers            = 0x06
addr_timestamp           = 0x0E
addr_operation           = 0x0F
addr_heaters             = 0x20
addr_temp_90             = 0x21
addr_temp_92             = 0x22
addr_dac_hv1             = 0x30
addr_dac_hv2             = 0x31
addr_dac_hv3             = 0x32
addr_dac_hv4             = 0x33
addr_dac_hv5             = 0x34
addr_dac_hv6             = 0x35
addr_dac_hv7             = 0x36
addr_dac_hv8             = 0x37
addr_dac_tlevel1         = 0x38
addr_dac_tlevel2         = 0x39
addr_dac_tlevel3         = 0x3A
addr_dac_tlevel4         = 0x3B
addr_dac_tlevel5         = 0x3C
addr_dac_tlevel6         = 0x3D
addr_dac_tlevel7         = 0x3E
addr_dac_tlevel8         = 0x3F
addr_dac_bias            = 0x40
addr_dac_va              = 0x41
addr_dac_vb              = 0x42
addr_dac_rofs            = 0x4B
addr_dac_calp            = 0x4C
addr_dac_calm            = 0x4D
addr_calibration         = 0x4E
addr_drs_config          = 0x4F  
addr_last_command        = 0x50
addr_last_data           = 0x51
addr_command_count       = 0x52
addr_sram_data           = 0x60
addr_sram_data_inc       = 0x61
addr_sram_address_row    = 0x62
addr_sram_address_col    = 0x63
addr_sram_demo_data      = 0x6D
addr_sram_burst_length   = 0x6E
addr_sram_burst_data     = 0x6F
addr_fifo                = 0x70
addr_fifo_burst          = 0x71
addr_fifo_burst_length   = 0x72
addr_readout_mode        = 0x80
addr_readout_channels    = 0x81
addr_readout_delay       = 0x82
addr_readout_length      = 0x83
addr_readout_start       = 0x84
addr_counter_pattern_0   = 0xD0
addr_counter_pattern_1   = 0xD1
addr_counter_pattern_2   = 0xD2
addr_counter_pattern_3   = 0xD3
addr_counter_pattern_4   = 0xD4
addr_counter_pattern_5   = 0xD5
addr_counter_pattern_6   = 0xD6
addr_counter_pattern_7   = 0xD7
addr_counter_trigger_0   = 0xD8
addr_counter_trigger_1   = 0xD9
addr_counter_trigger_2   = 0xDA
addr_counter_trigger_3   = 0xDB
addr_counter_trigger_4   = 0xDC
addr_counter_trigger_5   = 0xDD
addr_counter_trigger_6   = 0xDE
addr_counter_trigger_7   = 0xDF
addr_pattern_0           = 0xE0
addr_pattern_1           = 0xE1
addr_pattern_2           = 0xE2
addr_pattern_3           = 0xE3
addr_pattern_4           = 0xE4
addr_pattern_5           = 0xE5
addr_pattern_6           = 0xE6
addr_pattern_7           = 0xE7
addr_debug_1             = 0xF1
addr_debug_2             = 0xF2
addr_debug               = 0xFF

################################################################################

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
               "fifo empty            ",
               "fifo full             ",
               "plllck                "]


def parse_int(x):
    if isinstance(x, str):
        if x=='0x':
            return 0
        if '0x' in x:
            return int(x, 16)
        else:
            return int(x)
    return x


class DaqComm(object):

    def __init__(self):
        super(DaqComm, self).__init__()
        self.address = '10.42.0.130'
        self.port = 1002
        self.server_address = None
        # self.parent=parent
        self.s = None
        self.hw_ready = False
        self.telecommand_counter = 0
        self.telemetry_counter = 0
        self.archive_manager = archive.Archive()

   
    def read_register_burst(self,register, length):
        a = (cmd_read & 0xF0) + ((register >> 4) & 0x0F)
        b = ((register << 4) & 0xF0) + (cmd_read & 0x0F)
        double_len=2*int(length)
        message = [a, b, 0xFF, 0xFF]
        message.extend([0xFF]*double_len)
        data = []
        value = []
        try:
            self.s.sendall(bytes(message))
            data=[ self.s.recv(1) for x in range(double_len+4)]
            value=[ int.from_bytes(data[4+(word*2)], byteorder='big') * 256 
                    + int.from_bytes(data[5+(word*2)], byteorder='big') for word in range(int(length))] 
            return value
        except Exception as e:
            print(str(e))
            return []
    
    def fifo_burst_read(self, length):
        self.write(addr_fifo_burst_length, int(length))
        ret = self.read_register_burst(addr_fifo_burst, length)
        print(ret)
        return ret
        #for word in range(int(length)):
        #    print("Word %03d = 0x%0*X" %(word, 4, ret[word]))


    def fifo_onebyone_read(self):
        word = 0
        ret=[]
        while (((self.read_register(addr_status) >> 13) & 0x01) == 0):
          ret.append(self.read_register(addr_fifo))
          word = word + 1
        return ret





    def connect_host(self, address, port):
        self.address = address
        self.port = port
        self.hw_ready = False
        server_address = (address, port)
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect(server_address)
            self.hw_ready = True
            return True
        except Exception as e:
            self.error(str(e))
        return False

    def close_all(self):
        if self.s:
            self.s.close()

    def read(self, register):
        self.telemetry_counter += 1
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
            value = int.from_bytes(
                data[4], byteorder='big') * 256 + int.from_bytes(data[5], byteorder='big')
            self.archive_manager.append(['read', register, value])
            return value
        except Exception as e:
            self.error(str(e))
        return None

    def read_burst(self, register):
        self.telemetry_counter += 1
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
                value.append(int.from_bytes(
                    data[4+(word*2)], byteorder='big') * 256 + int.from_bytes(data[5+(word*2)], byteorder='big'))
            self.archive_manager.append(['burst_read', register, value])
            #print(value)
            return value
        except Exception as e:
            raise
            self.error(str(e))
        return None


    def read_register(self, register):
        register = parse_int(register)
        #print('reading ', register)
        value = self.read(register)
        #print('result:', value)
        return value

    def decode_status(self, inputs_tuple, value):
        addr_status = inputs_tuple[0]
        if value:
            self.info("register: %s read = %s" %
                      (hex(addr_status), hex(value)))
            for bit in range(16):
                self.info(f'\t{status_bits[bit]}:{((value >> bit) & 1) == 1}')
            return None
        self.info(f"status for {addr_status}: None")
        return None
    def is_fifo_empty(self):
        value = self.read(addr_status)
        if value:
            bit=13
            return ((value >> bit) & 1) == 1
        return None

    def status(self):
        value = self.read(addr_status)
        if value:
            self.info("register: %s read = %s" %
                      (hex(addr_status), hex(value)))
            for bit in range(16):
                self.info(f'\t{status_bits[bit]}:{((value >> bit) & 1) == 1}')
            return None
        self.info(f"status for {addr_status}: None")
        return None

    def decode_temp(self, readout):
        if (readout & 0x8000):
            decoded = ((0x7FFF - (readout & 0x7FFF) + 1) * 0.0078125) * (-1)
        else:
            decoded = readout * 0.0078125
        return decoded
    def _decode_temp(self, inputs,  readout):
        # reg=inputs[0]
        return self.decode_temp(readout)

    def get_temperatures(self):
        t1 = self.read(0x21)
        t2 = self.read(0x22)
        tt1 = self.decode_temp(t1)
        tt2 = self.decode_temp(t2)
        msg = []
        msg.append("temperature 0x90: %s = %sC" % (hex(t1), str(tt1)))
        msg.append("temperature 0x92: %s = %sC" % (hex(t2), str(tt2)))
        return msg



    def decode_readout_mode(self):
        ret       = self.read_register(addr_readout_mode)
        channels  = self.read_register(addr_readout_channels)
        delay     = self.read_register(addr_readout_delay)
        length    = self.read_register(addr_readout_length)
        start     = read_register(addr_readout_start)
        test = (ret >> 2) & 0x01
        mode = (ret & 0x03)
        self.info("Readout mode: %s" %(hex(ret)))

        if (mode == 1):
            self.info("\tRegion of Interest readout")
        elif (mode == 2):
            self.info("\tSmart readout")
        elif (mode == 3):
            self.info("\tFull readout")
        else:
            self.info("\tUnsupported readout")

        if (test == 1):
            self.info("\tTest on")
        else:
            self.info("\tTest off")

        self.info("Channels register: %s" %(channels))
        self.info("\t%s %s %s %s %s %s %s %s %s" %(((channels >> 8) & 0x01), ((channels >> 7) & 0x01), 
            ((channels >> 6) & 0x01), ((channels >> 5) & 0x01), ((channels >> 4) & 0x01), 
            ((channels >> 3) & 0x01), ((channels >> 2) & 0x01), 
            ((channels >> 1) & 0x01), ((channels >> 0) & 0x01)))
        self.info("Delay register:    %s" %(delay))
        self.info("Length register:   %s" %(length))
        self.info("Start register:    %s" %(start))


    def write(self, register, value):
        self.telecommand_counter += 1
        a = (cmd_write & 0xF0) + ((register >> 4) & 0x0F)
        b = ((register << 4) & 0xF0) + (cmd_write & 0x0F)
        c = (value & 0xFF00) >> 8
        d = (value & 0x00FF)
        message = [a, b, c, d, 0xFF, 0xFF]
        self.archive_manager.append(['write', register, value])
        try:
            self.s.sendall(bytes(message))
            amount_received = 0
            amount_expected = len(message)
            data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
            while amount_received < amount_expected:
                data[amount_received] = self.s.recv(1)
                amount_received += 1
            return True
        except Exception as e:
            self.error(str(e))
        return False

    def write_register(self, register, value, desc=''):
        register = parse_int(register)
        value = parse_int(value)
        msg = ''
        if desc:
            msg = (" {:50} (Register: {}, value: {} [{}])".format(
                desc, hex(register), value, hex(value)))
        else:
            msg = ("Writing register: {}, value: {}".format(
                hex(register), hex(value)))

        loc, item = self.info(msg)
        status = self.write(register, value)
        if loc == 'log':
            color = 'green' if status else 'red'
            item.setForeground(QtGui.QColor(color))

    def read_sram(self, address):
        row = (address & 0x7FF)
        column = (address & 0x3FF800) >> 11
        self.write(addr_sram_address_row, row)
        self.write(addr_sram_address_col, column)
        value = self.read_register(addr_sram_data)
        self.info("SRAM: %s read = %s" % (hex(address), hex(value)))
        return value


    def read_sram_burst(self, address,length):
        row = (address & 0x7FF)
        column = (address & 0x3FF800) >> 11
        self.write_register(addr_sram_address_row, row)
        self.write_register(addr_sram_address_col, column)
        self.write_register(addr_sram_burst_length, int(length))
        ret = self.read_register_burst(addr_sram_burst_data, int(length))
        return ret



    def read_sram_inc(self):
        row = self.read_register(addr_sram_address_row)
        column = self.read_register(addr_sram_address_col)
        address = (column << 11) + row
        value = self.read_register(addr_sram_data_inc)
        self.info("SRAM: %s read = %s" % (hex(address), hex(value)))
        return (address, value)

    def write_sram(self, address, value):
        row = (address & 0x7FF)
        column = (address & 0x3FF800) >> 11
        self.write_register(addr_sram_address_row, row)
        self.write_register(addr_sram_address_col, column)
        self.write_register(addr_sram_data, value)






    def is_connected(self):
        if self.s:
            return True
        return False

    def is_initialized(self):
        return self.hw_ready
