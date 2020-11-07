#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import sys
import signal
from PyQt5 import  QtWidgets, QtCore, QtGui
from mainwindow import Ui

def main():
    filename = None
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    window = Ui(MainWindow)
    MainWindow.show()
    #if filename:
    #    #window.openFile(filename)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
