import socket
import sys
from io import BytesIO
import msvcrt
import random
import time
import matplotlib.pyplot as plt


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

address = '192.168.1.117'
port = 1002
server_address = (address, port)

def read(register):  
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

def read_burst(register):  
  a = (cmd_read & 0xF0) + ((register >> 4) & 0x0F)
  b = ((register << 4) & 0xF0) + (cmd_read & 0x0F)
  message = [a, b, 0xFF, 0xFF]
  data = [0x00, 0x00, 0x00, 0x00]
  for word in range(burst_length):
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
    for word in range(burst_length):
      value.append( int.from_bytes(data[4+(word*2)], byteorder='big') * 256 + int.from_bytes(data[5+(word*2)], byteorder='big') )
      #print("Word %s = %s" %(word, hex(value[word])))
    return value
  finally:
    s.close()

def read_samples(event, channel):
  address = ((event & 0x1FF) << 13) + ((channel & 0x07) << 10)
  #print("%s" %(hex(address)))
  value = get_sram_burst(address)
  return value


def read_register(register):  
  value = read(register)
  return "register: %s read = %s" %(hex(register), hex(value))  

def status():
  value = read(addr_status)
  msg=["register: %s read = %s" %(hex(addr_status), hex(value))]
  msg=[]
  for bit in range(16):
      msg.append("\t%s: %s" %( status_bits[bit], (((value >> bit) & 1) == 1) ))
  return msg

def decode_temp(readout):
  if (readout & 0x8000):
    decoded = ((0x7FFF - (readout & 0x7FFF) + 1) * 0.0078125) * (-1)
  else:
    decoded = readout * 0.0078125
  return decoded

def get_temperatures():
  t1 = read(0x21)
  t2 = read(0x22)
  tt1 = decode_temp(t1)
  tt2 = decode_temp(t2)
  msg=[]
  msg.append("temperature 0x90: %s = %sC" %(hex(t1), str(tt1)))
  msg.append("temperature 0x92: %s = %sC" %(hex(t2), str(tt2)))
  return msg
def read_all_registers():
  return [read_register(register)  for register in range(0x100)]
    

def read_all_registers_silent():
  for register in range(0x100):
    value = read(register)
    if (value != 0xbaad):
      print("register: %s read = %s" %(hex(register), hex(value)))  

def write(register, value):  
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

def write_register(register, value):  
  write(register, value)
  print("register: %s written = %s" %(hex(register), hex(value)))

def read_sram(address):
  row = (address & 0x7FF)
  column = (address & 0x3FF800) >> 11
  write(addr_row, row)
  write(addr_column, column)
  value = read(addr_sram)
  print("SRAM: %s read = %s" %(hex(address), hex(value)))

def read_sram_burst(address):
  row = (address & 0x7FF)
  column = (address & 0x3FF800) >> 11
  write(addr_row, row)
  write(addr_column, column)
  value = read_burst(addr_sram_burst)

def get_sram_burst(address):
  row = (address & 0x7FF)
  column = (address & 0x3FF800) >> 11
  write(addr_row, row)
  write(addr_column, column)
  value = read_burst(addr_sram_burst)
  return value

def read_sram_one_by_one(address, size):
  row = (address & 0x7FF)
  column = (address & 0x3FF800) >> 11
  write(addr_row, row)
  write(addr_column, column)
  for a in range(size):
    read_sram_inc()

def read_sram_silent(address):
  row = (address & 0x7FF)
  column = (address & 0x3FF800) >> 11
  write(addr_row, row)
  write(addr_column, column)
  value = read(addr_sram)
  return value

def read_sram_inc_silent():
  value = read(addr_sram_inc)
  return value

def read_sram_inc():
  row = read(addr_row)
  column = read(addr_column)
  address = (column << 11) + row
  value = read(addr_sram_inc)
  print("SRAM: %s read = %s" %(hex(address), hex(value)))
  return value

def write_sram(address, value):
  row = (address & 0x7FF)
  column = (address & 0x3FF800) >> 11
  write(addr_row, row)
  write(addr_column, column)
  write(addr_sram, value)
  print("SRAM: %s written = %s" %(hex(address), hex(value)))

def write_sram_silent(address, value):
  row = (address & 0x7FF)
  column = (address & 0x3FF800) >> 11
  write(addr_row, row)
  write(addr_column, column)
  write(addr_sram, value)

def memory_test():
  memory = []
  for a in range(10):
    memory.append(random.randint(0, 0x10000))
    write_sram_silent(a, memory[a])
  read_sram_silent(0)
  for a in range(10):
    value = read_sram_inc_silent()
    if (value != memory[a]):
      print("ERROR! address: %s written: %s read: %s" %(hex(a), hex(memory[a]), hex(value)))
  print("Memory test done")

def memory_dump(address_start, address_stop):
  read_sram_silent(address_start)
  values = []
  start = time.time()
  for a in range(address_start, address_stop):
    values.append(read_sram_inc_silent())
  end = time.time()
  print("SRAM: from %s to %s:" %(hex(address_start), hex(address_stop)))
  for a in range(address_start, address_stop):
    print(values[a])
  print("... in %d seconds" %(end - start))

'''
def plot_event(event):
  plt.figure()
  for channel in range(8):
    y = read_samples(event, channel)
    x = [*range(0,len(y),1)]
    plt.subplot(3,3,channel+1+int(channel/4))
    plt.plot(x, y,'r.')
    plt.title('channel: ' + str(channel))     
  plt.show()
  '''

def list_event(event):
  return [read_samples(event, i) for i in range (8)]

    #print(channel)
    #print(len(y))
    #print(y)
    

def plot_channel(event, channel):
  y = read_samples(event, channel)
  x = [*range(0,len(y),1)]
  plt.figure() 
  plt.plot(x, y, 'r.')
  plt.xlabel('sample') 
  plt.ylabel('value') 
  plt.title('event: ' + str(event) + ' channel: ' + str(channel)) 
  plt.show() 

