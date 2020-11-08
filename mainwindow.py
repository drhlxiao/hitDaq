#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import sys
import pickle
import time
import gzip
import binascii
import struct
import pprint
import socket
import signal
import math
import webbrowser
from functools import partial
from datetime import datetime
import numpy as np
from functools import partial

from PyQt5 import  QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QObject, QRunnable, QThreadPool
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtChart  import QBarSeries, QBarSet, QScatterSeries
import window
import daq_comm 

import config


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress 

    '''
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(object)
    #progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread
    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()    


    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        try:
            result = self.fn(*self.args, **self.kwargs)
            if result:
                self.signals.result.emit(result)  # Return the result of the processing
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()  # Done


class Ui(window.Ui_MainWindow, daq_comm.DaqComm):
    def __init__(self, MainWindow):
        super(Ui, self).setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.current_folder='.'
        self.dynamic_layouts=[]
        self.dynamic_widgets={}
        self.button_actions={}
        self.is_connected=False
        button_connections={
                self.connectBtn: self.ui_connect_host,
                #self.selectFolderBtn: self.select_folder,
                #self.initBtn:self.init_board,
                #self.readStatBtn:self.read_status,
                #self.lastCmdBtn:self.last_command,
                self.registerReadButton: self._register_read,
                self.registerWriteButton: self._register_write,
                self.hkSingleReadBtn:self.single_read,
                self.hkStartBtn: self.hk_acq_start,
                self.sciStartDRSBtn:self.sci_acq_start,
                self.sciStopDRSBtn:self.sci_acq_stop,
                self.sciTrigDRSBtn:self.sci_single_trigger,
                self.sciSingReadBtn:self.sci_single_read,
                #self.calStartBtn:self.calibration_start,
                #self.calStopBtn:self.calibration_stop,
                #self.tempReadBtn:self.read_temperature
                }
        for btn, fun in button_connections.items():
            btn.clicked.connect(fun)

        self.load_register_read_buttons()
        self.load_widgets()


        #self=daq_comm.DaqComm(self)

        self.set_button_status(1, False)
        self.threadpool = QThreadPool()
    def _register_read(self):
        add=self.registerAddressInput.text()
        address=0
        name=self.registerNameLabel.text()

        try:
            if '0x' in add:
                address=int(add,16)
            else:
                address=int(add)
        except Exception as e:
            self.error('Invalid parameters')
            return

        loc, item=self.info(f'Reading register {name} (addr {address})',color='darkYello')
        value=self.read_register(address)
        if value is not None:
            self.info(f'{name} raw value {value}',color='darkCyan')

    def _register_write(self):
        add=self.registerAddressInput.text()
        val=self.registerValueInput.text()
        address=0
        value=0
        name=self.registerNameLabel.text()


        try:
            if '0x' in add:
                address=int(add,16)
            else:
                address=int(add)
            if '0x' in val:
                value=int(val,16)
            else:
                value=int(val)
            
        except Exception as e:
            self.error('Invalid parameters')
            return


        value=self.write_register(address, value, 'Writing '+name)



    
    def set_button_status(self, level, status):
        button_groups={
                0: [],
                1: [self.hkSingleReadBtn, self.hkStartBtn, self.sciSingReadBtn, 
                    self.sciStartDRSBtn, self.sciStopDRSBtn,
                    self.sciTrigDRSBtn, self.calStopBtn, self.calStartBtn]}
        if level>=0:
            for btn in button_groups[0]:
                btn.setEnabled(status)
            for dynamic_btn in self.dynamic_widgets.values():
                dynamic_btn.setEnabled(status)
        if level>=1:
            for btn in button_groups[1]:
                btn.setEnabled(status)



    def async_run(self, func, *args, **kwargs):
        try:
            worker = Worker(func, *args, **kwargs) 
            worker.signals.result.connect(self.handle_result)
            worker.signals.finished.connect(self.handle_finished)
            worker.signals.error.connect(self.error)
            self.threadpool.start(worker)
        except Exception as e:
            self.error(str(e))

    def load_widgets(self):
        self.create_groups('basicOperationGroup')
        self.create_groups('readoutsGroup')
        self.create_groups('readRegisterGroup')
        #self.create_groups('writeRegisterGroup')
        #self.create_groups('readWriteRegisterGroup')


    def create_groups(self, group_name):
        container=config.commands[group_name]['container']
        print('registering',group_name)
        group=self.MainWindow.findChild(QtWidgets.QWidget,container)
        if not group:
            self.error('Can not find container {}'.format(container))
            return
        grid= QtWidgets.QGridLayout(group)
        self.dynamic_layouts.append(grid)
        commands=config.commands[group_name]['sequences']
        row_cols=config.commands[group_name]['grid_columns']
        rowspan=1
        colspan=1
        row=0
        col=0
        for item in commands:
            with_inputs=False
            layout=item.get('layout','inline')
            inputs=item.get('inputs',None)
            
            if inputs:
                if layout=='row':
                    row+=1
                    col=0
                label= QtWidgets.QLabel(group)
                label.setText(item['label'])
                grid.addWidget(label, row, col, rowspan, 1)
                if layout=='row':
                    row+=1
                    col=0
                else:
                    col+=1
                    if col>=colspan:
                        col=1

                for sub_item in inputs:
                    with_inputs=True

                    edit= QtWidgets.QSpinBox(group)
                    edit.setObjectName(sub_item['name'])
                    if 'tooltip' in sub_item:
                        edit.setToolTip(sub_item['tooltip'])
                        edit.setStatusTip(sub_item['tooltip'])
                    if 'max' in sub_item:
                        edit.setMaximum(sub_item['max'])
                    if 'min' in sub_item:
                        edit.setMinimum(sub_item['min'])
                    if 'default' in sub_item:
                        edit.setValue(sub_item['default'])
                    self.dynamic_widgets[sub_item['name']]=edit
                    colspan=sub_item.get('colspan',1)
                    print(sub_item['name'], row, col, rowspan, colspan)
                    grid.addWidget(edit, row, col, rowspan, colspan)

                    col+=colspan
                    if col>=row_cols:
                        row+=1
                        col=0

            colspan=1
            btn= QtWidgets.QPushButton(group)
            btn_name=item['name']
            btn_title=item['button_title']
            btn.setObjectName(btn_name)
            btn.setText(btn_title)
            tooltip=item.get('tooltip',btn_title)
            btn.setToolTip(tooltip)
            btn.setStatusTip(tooltip)
            self.dynamic_widgets[btn_name]=btn
            btn.clicked.connect(
                    partial(self.execute_sequence, item))
            grid.addWidget(btn, row, col, rowspan, colspan)

            if layout=='row':
                row+=1
                col=0
            else:
                col+=1
                if col>=row_cols:
                    row+=1
                    col=0
            

    def _sequence_read(self, seq, args):
        loc, item=self.info(seq[2],color='darkYello')
        value=self.read_register(seq[1][0])
        if value is not None:
            self.info(f'Result raw value: {value}',color='darkCyan')
            if len(seq[0])>1:
                print('calling back')
                callback= getattr(self, seq[0][1])
                print(callback)
                print(seq[1], value)
                result=callback(seq[1], value)
                if result:
                    self.info(f'Eng. value: {result}',color='darkCyan')



    def _sequence_write(self, seq, args):
        value=0
        print('write:')
        print(seq)
        address, origin_value=seq[1]
        #args=seq['args']
        if isinstance(origin_value, str) and origin_value in args:
            value=args[origin_value]
        elif isinstance(origin_value, int):
            value=origin_value
        desc=''
        try:
            desc=seq[2]
            placeholder='{'+str(origin_value)+'}'
            if placeholder in desc:
                desc=desc.replace(placeholder,str(value))
        except Exception as e:
            self.error(str(e))
        self.write_register(address, value, desc)
    def _burst_read(self,seq, args):
        reg=seq[1][0]
        self.info('Burst read ... ')
        values=self.read_burst(reg)  
        if not values:
            self.info('Result is None')
            return None

        self.info(f'Results (n={len(values)}):')
        result='['
        if values:
            for i, val in enumerate(values):
                result+=f'{val},'
                if i%8==0 and i>0:
                    self.info('{:50}'.format(result), timestamp=False, color='blue')
                    result=''
            if result:
                self.info('{:50}]'.format(result), timestamp=False, color='blue')
        return None


    def execute_sequence(self, command, args):
        sequence=command['sequence']
        thread_lock=command.get('thread_lock', False)

        args={}
        try:
            for item in command['inputs']:
                if item['type'] == 'int':
                    args[item['name']]=self.dynamic_widgets[item['name']].value()
                else:
                    args[item['name']]=self.dynamic_widgets[item['name']].text()

        except Exception as e:
            pass
        def _excecute_command():
            if thread_lock:
                try:
                    self.dynamic_widgets[command['name']].setEnabled(False)
                except:
                    pass
            for seq in sequence:
                func_name=seq[0][0]
                print('function name:',func_name)
                func= getattr(self, func_name)
                if func:
                    result=func(seq, args=args)
            try:
                self.dynamic_widgets[command['name']].setEnabled(True)
            except:
                pass

        _excecute_command()

        #self.async_run(_excecute_command)
            
            
    def load_register_read_buttons(self):
        self.registerGridLayout= QtWidgets.QGridLayout(self.registerListGroup)
        register_buttons=config.registers
        index=0
        row_cols=6
        rowspan=1
        colspan=1
        for item in register_buttons:
            if 'write' not in item['operation']:
                continue
            btn= QtWidgets.QPushButton(self.registerListGroup)
            btn.setObjectName(item['name'])
            btn.setText(item['name'])
            btn.setToolTip(f"{item['name']}, address: {item['address']}")
            self.dynamic_widgets[item['name']]=btn
            row=index//row_cols
            col=index%row_cols
            
            btn.clicked.connect(
                partial(self.set_current_register, item))

            self.registerGridLayout.addWidget(btn, row, col, rowspan, colspan)
            index+=1
    def set_current_register(self, item):
        address=item['address']
        default=item['default']
        operation=item['operation']
        self.registerAddressInput.setText(address)
        self.registerNameLabel.setText(item['name'])
        if 'write' in operation:
            self.registerValueInput.setText(default)
        self.registerReadButton.setEnabled('read' in operation)
        self.registerWriteButton.setEnabled('write' in operation)


            


    def handle_finished(self):
        pass
    def handle_result(self, data):
        if isinstance(data,dict):
            if 'error'  in data:
                self.error(data['error'])
                return
            if 'info'  in data:
                self.info(data['info'])
                return
            if 'warning'  in data:
                self.info(data['warning'])
                return
        self.info(str(data))




    def error(self,msg, where=1):
        return self.show_message(msg,where, 'red')
    def info(self,msg,where=1, timestamp=True, color=''):
        return self.show_message(msg,where,color, timestamp)
    def warning(self,msg,where=1):
        return self.show_message(msg,where,'yellow')

    def show_message(self, msg, where=0, color='darkGray', timestamp=True):
        if where != 1:
            self.statusbar.showMessage(msg)
            return 'status', self.statusbar
        if where != 0:
            if timestamp:
                msg=f'[{datetime.now().isoformat()}] {msg}'
            item = QtWidgets.QListWidgetItem(msg)
            item.setForeground(QtGui.QColor(color))
            self.listWidget.addItem(item)
            self.listWidget.scrollToBottom()
            return 'log',item

        
    def close(self):
        self.MainWindow.close()
    def style(self):
        return self.MainWindow.style()
    def read_temperature(self):
        def _read_temperature():
            res=self.get_temperatures()
            for msg in res: 
                self.info(msg)
        self.async_run(_read_temperature)

    def ui_connect_host(self):
        def _connect_host():
            if  not self.is_connected:
                address=self.ipAddressInput.text()
                port=int(self.portInput.text())
                self.info(f'Connecting host {address} port {port}...')

                if self.connect_host(address,port):
                    self.is_connected=True
                    self.info('Connected.')
                    self.connectBtn.setText('Disconnect')
                    self.portInput.setEnabled(False)
                    self.ipAddressInput.setEnabled(False)
                    self.connectBtn.setStyleSheet("background-color:green; color: white;")
                    self.set_button_status(0, True)
                else:
                    self.error('Connection failed!')
                return
            self.close_all()
            self.info('Disconnected!')
            self.connectBtn.setText('Connect')
            self.portInput.setEnabled(True)
            self.ipAddressInput.setEnabled(True)
            self.is_connected=False
            self.connectBtn.setStyleSheet("")
            self.set_button_status(1,False)
        self.async_run(_connect_host)
        


    def select_folder(self):
        self.current_folder= str(QtWidgets.QFileDialog.getExistingDirectory())
        self.folderLabel.setText(self.current_folder)



    #def read_status(self):
    #    self.info('Reading ...', 0)
    #    self.async_run(self.status)

    def last_command(self):
        def _last_command():
            reg=0x52
            res=self.read_register(reg)
            if res:
                msg="register: %s read = %s" %(hex(reg), hex(res))  
                self.info(msg)
            else:
                self.info('Return value is None')
        self.async_run(_last_command)

    def single_read(self):
        self.info('Read single event...', 0)
        pass
    def hk_acq_start(self):
        self.info('Starting hk read...', 0)
        pass
    def sci_acq_start(self):
        self.info('Acq starting...', 0)
        pass
    def sci_acq_stop(self):
        self.info('Stopping acquisition...', 0)
        pass
    def sci_single_trigger(self):
        self.info('single ...', 0)
        pass
    def sci_single_read(self):
        self.info('single read ...', 0)
        pass
    def calibration_start(self):
        self.info('Starting calibration...', 0)
        pass
    def calibration_stop(self):
        self.info('Stopping calibration...', 0)
        pass
    def register_read(self, reg):
        def read_reg(reg_add):
            self.info(f'Reading  {hex(reg)} ...')
            result=self.read_register(reg_add)
            self.info(f'Register {hex(reg)} value: {result}')
        self.async_run(read_reg, reg)



