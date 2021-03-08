################################################################################
################################################################################

import socket
import sys
from io import BytesIO
import random
import time
import matplotlib.pyplot as plt

################################################################################

address = '10.42.0.136'
port = 1002
server_address = (address, port)
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

################################################################################
################################################################################

def read_register(register):  
  a = (cmd_read & 0xF0) + ((register >> 4) & 0x0F)
  b = ((register << 4) & 0xF0) + (cmd_read & 0x0F)
  message = [a, b, 0xFF, 0xFF, 0xFF, 0xFF]
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(server_address)
  try:
    s.sendall(bytes(message))
    amount_received = 0
    amount_expected = len(message)
    data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    while amount_received < amount_expected:
      data[amount_received] = s.recv(1)
      amount_received += 1
    value = int.from_bytes(data[4], byteorder='big') * 256 + int.from_bytes(data[5], byteorder='big')
    return value
  finally:
    s.close()  

################################################################################

def read_register_burst(register, length):  
  a = (cmd_read & 0xF0) + ((register >> 4) & 0x0F)
  b = ((register << 4) & 0xF0) + (cmd_read & 0x0F)
  message = [a, b, 0xFF, 0xFF]
  data = [0x00, 0x00, 0x00, 0x00]
  for word in range(int(length)):
    message.append(0xFF)
    message.append(0xFF)
    data.append(0x00)
    data.append(0x00)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(server_address)
  try:
    s.sendall(bytes(message))
    amount_received = 0
    amount_expected = len(message)
    while amount_received < amount_expected:
      data[amount_received] = s.recv(1)
      amount_received += 1
    value = []
    for word in range(int(length)):
      value.append( int.from_bytes(data[4+(word*2)], byteorder='big') * 256 + int.from_bytes(data[5+(word*2)], byteorder='big') )
    return value
  finally:
    s.close()

################################################################################

def write_register(register, value):  
  a = (cmd_write & 0xF0) + ((register >> 4) & 0x0F)
  b = ((register << 4) & 0xF0) + (cmd_write & 0x0F)
  c = (value & 0xFF00) >> 8
  d = (value & 0x00FF)
  message = [a, b, c, d, 0xFF, 0xFF]
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(server_address)
  try:
    s.sendall(bytes(message))
    amount_received = 0
    amount_expected = len(message)
    data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    while amount_received < amount_expected:
      data[amount_received] = s.recv(1)
      amount_received += 1
  finally:
    s.close()

################################################################################
################################################################################

def decode_status():
  value = read_register(addr_status)
  print("Status: %s" %(hex(value)))
  for bit in range(16):
    print("\t%s %s" %( status_bits[bit], (((value >> bit) & 1) == 1) ))

################################################################################

def decode_readout_mode():
  ret       = read_register(addr_readout_mode)
  channels  = read_register(addr_readout_channels)
  delay     = read_register(addr_readout_delay)
  length    = read_register(addr_readout_length)
  start     = read_register(addr_readout_start)

  test = (ret >> 2) & 0x01
  mode = (ret & 0x03)

  print("Readout mode: %s" %(hex(ret)))

  if (mode == 1):
    print("\tRegion of Interest readout")
  elif (mode == 2):
    print("\tSmart readout")
  elif (mode == 3):
    print("\tFull readout")
  else:
    print("\tUnsupported readout")

  if (test == 1):
    print("\tTest on")
  else:
    print("\tTest off")

  print("Channels register: %s" %(channels))
  print("\t%s %s %s %s %s %s %s %s %s" %(((channels >> 8) & 0x01), ((channels >> 7) & 0x01), ((channels >> 6) & 0x01), ((channels >> 5) & 0x01), ((channels >> 4) & 0x01), ((channels >> 3) & 0x01), ((channels >> 2) & 0x01), ((channels >> 1) & 0x01), ((channels >> 0) & 0x01)))
  print("Delay register:    %s" %(delay))
  print("Length register:   %s" %(length))
  print("Start register:    %s" %(start))

################################################################################

def calculate_temp(readout):
  if (readout & 0x8000):
    decoded = ((0x7FFF - (readout & 0x7FFF) + 1) * 0.0078125) * (-1)
  else:
    decoded = readout * 0.0078125
  return decoded

