#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import sys
import time
import pprint
import socket
import signal
import math
import queue
from datetime import datetime
from functools import partial

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QObject, QRunnable, QThreadPool
import pyqtgraph as pg
from core import window
from core import daq_comm
from core import config
from core import calibration

debug=False
MAX_LOG_ITEMS=5000


class WorkerSignals(QObject):
    '''
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
                # Return the result of the processing
                self.signals.result.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()  # Done


class Ui(window.Ui_MainWindow, daq_comm.DaqComm):
    def __init__(self, MainWindow):
        super(Ui, self).setupUi(MainWindow)
        super(Ui, self).__init__()
        self.MainWindow = MainWindow
        self.burst_read_fifo_length=514
        

        self.channel_id=10
        #self.waveform_data={}
        self.waveform_data={'time':0, 'data':{}}
        self.num_log_items=0

        self.current_folder = '.'
        self.dynamic_layouts = []
        self.dynamic_widgets = {}
        self.button_actions = {}
        self.is_connected = False
        self.archiving_enabled = False
        self.archiving_file = None
        self.buffer_packets = []
        self.burst_read=[]

        self.settings = QtCore.QSettings('LGR', 'daq')
        self.load_settings()

        self.register_names={}


        self.load_widgets()
        self.load_register_read_buttons()
        self.set_button_status(1, False)
        self.threadpool = QThreadPool()
        self.create_sci_chart()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.on_timeout)
        self.timer.start(1000)
        


        self.update_readout_widgets(1)
        self.statusTreeWidget.setColumnWidth(0,50)
        self.statusTreeWidget.setColumnWidth(1,300)
        self.readoutInput2.setHidden(True)
        self.readoutInput3.setHidden(True)
        self.readoutLabel2.setHidden(True)
        self.readoutLabel3.setHidden(True)

        
        button_connections = {
            self.connectBtn: self.ui_connect_host,
            self.openScriptButton: self.select_script_file,
            self.selectArchiveFolderButton: self.select_archive_folder,
            self.drs4SingleShotButton: self.drs4_single_read_btn_clicked,
            self.registerReadButton: self._register_read,
            self.executeScriptButton: self.execute_script,
            self.registerWriteButton: self._register_write,
            self.enableArchingButton: self.enable_archiving,
            self.truncateArchivingButton: self.truncate_archiving,
            self.drs4RunButton: self.drs4_run,
            self.readoutConfigButton: self.config_readout_mode,
            self.clearWaveformsButton: self.clear_waveforms,
            self.readStatusButton: self.read_and_show_status,
            self.hvSetPushButton:self.set_hv
        }
        actions = {self.action_Exit: self.closeEvent,
                   self.actionAbout: self.about,

                   }
        for btn, fun in button_connections.items():
            btn.clicked.connect(fun)
        for action, fun in actions.items():
            action.triggered.connect(fun)

        self.hv1OnPushButton.clicked.connect(lambda:self.power_on_off_hv(1, True))
        self.hv2OnPushButton.clicked.connect(lambda:self.power_on_off_hv(2, True))
        self.hv1OffPushButton.clicked.connect(lambda:self.power_on_off_hv(1, False)) 
        self.hv2OffPushButton.clicked.connect(lambda:self.power_on_off_hv(2, False)) 
        self.hvChannelSpinBox.valueChanged.connect(self.show_hv_channel)
        self.copyLogButton.clicked.connect(self.copy_log)
        
        self.readoutModeComboBox.currentIndexChanged.connect(self.readout_mode_change)
        self.registerAddressInput.textChanged.connect(self.update_register_info)
        #self.actionLogDock.stateChanged.connect(self.update_logger_state)
        self.logDockWidget.visibilityChanged['bool'].connect(self.actionLogDock.setChecked)
        self.actionLogDock.toggled['bool'].connect(self.logDockWidget.setVisible)

        self.channelListWidget.itemChanged.connect(self.update_drs4_channel_selection)
        self.waveformUpdatePeriodInput.valueChanged.connect(self.update_read_frequency)
        self.fifoLengthSpinBox.valueChanged.connect(self.update_fifo_read_length)

        self.drs4_timer = QtCore.QTimer()
        self.drs4_timer.timeout.connect(self.drs4_single_read_and_plot)
        self.drs4_timer_running = False
        self.update_drs4_channel_selection()
        #self.burst_fifo= queue.Queue()
        self.burst_fifo= []
        self.debug_waveform_phase=0

    def update_logger_state(self):
        pass
        
        
    def update_register_info(self):
        addr=self.registerAddressInput.text()
        if addr:
            name=self.register_names.get(str(daq_comm.parse_int(addr)),'Not defined register')
            self.registerNameLabel.setText(name)
    def read_and_show_status(self):
        value = self.read_register(0x02)
        self.statusTreeWidget.clear()
        true_color='#228b22'
        false_color='#b22222'
        self.statusUpdateInfoLabel.setText('Last updated at {} '.format(datetime.now().isoformat()))
        
        if value == None:
            self.error('Invalid status value!')
            return
        for bit in range(16):
            root = QtWidgets.QTreeWidgetItem(self.statusTreeWidget)
            root.setText(0, str(bit))
            root.setText(1, daq_comm.status_bits[bit])
            s=((value >> bit) & 1) == 1
            root.setText(2, 'True' if s else 'False')
            color=true_color if s else false_color
            root.setForeground(0, QtGui.QBrush(QtGui.QColor(color)))
            root.setForeground(1, QtGui.QBrush(QtGui.QColor(color)))
            root.setForeground(2, QtGui.QBrush(QtGui.QColor(color)))


    def load_settings(self):
        host = self.settings.value('host', [])
        if host:
            if len(host):
                self.ipAddressInput.setText(host[0])
                self.portInput.setValue(int(host[1]))
        archive = self.settings.value('archive', [])
        if archive:
            self.archiveFolderInput.setText(archive[0])
            self.archiveFilenamePrefixInput.setText(archive[1])
            self.archiveBufferSizeInput.setValue(int(archive[2]))
            self.archiveFilesizeMaxInput.setValue(int(archive[3]))
        script_name= self.settings.value('script', [])
        if script_name:
            self.scriptFilenameInput.setText(script_name)
    def update_readout_widgets(self, mode):
        conf=config.readouts
        for iw, wname in enumerate(conf['widgets']):
            widget= self.MainWindow.findChild(QtWidgets.QWidget, wname)
            visible=conf['visible'][mode][iw]
            name=conf['name'][mode][iw]
            widget.setHidden(not visible)
            widget.setText(name)
            
    def readout_mode_change(self):
        index=self.readoutModeComboBox.currentIndex()
        self.update_readout_widgets(index)
    def config_readout_mode(self):
        index=self.readoutModeComboBox.currentIndex()
        readout_mode=[3, 1,2]
        self.write_register(0x80, readout_mode[index])
        inputs=[self.readoutInput1.text(), 
                self.readoutInput2.text(), self.readoutInput3.text()] 
        self.write_register(0x81, daq_comm.parse_int(inputs[0]))
        if index>0:
            self.write_register(0x83, daq_comm.parse_int(inputs[2]))

        if index==1:
            self.write_register(0x82, daq_comm.parse_int(inputs[1]))
        elif index==2:
            self.write_register(0x84, daq_comm.parse_int(inputs[1]))




    def closeEvent(self, event):
        self.archive_manager.stop()
        self.close_all()
        self.MainWindow.close()

    def about(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText(
            f"DAQ for HIT, {config.version}, released on {config.release_date}, Hualin Xiao(hualin.xiao@psi.ch)")
        msgBox.setWindowTitle("HIT DAQ")

        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    def select_archive_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            None, 'Select working directory')
        self.archiveFolderInput.setText(folder)

    def truncate_archiving(self):
        filename = self.archive_manager.truncate()
        if filename:
            self.info(f'Log has been written to filename:{filename}')
            self.info(f'New log filename:{self.archive_manager.current_filename()}')
            return
        self.error(f'Archiving was not running.')

    def enable_archiving(self):
        self.info('Archiving button clicked')
        inputs = (self.archiveFolderInput, self.archiveFilenamePrefixInput,
                  self.archiveBufferSizeInput, self.archiveFilesizeMaxInput)
        self.settings.setValue('archive', [self.archiveFolderInput.text(),
                                           self.archiveFilenamePrefixInput.text(),
                                           self.archiveBufferSizeInput.value(),
                                           self.archiveFilesizeMaxInput.value()])

        if not self.archiving_enabled:
            self.archive_manager.start(self.archiveFolderInput.text(), self.archiveFilenamePrefixInput.text(),
                                       self.archiveBufferSizeInput.value(), self.archiveFilesizeMaxInput.value())

            self.currentArchiveFilenameLabel.setText(
                self.archive_manager.current_filename())
            self.archiving_enabled = self.archive_manager.is_running()
            filename = self.archive_manager.current_filename()
            if filename:
                self.info(f'Archiving enabled, archive filename:{filename}')
                for x in inputs:
                    x.setEnabled(False)

        else:
            self.archive_manager.stop()
            self.archiving_enabled = False
            self.info('Archiving stopped.')
            for x in inputs:
                x.setEnabled(True)

        state = 'ON' if self.archiving_enabled else 'OFF'
        style = "background-color:green; color: white;" if self.archiving_enabled else 'color: rgb(255, 255, 255); background-color: rgb(239, 41, 41);'
        self.archiveStatusLabel.setText(state)
        self.truncateArchivingButton.setEnabled(self.archiving_enabled)
        self.archiveStatusLabel.setStyleSheet(style)
        self.enableArchingButton.setText(
            'Disable Archiving' if self.archiving_enabled else 'Enable Archiving')

    def on_timeout(self):
        self.packetSentCounterLabel.setText(str(self.telecommand_counter))
        self.packetReadCounterLabel.setText(str(self.telemetry_counter))
        self.currentArchiveFilenameLabel.setText(
            self.archive_manager.current_filename())

    def create_sci_chart(self):
        pg.setConfigOption('leftButtonPan', False)
        self.plt= pg.PlotWidget()
    
        self.chartLayout = QtWidgets.QHBoxLayout(self.waveformGroupBox)
        self.chartLayout.addWidget(self.plt)
        colors=[(0,255,0),(255,0,0),(80,62,255),(136,86,167),(3,187,132),(227,74,51),(1,108,200),(255,158,119),(253,104,255), (255,200,200) ]
        #self.plt.addLegend()
        self.plots={i: self.plt.plot(pen=pg.mkPen(color=colors[i] ), 
            name=f'Channel {i+1}') for i in range(len(colors))}
        #set color for channel selection boxes
        for index,color in enumerate(colors):
            try:
                self.channelListWidget.item(index).setForeground(QtGui.QColor(color[0],color[1],color[2]))
            except:
                pass

        self.plt.setLabel('left', "ADC", units='')
        self.plt.setLabel('bottom', "Time", units='')
        self.plt.showGrid(x=True, y=True)
        self.plt.showAxis('top')
        self.plt.showAxis('right')
    def clear_waveforms(self):
        
        self.waveform_data['data']={}
        for index in self.plots:
            value=[0]
            self.plots[index].setData(value)

    def drs4_single_read_btn_clicked(self):
        self.info('Reading waveform...')
        for index in self.plots:
            value=[0]
            self.plots[index].setData(value)
        self.drs4_single_read_and_plot()
        self.info('Waveform updated')

    def drs4_single_read_and_plot(self):
        if self.is_fifo_empty() == None:
            self.info('Fifo status unknown!')
            self.clear_waveforms()
            return
        if self.is_fifo_empty() == True:
            #self.plot_waveform(self.waveform_data)
            self.clear_waveforms()
            self.info('Fifo is empty')
            return 
        i=0
        samples = self.fifo_burst_read(self.burst_read_fifo_length)
        len_samples=len(samples)
        self.waveform_data['data']={}

        while i < len_samples:
            timestamp=0
            sample=samples[i]
            if sample==0xFFFF:
                #timestamp
                self.plot_waveform(self.waveform_data)
                self.waveform_data['data']={}
                self.channel_id=0
                if i+3<len_samples:
                    self.waveform_data['time']=samples[i+1]*256+samples[i+2]
                    self.channel_id=samples[i+3]&0x000F
                    i=i+3
            elif sample >>4 == 0xfff:
                #a new channel
                self.channel_id=sample&0x000F
                self.plot_waveform(self.waveform_data)
            else:
                if self.channel_id not in self.waveform_data['data']:
                    self.waveform_data['data'][self.channel_id]=[]
                #print('add sample to channel:',self.channel_id)
                self.waveform_data['data'][self.channel_id].append(sample)
            i+=1


    def update_drs4_channel_selection(self):
        self.drs4_channel_enabled=[False]*self.channelListWidget.count()

        for index in range(self.channelListWidget.count()):
            item = self.channelListWidget.item(index)
            checked=item.checkState() == QtCore.Qt.Checked
            self.drs4_channel_enabled[index]=checked
            if not checked:
                self.plots[index].setData([0])
            #else:
            #    self.plt.addItem(self.plots[index])

            


    def update_fifo_read_length(self):
        self.burst_read_fifo_length=self.fifoLengthSpinBox.value()
        self.info(f'Burst fifo read length:{self.burst_read_fifo_length}')

    def update_read_frequency(self):
        if self.drs4_timer_running:
            self.drs4_timer.stop()
            self.drs4_timer_running = False
            update_period = self.waveformUpdatePeriodInput.value()
            ms = math.floor(update_period * 1000)
            self.drs4_timer.start(ms)
            self.drs4_timer_running = True



    def drs4_run(self):
        if self.drs4_timer_running:
            self.info('Waveform reading stopped.')
            self.drs4_timer.stop()
            self.drs4_timer_running = False
            self.drs4RunButton.setText('Run')
        else:
            self.info('Reading waveforms ...')
            update_period = self.waveformUpdatePeriodInput.value()
            ms = math.floor(update_period * 1000)
            self.drs4_timer.start(ms)
            self.drs4_timer_running = True
            self.drs4RunButton.setText('Stop')

    def plot_waveform(self, waveform_data):
        if not waveform_data['data']:
            return
        for key, value in waveform_data['data'].items():
            index=key
            #print('plotting waveforms: ', key, value)
            if len(value)>0 and index in self.plots:
                if self.drs4_channel_enabled[index]:
                    #self.plots[index].clear()
                    #print('plotting waveforms')
                    self.plots[index].setData(value)



    def _register_read(self):
        add = self.registerAddressInput.text()
        address = 0
        name = self.registerNameLabel.text()

        try:
            if '0x' in add:
                address = int(add, 16)
            else:
                address = int(add)
        except Exception as e:
            self.error('Invalid parameters')
            return

        loc, item = self.info(
            f'Reading register {name} (addr {address})', color='darkYellow')
        value = self.read_register(address)
        if value is not None:
            try:
                hexdec=hex(value)
            except Exception as e:
                hexdec=str(e)
            self.registerValueInput.setText(hexdec)
            self.info(f'{name} raw value {value} ({hexdec})', color='darkCyan')

    def _register_write(self):
        add = self.registerAddressInput.text()
        val = self.registerValueInput.text()
        address = 0
        value = 0
        name = self.registerNameLabel.text()

        try:
            if '0x' in add:
                address = int(add, 16)
            else:
                address = int(add)
            if '0x' in val:
                value = int(val, 16)
            else:
                value = int(val)

        except Exception as e:
            self.error('Invalid parameters')
            return

        value = self.write_register(address, value, 'Writing '+name)

    def set_button_status(self, level, status):
        button_groups = {
            0: [self.registerReadButton, self.registerWriteButton, self.executeScriptButton, self.readoutConfigButton,
                self.drs4SingleShotButton, self.drs4RunButton,  self.readStatusButton,
                self.hv1OnPushButton, 
                self.hv2OnPushButton, 
                self.hv1OffPushButton, 
                self.hv2OffPushButton, 
                self.hvChannelSpinBox,
                self.hvSetPushButton,
                self.hvDoubleSpinBox,
                ],
            1: []}
        if level >= 0:
            for btn in button_groups[0]:
                btn.setEnabled(status)
            for dynamic_btn in self.dynamic_widgets.values():
                dynamic_btn.setEnabled(status)
        if level >= 1:
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
        #self.create_groups('readoutsGroup')
        self.create_groups('readRegisterGroup')
        # self.create_groups('writeRegisterGroup')
        # self.create_groups('readWriteRegisterGroup')

    def create_groups(self, group_name):
        container = config.commands[group_name]['container']
        group = self.MainWindow.findChild(QtWidgets.QWidget, container)
        if not group:
            self.error('Can not find container {}'.format(container))
            return
        grid = QtWidgets.QGridLayout(group)
        self.dynamic_layouts.append(grid)
        commands = config.commands[group_name]['sequences']
        row_cols = config.commands[group_name]['grid_columns']
        rowspan = 1
        colspan = 1
        row = 0
        col = 0
        for item in commands:
            with_inputs = False
            layout = item.get('layout', 'inline')
            inputs = item.get('inputs', None)

            if inputs:
                if layout == 'row':
                    row += 1
                    col = 0
                label = QtWidgets.QLabel(group)
                label.setText(item['label'])
                grid.addWidget(label, row, col, rowspan, 1)
                if layout == 'row':
                    row += 1
                    col = 0
                else:
                    col += 1
                    if col >= colspan:
                        col = 1

                for sub_item in inputs:
                    with_inputs = True

                    edit = QtWidgets.QSpinBox(group)
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
                    self.dynamic_widgets[sub_item['name']] = edit
                    colspan = sub_item.get('colspan', 1)
                    grid.addWidget(edit, row, col, rowspan, colspan)

                    col += colspan
                    if col >= row_cols:
                        row += 1
                        col = 0

            colspan = 1
            btn = QtWidgets.QPushButton(group)
            btn_name = item['name']
            btn_title = item['button_title']
            btn.setObjectName(btn_name)
            btn.setText(btn_title)
            tooltip = item.get('tooltip', btn_title)
            btn.setToolTip(tooltip)
            btn.setStatusTip(tooltip)
            self.dynamic_widgets[btn_name] = btn
            btn.clicked.connect(
                partial(self.execute_sequence, item))
            grid.addWidget(btn, row, col, rowspan, colspan)

            if layout == 'row':
                row += 1
                col = 0
            else:
                col += 1
                if col >= row_cols:
                    row += 1
                    col = 0

    def _sequence_read(self, seq, args):
        loc, item = self.info(seq[2], color='darkYellow')
        value = self.read_register(seq[1][0])
        if value is not None:
            self.info(f'Result raw value: {value}', color='darkCyan')
            if len(seq[0]) > 1:
                callback = getattr(self, seq[0][1])
                result = callback(seq[1], value)
                if result:
                    self.info(f'Eng. value: {result}', color='darkCyan')

    def _sequence_write(self, seq, args):
        value = 0
        address, origin_value = seq[1]
        if isinstance(origin_value, str) and origin_value in args:
            value = args[origin_value]
        elif isinstance(origin_value, int):
            value = origin_value
        desc = ''
        try:
            desc = seq[2]
            placeholder = '{'+str(origin_value)+'}'
            if placeholder in desc:
                desc = desc.replace(placeholder, str(value))
        except Exception as e:
            self.error(str(e))
        self.write_register(address, value, desc)

    def _burst_read(self, seq, args):
        reg = seq[1][0]
        self.info('Burst read ... ')
        values = self.fifo_burst_read(self.burst_read_fifo_length)
        if not values:
            self.info('Result is None')
            return None

        self.info(f'Results (n={len(values)}):')
        result = '['
        if values:
            for i, val in enumerate(values):
                result += f'{val},'
                if i % 8 == 0 and i > 0:
                    self.info('{:50}'.format(result),
                              timestamp=False, color='blue')
                    result = ''
            if result:
                self.info('{:50}]'.format(result),
                          timestamp=False, color='blue')
        return None

    def execute_sequence(self, command, args):
        sequence = command['sequence']
        thread_lock = command.get('thread_lock', False)

        args = {}
        try:
            for item in command['inputs']:
                if item['type'] == 'int':
                    args[item['name']] = self.dynamic_widgets[item['name']].value()
                else:
                    args[item['name']] = self.dynamic_widgets[item['name']].text()

        except Exception as e:
            pass

        def _excecute_command():
            if thread_lock:
                try:
                    self.dynamic_widgets[command['name']].setEnabled(False)
                except:
                    pass
            for seq in sequence:
                func_name = seq[0][0]
                func = getattr(self, func_name)
                if func:
                    result = func(seq, args=args)
            try:
                self.dynamic_widgets[command['name']].setEnabled(True)
            except:
                pass

        _excecute_command()

        # self.async_run(_excecute_command)

    def load_register_read_buttons(self):
        self.registerGridLayout = QtWidgets.QGridLayout(self.registerListGroup)
        register_buttons = config.registers
        index = 0
        row_cols = 6
        rowspan = 1
        colspan = 1
        for item in register_buttons:
            addr=str(daq_comm.parse_int(item['address']))
            self.register_names[addr]=item['name']

            if 'write' not in item['operation']:
                continue
            btn = QtWidgets.QPushButton(self.registerListGroup)
            btn.setObjectName(item['name'])
            btn.setText(item['name'])
            btn.setToolTip(f"{item['name']}, address: {item['address']}")
            btn.setStatusTip(f"{item['name']}, address: {item['address']}")
            self.dynamic_widgets[item['name']] = btn
            row = index//row_cols
            col = index % row_cols

            btn.clicked.connect(
                partial(self.set_current_register, item))

            self.registerGridLayout.addWidget(btn, row, col, rowspan, colspan)
            index += 1

    def set_current_register(self, item):
        address = item['address']
        default = item['default']
        operation = item['operation']
        self.registerAddressInput.setText(address)
        self.registerNameLabel.setText(item['name'])
        if 'write' in operation:
            self.registerValueInput.setText(default)
        self.registerReadButton.setEnabled('read' in operation)
        self.registerWriteButton.setEnabled('write' in operation)

    def handle_finished(self):
        pass

    def handle_result(self, data):
        if isinstance(data, dict):
            if 'error' in data:
                self.error(data['error'])
                return
            if 'info' in data:
                self.info(data['info'])
                return
            if 'warning' in data:
                self.info(data['warning'])
                return
        self.info(str(data))

    def error(self, msg, where=1):
        return self.show_message(msg, where, 'red')

    def info(self, msg, where=1, timestamp=True, color=''):
        return self.show_message(msg, where, color, timestamp)

    def warning(self, msg, where=1):
        return self.show_message(msg, where, 'red')

    def show_message(self, msg, where=0, color='darkGray', timestamp=True):
        self.archive_manager.write_one(msg)
        if where != 1:
            self.statusbar.showMessage(msg)
            return 'status', self.statusbar
        if where != 0:
            if timestamp:
                msg = f'[{datetime.now().isoformat()}] {msg}'
            if self.num_log_items>MAX_LOG_ITEMS:
                return 'log',item
            if self.num_log_items == MAX_LOG_ITEMS:
                color='red'
                msg=f"Log window can not show more than {MAX_LOG_ITEMS} items!"
            


            item = QtWidgets.QListWidgetItem(msg)
            item.setForeground(QtGui.QColor(color))
            self.listWidget.addItem(item)
            self.listWidget.scrollToBottom()
            self.num_log_items+=1
            return 'log', item

    def close(self):
        self.MainWindow.close()

    def style(self):
        return self.MainWindow.style()

    def read_temperature(self):
        def _read_temperature():
            res = self.get_temperatures()
            for msg in res:
                self.info(msg)
        _read_temperature()

    def ui_connect_host(self):
        def _connect_host():
            if not self.is_connected:
                address = self.ipAddressInput.text()
                port = int(self.portInput.text())
                self.info(f'Connecting host {address} port {port}...')
                self.settings.setValue('host', [address, port])

                if self.connect_host(address, port):
                    self.is_connected = True
                    self.info('Connected.')
                    self.connectBtn.setText('Disconnect')
                    self.portInput.setEnabled(False)
                    self.ipAddressInput.setEnabled(False)
                    self.connectBtn.setStyleSheet(
                        "background-color:green; color: white;")
                    self.set_button_status(0, True)
                else:
                    self.error('Connection failed!')
                return
            self.close_all()
            self.info('Disconnected!')
            self.connectBtn.setText('Connect')
            self.portInput.setEnabled(True)
            self.ipAddressInput.setEnabled(True)
            self.is_connected = False
            self.connectBtn.setStyleSheet("")
            self.set_button_status(1, False)
        _connect_host()

    def select_script_file(self):
        try:
            fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Open script file',
                                                          '.', "script files (*.txt *.csv)")[0]
            self.scriptFilenameInput.setText(fname)
        except Exception as e:
            pass

    def execute_script(self):
        fname = self.scriptFilenameInput.text()
        if not fname:
            self.error('Select a script file first!')
            return
        self.info(f'Starting to execute {fname} ...')
        self.settings.setValue('script',fname)
        with open(fname) as fs:
            lines = fs.readlines()
            commands = []
            for l in lines:
                line = l.strip()
                if line.startswith('#') or not line:
                    continue
                if '#' in line:
                    line = line.split('#')[0]
                cmd = line.split()

                if len(cmd) >= 2:
                    commands.append(cmd)

        def _execute_script(cmds):
            for cmd in cmds:
                if cmd[0] == 'wait':
                    loc, item = self.info(
                        f'Waiting for {cmd[1]} s', color='darkYellow')
                    time.sleep(int(cmd[1]))
                elif cmd[0] == 'read':
                    msg = 'Reading register {}'.format(cmd[1])
                    loc, item = self.info(msg, color='darkYellow')
                    value = self.read_register(cmd[1])
                    if value is not None:
                        self.info(
                            f'Result raw value: {value}', color='darkCyan')
                elif cmd[0] == 'write':
                    msg = 'Writing register {} {}'.format(cmd[1], cmd[2])
                    loc, item = self.info(msg, color='darkYellow')
                    self.write_register(cmd[1], cmd[2], '')
        try:
            _execute_script(commands)
        except Exception as e:
            self.erro(str(e))

    def last_command(self):
        def _last_command():
            reg = 0x52
            res = self.read_register(reg)
            if res:
                msg = "register: %s read = %s" % (hex(reg), hex(res))
                self.info(msg)
            else:
                self.info('Return value is None')
        self.async_run(_last_command)

    def register_read(self, reg):
        def read_reg(reg_add):
            self.info(f'Reading  {hex(reg)} ...')
            result = self.read_register(reg_add)
            self.info(f'Register {hex(reg)} value: {result} {hex(result)}')
        self.async_run(read_reg, reg)

    def power_on_off_hv(self, hvch, status):
        address=0x41 if hvch==1 else 0x42
        value=0xffff if status else 0x0000
        value = self.write_register(address, value)
    def set_hv(self):
        channel=self.hvChannelSpinBox.value()
        value=self.hvDoubleSpinBox.value()
        addr=channel+0x31
        raw=calibration.convert_HV_real_to_raw(value)
        value=self.write_register(addr, raw)
    def show_hv_channel(self):
        channel=self.hvChannelSpinBox.value()
        position={5:'Pos 1', 7:'Pos 2', 3:'Pos 3', 2:'Pos 4' }
        self.hvPosition.setText(position.get(channel, 'Unused'))

    def copy_log(self):
        text =  '\n'.join([str(self.listWidget.item(i).text()) for i in range(self.listWidget.count())])
        cb = QtWidgets.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(text, mode=cb.Clipboard) 
        self.statusbar.showMessage('The log has been copied to the clipboard')
    



