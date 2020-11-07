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


class Ui(window.Ui_MainWindow):
    def __init__(self, MainWindow):
        super(Ui, self).setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.current_folder='.'
        self.dynamic_layouts=[]
        self.is_connected=False
        button_connections={
                self.connectBtn: self.connect_host,
                #self.selectFolderBtn: self.select_folder,
                #self.initBtn:self.init_board,
                #self.readStatBtn:self.read_status,
                #self.lastCmdBtn:self.last_command,
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
        self.create_commands()


        self.comm=daq_comm.DaqComm(self)

        self.set_button_status(1, False)
        self.threadpool = QThreadPool()
    
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
        worker = Worker(func, *args, **kwargs) 
        worker.signals.result.connect(self.handle_result)
        worker.signals.finished.connect(self.handle_finished)
        worker.signals.error.connect(self.error)
        self.threadpool.start(worker)

    def create_commands(self):
        self.add_command_to_group('basicOperationGroup', row_cols=5)
        self.add_command_to_group('readoutsGroup', row_cols=4)
    def add_command_to_group(self, group_name, row_cols):
        group=self.MainWindow.findChild(QtWidgets.QGroupBox,group_name)
        grid= QtWidgets.QGridLayout(group)
        self.dynamic_layouts.append(grid)
        commands=config.commands[group_name]
        rowspan=1
        colspan=1
        row=0
        col=0
        for item in commands:
            with_inputs=False
            if 'inputs' in item:
                if item['inputs']:
                    print('here')
                    inputs=item['inputs']
                    row+=1
                    col=0
                    label= QtWidgets.QLabel(group)
                    label.setText(item['label'])
                    grid.addWidget(label, row, col, rowspan, 1)
                    row+=1
                    col=0

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
                            print(sub_item['default'])

                        #row=index//row_cols
                        #col=index%row_cols

                        print(row,col)
                        self.dynamic_widgets[sub_item['name']]=edit
                        try:
                            colspan=sub_item['colspan']
                        except KeyError:
                            colspan=1
                        grid.addWidget(edit, row, col, rowspan, colspan)
                        col+=colspan
                        if col==row_cols:
                            row+=1
                            col=0

            colspan=1
            btn= QtWidgets.QPushButton(group)
            btn_name=item['name']
            btn_title=item['button_title']
            btn.setObjectName(btn_name)
            btn.setText(btn_title)
            tooltip=btn_title
            if 'tooltip' in item:
                tooltip=item['tooltip']
            btn.setToolTip(tooltip)
            btn.setStatusTip(tooltip)
            self.dynamic_widgets[btn_name]=btn
            btn.clicked.connect(
                    partial(self.execute_sequence, item))
            grid.addWidget(btn, row, col, rowspan, colspan)
            if with_inputs:
                row+=1
                col=0
            else:
                col+=1
                if col==row_cols:
                    row+=1
                    col=0
            


    def execute_sequence(self, command):
        sequence=command['sequence']
        inputs=[]
        args={}
        if command['inputs']:
            for item in command['inputs']:
                args[item['name']]=self.dynamic_widgets[item['name']].value()
        print(args)
        for seq in sequence:
            print(seq)
        
        

    def load_register_read_buttons(self):
        self.registerGridLayout= QtWidgets.QGridLayout(self.tabRegisters)
        self.dynamic_widgets={}
        self.button_actions={}
        register_buttons=config.buttons['registers']
        index=0
        row_cols=6
        rowspan=1
        colspan=1
        for item in register_buttons:
            if item['Operation'] =='write':
                continue
            btn= QtWidgets.QPushButton(self.tabRegisters)
            btn.setObjectName(item['name'])
            btn.setText(item['name'])
            btn.setToolTip(f"{item['name']}, address: {item['address']}")
            self.dynamic_widgets[item['name']]=btn
            row=index//row_cols
            col=index%row_cols
            #if item['Operation'] in ['write','rw']:
            #    colspan=2
            address=item['address']
            if '0x' in address:
                address=int(address,16)
            else:
                address=int(address)
            
            btn.clicked.connect(
                partial(self.register_read, address))

            self.registerGridLayout.addWidget(btn, row, col, rowspan, colspan)
            index+=1
            


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
        self.show_message(msg,where, 'red')
    def info(self,msg,where=1, timestamp=True):
        self.show_message(msg,where,'dakGray', timestamp)
    def warning(self,msg,where=1):
        self.show_message(msg,where,'yellow')

    def show_message(self, msg, where=0, color='darkGray', timestamp=True):
        if where != 1:
            self.statusbar.showMessage(msg)
        if where != 0:
            if timestamp:
                msg=f'[{datetime.now().isoformat()}] {msg}'
            item = QtWidgets.QListWidgetItem(msg)
            item.setForeground(QtGui.QColor(color))
            self.listWidget.addItem(item)
        
    def close(self):
        self.MainWindow.close()
    def style(self):
        return self.MainWindow.style()
    def read_temperature(self):
        def _read_temperature():
            res=self.comm.get_temperatures()
            for msg in res: 
                self.info(msg)
        self.async_run(_read_temperature)

    def connect_host(self):
        def _connect_host():
            if  not self.is_connected:
                address=self.ipAddressInput.text()
                port=int(self.portInput.text())
                self.info(f'Connecting host {address} port {port}...')

                if self.comm.connect_host(address,port):
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
            self.comm.close_all()
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
    #    self.async_run(self.comm.status)

    def last_command(self):
        def _last_command():
            reg=0x52
            res=self.comm.read_register(reg)
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
            result=self.comm.read_register(reg_add)
            self.info(f'Register {hex(reg)} value: {result}')
        self.async_run(read_reg, reg)