################################################################################

def decode_temperatures():
  t1 = read_register(0x21)
  t2 = read_register(0x22)
  tt1 = calculate_temp(t1)
  tt2 = calculate_temp(t2)
  print("temperature 0x90: %s = %sC" %(hex(t1), str(tt1)))
  print("temperature 0x92: %s = %sC" %(hex(t2), str(tt2)))

################################################################################

def decode_debug():
  value = read_register(addr_debug_1)
  print("debug register 1 = %s" %(hex(value)))
  value = read_register(addr_debug_2)
  print("debug register 2 = %s" %(hex(value)))
  value = read_register(addr_debug)
  print("debug register   = %s" %(hex(value)))
  print("\t15.'0'                  = %d" %( (value >> 15) & 0x01))
  print("\t14.'0'                  = %d" %( (value >> 14) & 0x01))
  print("\t13.'0'                  = %d" %( (value >> 13) & 0x01))
  print("\t12.'0'                  = %d" %( (value >> 12) & 0x01))
  print("\t11.'0'                  = %d" %( (value >> 11) & 0x01))
  print("\t10.'0'                  = %d" %( (value >> 10) & 0x01))
  print("\t 9.'0'                  = %d" %( (value >>  9) & 0x01))
  print("\t 8.'0'                  = %d" %( (value >>  8) & 0x01))
  print("\t 7.'0'                  = %d" %( (value >>  7) & 0x01))
  print("\t 6.reg_operation(9)     = %d" %( (value >>  6) & 0x01))
  print("\t 5.prev_reg_operation_9 = %d" %( (value >>  5) & 0x01))
  print("\t 4.reg_operation_9      = %d" %( (value >>  4) & 0x01))
  print("\t 3.'0'                  = %d" %( (value >>  3) & 0x01))
  print("\t 2.drs_trigger_command  = %d" %( (value >>  2) & 0x01))
  print("\t 1.drs_trigger          = %d" %( (value >>  1) & 0x01))
  print("\t 0.drs_trigger_pattern  = %d" %( (value >>  0) & 0x01))

################################################################################

def fifo_burst_read(length):
  write_register(addr_fifo_burst_length, int(length))
  ret = read_register_burst(addr_fifo_burst, length)
  for word in range(int(length)):
    print("Word %03d = 0x%0*X" %(word, 4, ret[word]))

################################################################################

def fifo_onebyone_read():
  word = 0
  while (((read_register(addr_status) >> 13) & 0x01) == 0):
    print("Word %03d = 0x%0*X" %(word, 4, read_register(addr_fifo)))
    word = word + 1

################################################################################

def write_sram(address, value):
  row = (address & 0x7FF)
  column = (address & 0x3FF800) >> 11
  write_register(addr_sram_address_row, row)
  write_register(addr_sram_address_col, column)
  write_register(addr_sram_data, value)

################################################################################

def read_sram(address):
  row = (address & 0x7FF)
  column = (address & 0x3FF800) >> 11
  write_register(addr_sram_address_row, row)
  write_register(addr_sram_address_col, column)
  value = read_register(addr_sram_data)
  return value

################################################################################

def read_sram_inc():
  row = read_register(addr_sram_address_row)
  column = read_register(addr_sram_address_col)
  address = (column << 11) + row
  value = read_register(addr_sram_data_inc)
  return (address, value)

################################################################################

def read_sram_burst(address, length):
  row = (address & 0x7FF)
  column = (address & 0x3FF800) >> 11
  write_register(addr_sram_address_row, row)
  write_register(addr_sram_address_col, column)
  write_register(addr_sram_burst_length, int(length))
  ret = read_register_burst(addr_sram_burst_data, int(length))
  for word in range(int(length)):
    print("Word %07d = 0x%0*X" %(word+address, 4, ret[word]))

################################################################################
################################################################################

def usage():
  print("Usage:")
  print("\t g  0x<address>             - read (get) the register")
  print("\t s  0x<address> 0x<value>   - write (set) to the register")
  print("\t p                          - read all registers")
  print("\t ?                          - read and decode the status register")
  print("\t m                          - read and decode the readout mode registers")
  print("\t t                          - read and decode temperature registers")
  print("\t d                          - read and decode debug register")  
  print("\t f                          - read one word from FIFO")
  print("\t fb <length>                - FIFO burst read")
  print("\t f1                         - FIFO one-by-one read till empty")
  print("\t w  0x<address> 0x<value>   - write to the SRAM memory")
  print("\t r  0x<address>             - read from the SRAM memory")
  print("\t i                          - incremental read from the SRAM memory")
  print("\t b  0x<address> <length>    - SRAM memory burst read")
  quit()

################################################################################

def main():

  if len(sys.argv) >= 2:

    if (sys.argv[1] == 'g') or (sys.argv[1] == 'G'):
      if len(sys.argv) == 3:
        print("register: %s read = 0x%0*X" %(sys.argv[2], 4, read_register(int(sys.argv[2], base=16))))  
      else:
        usage()

    elif (sys.argv[1] == 's') or (sys.argv[1] == 'S'):
      if len(sys.argv) == 4:
        write_register( int(sys.argv[2], base=16), int(sys.argv[3], base=16) )
        print("register: %s written = %s" %(sys.argv[2], sys.argv[3]))  
      else:
        usage()

    elif (sys.argv[1] == 'p') or (sys.argv[1] == 'P'):
      if len(sys.argv) == 2:
        for register in range(0x100):
          if ((register != addr_sram_burst_data) and (register != addr_fifo_burst)):
            ret = read_register(register)
            if (ret != 0xbaad):
              print("register: %s read = 0x%0*X" %(hex(register), 4, ret))
      else:
        usage()

    elif (sys.argv[1] == '?'):
      if len(sys.argv) == 2:
        decode_status()
      else:
        usage()

    elif (sys.argv[1] == 'm') or (sys.argv[1] == 'M'):
      if len(sys.argv) == 2:
        decode_readout_mode()
      else:
        usage()

    elif (sys.argv[1] == 't') or (sys.argv[1] == 'T'):
      if len(sys.argv) == 2:
        decode_temperatures()
      else:
        usage()
    
    elif (sys.argv[1] == 'd') or (sys.argv[1] == 'D'):
      if len(sys.argv) == 2:
        decode_debug()
      else:
        usage()

    elif (sys.argv[1] == 'f') or (sys.argv[1] == 'F'):
      if len(sys.argv) == 2:
        ret = read_register(addr_fifo)
        print("FIFO read = 0x%0*X" %(4, ret))
      else:
        usage()

    elif (sys.argv[1] == 'fb') or (sys.argv[1] == 'FB'):
      if len(sys.argv) == 3:
        fifo_burst_read(sys.argv[2])
      else:
        usage()

    elif (sys.argv[1] == 'f1') or (sys.argv[1] == 'F1'):
      if len(sys.argv) == 2:
        fifo_onebyone_read()
      else:
        usage()
    
    elif (sys.argv[1] == 'w') or (sys.argv[1] == 'W'):
      if len(sys.argv) == 4:
        write_sram( int(sys.argv[2], base=16), int(sys.argv[3], base=16) )
        print("SRAM: %s written = %s" %(sys.argv[2], sys.argv[3]))
      else:
        usage()

    elif (sys.argv[1] == 'r') or (sys.argv[1] == 'R'):
      if len(sys.argv) == 3:
        ret = read_sram(int(sys.argv[2], base=16))
        print("SRAM: %s read = 0x%0*X" %(sys.argv[2], 4, int(ret)))
      else:
        usage()
    
    elif (sys.argv[1] == 'i') or (sys.argv[1] == 'I'):
      if len(sys.argv) == 2:
        (address, ret) = read_sram_inc()
        print("SRAM: 0x%0*X read inc = 0x%0*X" %(6, address, 4, ret))
      else:
        usage()

    elif (sys.argv[1] == 'b') or (sys.argv[1] == 'B'):
      if len(sys.argv) == 4:
        read_sram_burst( int(sys.argv[2], base=16), sys.argv[3] )
      else:
        usage()

    else:
      usage()
  else:
    usage()

################################################################################

if __name__== "__main__":
  main()

################################################################################=
