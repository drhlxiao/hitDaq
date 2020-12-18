# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1322, 950)
        MainWindow.setStyleSheet("")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockNestingEnabled(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(600, 300))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.tabWidget.setFont(font)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("QTabBar::tab { height: 35px; }")
        self.tabWidget.setIconSize(QtCore.QSize(20, 20))
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tabControls = QtWidgets.QWidget()
        self.tabControls.setObjectName("tabControls")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tabControls)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.connectionGroup = QtWidgets.QGroupBox(self.tabControls)
        self.connectionGroup.setMaximumSize(QtCore.QSize(16777215, 100))
        self.connectionGroup.setObjectName("connectionGroup")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.connectionGroup)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.connectionGroup)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.ipAddressInput = QtWidgets.QLineEdit(self.connectionGroup)
        self.ipAddressInput.setMaximumSize(QtCore.QSize(200, 16777215))
        self.ipAddressInput.setObjectName("ipAddressInput")
        self.horizontalLayout.addWidget(self.ipAddressInput)
        self.portLabel = QtWidgets.QLabel(self.connectionGroup)
        self.portLabel.setObjectName("portLabel")
        self.horizontalLayout.addWidget(self.portLabel)
        self.portInput = QtWidgets.QSpinBox(self.connectionGroup)
        self.portInput.setMaximum(65535)
        self.portInput.setProperty("value", 1002)
        self.portInput.setObjectName("portInput")
        self.horizontalLayout.addWidget(self.portInput)
        self.connectBtn = QtWidgets.QPushButton(self.connectionGroup)
        self.connectBtn.setObjectName("connectBtn")
        self.horizontalLayout.addWidget(self.connectBtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3.addWidget(self.connectionGroup)
        self.basicOperationGroup = QtWidgets.QGroupBox(self.tabControls)
        self.basicOperationGroup.setMinimumSize(QtCore.QSize(0, 150))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.basicOperationGroup.setFont(font)
        self.basicOperationGroup.setObjectName("basicOperationGroup")
        self.verticalLayout_3.addWidget(self.basicOperationGroup)
        self.readoutsGroup = QtWidgets.QGroupBox(self.tabControls)
        self.readoutsGroup.setMinimumSize(QtCore.QSize(0, 120))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.readoutsGroup.setFont(font)
        self.readoutsGroup.setObjectName("readoutsGroup")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.readoutsGroup)
        self.gridLayout_4.setContentsMargins(-1, 1, 1, -1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_14 = QtWidgets.QLabel(self.readoutsGroup)
        self.label_14.setObjectName("label_14")
        self.gridLayout_4.addWidget(self.label_14, 0, 0, 1, 1)
        self.readoutModeComboBox = QtWidgets.QComboBox(self.readoutsGroup)
        self.readoutModeComboBox.setObjectName("readoutModeComboBox")
        self.readoutModeComboBox.addItem("")
        self.readoutModeComboBox.addItem("")
        self.readoutModeComboBox.addItem("")
        self.gridLayout_4.addWidget(self.readoutModeComboBox, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(926, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 2, 1, 6)
        self.readoutLabel1 = QtWidgets.QLabel(self.readoutsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.readoutLabel1.sizePolicy().hasHeightForWidth())
        self.readoutLabel1.setSizePolicy(sizePolicy)
        self.readoutLabel1.setObjectName("readoutLabel1")
        self.gridLayout_4.addWidget(self.readoutLabel1, 1, 0, 1, 1)
        self.readoutInput1 = QtWidgets.QLineEdit(self.readoutsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.readoutInput1.sizePolicy().hasHeightForWidth())
        self.readoutInput1.setSizePolicy(sizePolicy)
        self.readoutInput1.setObjectName("readoutInput1")
        self.gridLayout_4.addWidget(self.readoutInput1, 1, 1, 1, 1)
        self.readoutLabel2 = QtWidgets.QLabel(self.readoutsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.readoutLabel2.sizePolicy().hasHeightForWidth())
        self.readoutLabel2.setSizePolicy(sizePolicy)
        self.readoutLabel2.setObjectName("readoutLabel2")
        self.gridLayout_4.addWidget(self.readoutLabel2, 1, 2, 1, 1)
        self.readoutInput2 = QtWidgets.QLineEdit(self.readoutsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.readoutInput2.sizePolicy().hasHeightForWidth())
        self.readoutInput2.setSizePolicy(sizePolicy)
        self.readoutInput2.setObjectName("readoutInput2")
        self.gridLayout_4.addWidget(self.readoutInput2, 1, 3, 1, 1)
        self.readoutLabel3 = QtWidgets.QLabel(self.readoutsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.readoutLabel3.sizePolicy().hasHeightForWidth())
        self.readoutLabel3.setSizePolicy(sizePolicy)
        self.readoutLabel3.setObjectName("readoutLabel3")
        self.gridLayout_4.addWidget(self.readoutLabel3, 1, 4, 1, 1)
        self.readoutInput3 = QtWidgets.QLineEdit(self.readoutsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.readoutInput3.sizePolicy().hasHeightForWidth())
        self.readoutInput3.setSizePolicy(sizePolicy)
        self.readoutInput3.setObjectName("readoutInput3")
        self.gridLayout_4.addWidget(self.readoutInput3, 1, 5, 1, 1)
        self.readoutConfigButton = QtWidgets.QPushButton(self.readoutsGroup)
        self.readoutConfigButton.setObjectName("readoutConfigButton")
        self.gridLayout_4.addWidget(self.readoutConfigButton, 1, 6, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(387, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 1, 7, 1, 1)
        self.verticalLayout_3.addWidget(self.readoutsGroup)
        self.groupBox = QtWidgets.QGroupBox(self.tabControls)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_6.setSpacing(5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.openScriptButton = QtWidgets.QPushButton(self.groupBox)
        self.openScriptButton.setObjectName("openScriptButton")
        self.horizontalLayout_6.addWidget(self.openScriptButton)
        self.scriptFilenameInput = QtWidgets.QLineEdit(self.groupBox)
        self.scriptFilenameInput.setMinimumSize(QtCore.QSize(450, 0))
        self.scriptFilenameInput.setObjectName("scriptFilenameInput")
        self.horizontalLayout_6.addWidget(self.scriptFilenameInput)
        self.executeScriptButton = QtWidgets.QPushButton(self.groupBox)
        self.executeScriptButton.setObjectName("executeScriptButton")
        self.horizontalLayout_6.addWidget(self.executeScriptButton)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.verticalLayout_7.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tabControls, "")
        self.tabRegisters = QtWidgets.QWidget()
        self.tabRegisters.setObjectName("tabRegisters")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tabRegisters)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.registerContainerTab = QtWidgets.QTabWidget(self.tabRegisters)
        self.registerContainerTab.setObjectName("registerContainerTab")
        self.registerReadTab = QtWidgets.QWidget()
        self.registerReadTab.setObjectName("registerReadTab")
        self.registerContainerTab.addTab(self.registerReadTab, "")
        self.registerReadWriteTab = QtWidgets.QWidget()
        self.registerReadWriteTab.setObjectName("registerReadWriteTab")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.registerReadWriteTab)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.registerReadWriteTab)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.registerAddressInput = QtWidgets.QLineEdit(self.registerReadWriteTab)
        self.registerAddressInput.setMaximumSize(QtCore.QSize(200, 16777215))
        self.registerAddressInput.setObjectName("registerAddressInput")
        self.horizontalLayout_5.addWidget(self.registerAddressInput)
        self.label_5 = QtWidgets.QLabel(self.registerReadWriteTab)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.registerValueInput = QtWidgets.QLineEdit(self.registerReadWriteTab)
        self.registerValueInput.setMaximumSize(QtCore.QSize(200, 100))
        self.registerValueInput.setObjectName("registerValueInput")
        self.horizontalLayout_5.addWidget(self.registerValueInput)
        self.registerWriteButton = QtWidgets.QPushButton(self.registerReadWriteTab)
        self.registerWriteButton.setObjectName("registerWriteButton")
        self.horizontalLayout_5.addWidget(self.registerWriteButton)
        self.registerReadButton = QtWidgets.QPushButton(self.registerReadWriteTab)
        self.registerReadButton.setObjectName("registerReadButton")
        self.horizontalLayout_5.addWidget(self.registerReadButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_9.addLayout(self.horizontalLayout_5)
        self.registerNameLabel = QtWidgets.QLabel(self.registerReadWriteTab)
        self.registerNameLabel.setMaximumSize(QtCore.QSize(16777215, 50))
        self.registerNameLabel.setAutoFillBackground(False)
        self.registerNameLabel.setStyleSheet("color: rgb(114, 159, 207);")
        self.registerNameLabel.setObjectName("registerNameLabel")
        self.verticalLayout_9.addWidget(self.registerNameLabel)
        self.registerListGroup = QtWidgets.QGroupBox(self.registerReadWriteTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.registerListGroup.sizePolicy().hasHeightForWidth())
        self.registerListGroup.setSizePolicy(sizePolicy)
        self.registerListGroup.setObjectName("registerListGroup")
        self.verticalLayout_9.addWidget(self.registerListGroup)
        self.registerContainerTab.addTab(self.registerReadWriteTab, "")
        self.verticalLayout_8.addWidget(self.registerContainerTab)
        self.tabWidget.addTab(self.tabRegisters, "")
        self.tabScience = QtWidgets.QWidget()
        self.tabScience.setObjectName("tabScience")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tabScience)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.waveformGroupBox = QtWidgets.QGroupBox(self.tabScience)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.waveformGroupBox.sizePolicy().hasHeightForWidth())
        self.waveformGroupBox.setSizePolicy(sizePolicy)
        self.waveformGroupBox.setObjectName("waveformGroupBox")
        self.gridLayout_3.addWidget(self.waveformGroupBox, 0, 0, 5, 1)
        self.line = QtWidgets.QFrame(self.tabScience)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 0, 1, 5, 1)
        self.drs4SingleShotButton = QtWidgets.QPushButton(self.tabScience)
        self.drs4SingleShotButton.setObjectName("drs4SingleShotButton")
        self.gridLayout_3.addWidget(self.drs4SingleShotButton, 0, 2, 1, 1)
        self.drs4RunButton = QtWidgets.QPushButton(self.tabScience)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drs4RunButton.sizePolicy().hasHeightForWidth())
        self.drs4RunButton.setSizePolicy(sizePolicy)
        self.drs4RunButton.setMinimumSize(QtCore.QSize(100, 0))
        self.drs4RunButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.drs4RunButton.setStyleSheet("")
        self.drs4RunButton.setObjectName("drs4RunButton")
        self.gridLayout_3.addWidget(self.drs4RunButton, 0, 4, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.tabScience)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 1, 2, 1, 2)
        self.waveformUpdatePeriodInput = QtWidgets.QDoubleSpinBox(self.tabScience)
        self.waveformUpdatePeriodInput.setMinimum(0.1)
        self.waveformUpdatePeriodInput.setSingleStep(0.1)
        self.waveformUpdatePeriodInput.setProperty("value", 0.5)
        self.waveformUpdatePeriodInput.setObjectName("waveformUpdatePeriodInput")
        self.gridLayout_3.addWidget(self.waveformUpdatePeriodInput, 1, 4, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.tabScience)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 2, 2, 1, 2)
        self.channelListWidget = QtWidgets.QListWidget(self.tabScience)
        self.channelListWidget.setMinimumSize(QtCore.QSize(200, 0))
        self.channelListWidget.setMaximumSize(QtCore.QSize(220, 16777215))
        self.channelListWidget.setObjectName("channelListWidget")
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.channelListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.channelListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.channelListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.channelListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.channelListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.channelListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.channelListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        item.setCheckState(QtCore.Qt.Checked)
        self.channelListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.channelListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.channelListWidget.addItem(item)
        self.gridLayout_3.addWidget(self.channelListWidget, 3, 2, 1, 3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 223, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem4, 4, 3, 1, 1)
        self.tabWidget.addTab(self.tabScience, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.readStatusButton = QtWidgets.QPushButton(self.tab)
        self.readStatusButton.setObjectName("readStatusButton")
        self.verticalLayout_6.addWidget(self.readStatusButton)
        self.statusTreeWidget = QtWidgets.QTreeWidget(self.tab)
        self.statusTreeWidget.setObjectName("statusTreeWidget")
        self.verticalLayout_6.addWidget(self.statusTreeWidget)
        self.statusUpdateInfoLabel = QtWidgets.QLabel(self.tab)
        self.statusUpdateInfoLabel.setObjectName("statusUpdateInfoLabel")
        self.verticalLayout_6.addWidget(self.statusUpdateInfoLabel)
        self.tabWidget.addTab(self.tab, "")
        self.tabArchive = QtWidgets.QWidget()
        self.tabArchive.setObjectName("tabArchive")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tabArchive)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tabArchive)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_2 = QtWidgets.QFrame(self.groupBox_2)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.archiveFolderInput = QtWidgets.QLineEdit(self.frame_2)
        self.archiveFolderInput.setMinimumSize(QtCore.QSize(500, 0))
        self.archiveFolderInput.setMaximumSize(QtCore.QSize(500, 16777215))
        self.archiveFolderInput.setObjectName("archiveFolderInput")
        self.gridLayout.addWidget(self.archiveFolderInput, 0, 1, 1, 4)
        self.selectArchiveFolderButton = QtWidgets.QPushButton(self.frame_2)
        self.selectArchiveFolderButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.selectArchiveFolderButton.setObjectName("selectArchiveFolderButton")
        self.gridLayout.addWidget(self.selectArchiveFolderButton, 0, 5, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(491, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 0, 6, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)
        self.archiveFilenamePrefixInput = QtWidgets.QLineEdit(self.frame_2)
        self.archiveFilenamePrefixInput.setMaximumSize(QtCore.QSize(500, 16777215))
        self.archiveFilenamePrefixInput.setObjectName("archiveFilenamePrefixInput")
        self.gridLayout.addWidget(self.archiveFilenamePrefixInput, 1, 1, 1, 4)
        spacerItem6 = QtWidgets.QSpacerItem(578, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 1, 5, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.archiveBufferSizeInput = QtWidgets.QSpinBox(self.frame_2)
        self.archiveBufferSizeInput.setMinimumSize(QtCore.QSize(150, 0))
        self.archiveBufferSizeInput.setMaximumSize(QtCore.QSize(150, 16777215))
        self.archiveBufferSizeInput.setMaximum(1024000)
        self.archiveBufferSizeInput.setSingleStep(100)
        self.archiveBufferSizeInput.setProperty("value", 4096)
        self.archiveBufferSizeInput.setObjectName("archiveBufferSizeInput")
        self.gridLayout.addWidget(self.archiveBufferSizeInput, 2, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 2, 2, 1, 2)
        self.archiveFilesizeMaxInput = QtWidgets.QSpinBox(self.frame_2)
        self.archiveFilesizeMaxInput.setMinimumSize(QtCore.QSize(150, 0))
        self.archiveFilesizeMaxInput.setMaximumSize(QtCore.QSize(150, 16777215))
        self.archiveFilesizeMaxInput.setMaximum(10240)
        self.archiveFilesizeMaxInput.setProperty("value", 256)
        self.archiveFilesizeMaxInput.setObjectName("archiveFilesizeMaxInput")
        self.gridLayout.addWidget(self.archiveFilesizeMaxInput, 2, 4, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(578, 27, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem7, 2, 5, 1, 2)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem8, 3, 0, 1, 1)
        self.enableArchingButton = QtWidgets.QPushButton(self.frame_2)
        self.enableArchingButton.setObjectName("enableArchingButton")
        self.gridLayout.addWidget(self.enableArchingButton, 3, 1, 1, 1)
        self.truncateArchivingButton = QtWidgets.QPushButton(self.frame_2)
        self.truncateArchivingButton.setEnabled(False)
        self.truncateArchivingButton.setObjectName("truncateArchivingButton")
        self.gridLayout.addWidget(self.truncateArchivingButton, 3, 2, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(711, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem9, 3, 3, 1, 4)
        self.horizontalLayout_4.addWidget(self.frame_2)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.tabArchive)
        self.groupBox_3.setMaximumSize(QtCore.QSize(16777215, 300))
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.packetSentCounterLabel = QtWidgets.QLabel(self.groupBox_3)
        self.packetSentCounterLabel.setMinimumSize(QtCore.QSize(200, 0))
        self.packetSentCounterLabel.setText("")
        self.packetSentCounterLabel.setObjectName("packetSentCounterLabel")
        self.gridLayout_2.addWidget(self.packetSentCounterLabel, 2, 2, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(20, 372, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem10, 4, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)
        self.currentArchiveFilenameLabel = QtWidgets.QLabel(self.groupBox_3)
        self.currentArchiveFilenameLabel.setMinimumSize(QtCore.QSize(300, 0))
        self.currentArchiveFilenameLabel.setAutoFillBackground(False)
        self.currentArchiveFilenameLabel.setText("")
        self.currentArchiveFilenameLabel.setObjectName("currentArchiveFilenameLabel")
        self.gridLayout_2.addWidget(self.currentArchiveFilenameLabel, 1, 2, 1, 1)
        self.packetReadCounterLabel = QtWidgets.QLabel(self.groupBox_3)
        self.packetReadCounterLabel.setMinimumSize(QtCore.QSize(200, 0))
        self.packetReadCounterLabel.setText("")
        self.packetReadCounterLabel.setObjectName("packetReadCounterLabel")
        self.gridLayout_2.addWidget(self.packetReadCounterLabel, 3, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 3, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox_3)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 0, 0, 1, 1)
        self.archiveStatusLabel = QtWidgets.QLabel(self.groupBox_3)
        self.archiveStatusLabel.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(239, 41, 41);")
        self.archiveStatusLabel.setObjectName("archiveStatusLabel")
        self.gridLayout_2.addWidget(self.archiveStatusLabel, 0, 1, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem11, 0, 2, 1, 1)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.tabWidget.addTab(self.tabArchive, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1322, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.logDockWidget = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logDockWidget.sizePolicy().hasHeightForWidth())
        self.logDockWidget.setSizePolicy(sizePolicy)
        self.logDockWidget.setMinimumSize(QtCore.QSize(120, 200))
        self.logDockWidget.setFloating(False)
        self.logDockWidget.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.logDockWidget.setObjectName("logDockWidget")
        self.logDock = QtWidgets.QWidget()
        self.logDock.setAutoFillBackground(False)
        self.logDock.setObjectName("logDock")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.logDock)
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(5, 2, 5, 2)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.logDock)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.listWidget = QtWidgets.QListWidget(self.logDock)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.logDockWidget.setWidget(self.logDock)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.logDockWidget)
        self.actionIP = QtWidgets.QAction(MainWindow)
        self.actionIP.setObjectName("actionIP")
        self.action_Exit = QtWidgets.QAction(MainWindow)
        self.action_Exit.setObjectName("action_Exit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionLogDock = QtWidgets.QAction(MainWindow)
        self.actionLogDock.setCheckable(True)
        self.actionLogDock.setChecked(True)
        self.actionLogDock.setObjectName("actionLogDock")
        self.menuFile.addAction(self.action_Exit)
        self.menuSettings.addAction(self.actionIP)
        self.menuHelp.addAction(self.actionAbout)
        self.menuView.addAction(self.actionLogDock)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.registerContainerTab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HIT DAQ"))
        self.connectionGroup.setTitle(_translate("MainWindow", "Connection"))
        self.label.setText(_translate("MainWindow", "IP"))
        self.ipAddressInput.setText(_translate("MainWindow", "10.42.0.136"))
        self.portLabel.setText(_translate("MainWindow", "Port"))
        self.connectBtn.setText(_translate("MainWindow", "Connect"))
        self.basicOperationGroup.setTitle(_translate("MainWindow", "Commands"))
        self.readoutsGroup.setTitle(_translate("MainWindow", "Readout"))
        self.label_14.setText(_translate("MainWindow", "Readout mode:"))
        self.readoutModeComboBox.setItemText(0, _translate("MainWindow", "Full"))
        self.readoutModeComboBox.setItemText(1, _translate("MainWindow", "ROI"))
        self.readoutModeComboBox.setItemText(2, _translate("MainWindow", "Smart"))
        self.readoutLabel1.setText(_translate("MainWindow", "Readout channels:"))
        self.readoutLabel2.setText(_translate("MainWindow", "delay"))
        self.readoutLabel3.setText(_translate("MainWindow", "samples"))
        self.readoutConfigButton.setText(_translate("MainWindow", "Set"))
        self.groupBox.setTitle(_translate("MainWindow", "Execute Script"))
        self.openScriptButton.setToolTip(_translate("MainWindow", "Open a script to execute"))
        self.openScriptButton.setText(_translate("MainWindow", "Open"))
        self.executeScriptButton.setText(_translate("MainWindow", "Run"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabControls), _translate("MainWindow", "Configuration"))
        self.registerContainerTab.setTabText(self.registerContainerTab.indexOf(self.registerReadTab), _translate("MainWindow", "Register Read"))
        self.label_4.setText(_translate("MainWindow", "Register"))
        self.label_5.setText(_translate("MainWindow", "Value"))
        self.registerWriteButton.setText(_translate("MainWindow", "Write"))
        self.registerReadButton.setText(_translate("MainWindow", "Read"))
        self.registerNameLabel.setText(_translate("MainWindow", "."))
        self.registerListGroup.setTitle(_translate("MainWindow", "Select a register to read/write"))
        self.registerContainerTab.setTabText(self.registerContainerTab.indexOf(self.registerReadWriteTab), _translate("MainWindow", "Register Read/Write"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabRegisters), _translate("MainWindow", "Registers"))
        self.waveformGroupBox.setTitle(_translate("MainWindow", "DRS4 waveforms"))
        self.drs4SingleShotButton.setText(_translate("MainWindow", "Single"))
        self.drs4RunButton.setText(_translate("MainWindow", "Run"))
        self.label_13.setText(_translate("MainWindow", "Refresh(s)"))
        self.label_15.setText(_translate("MainWindow", "Filter:"))
        __sortingEnabled = self.channelListWidget.isSortingEnabled()
        self.channelListWidget.setSortingEnabled(False)
        item = self.channelListWidget.item(0)
        item.setText(_translate("MainWindow", "Channel 1"))
        item = self.channelListWidget.item(1)
        item.setText(_translate("MainWindow", "Channel 2"))
        item = self.channelListWidget.item(2)
        item.setText(_translate("MainWindow", "Channel 3"))
        item = self.channelListWidget.item(3)
        item.setText(_translate("MainWindow", "Channel 4"))
        item = self.channelListWidget.item(4)
        item.setText(_translate("MainWindow", "Channel 5"))
        item = self.channelListWidget.item(5)
        item.setText(_translate("MainWindow", "Channel 6"))
        item = self.channelListWidget.item(6)
        item.setText(_translate("MainWindow", "Channel 7"))
        item = self.channelListWidget.item(7)
        item.setText(_translate("MainWindow", "Channel 8"))
        item = self.channelListWidget.item(8)
        item.setText(_translate("MainWindow", "Channel 9"))
        item = self.channelListWidget.item(9)
        item.setText(_translate("MainWindow", "Debug"))
        self.channelListWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabScience), _translate("MainWindow", "Science"))
        self.readStatusButton.setText(_translate("MainWindow", "Update"))
        self.statusTreeWidget.headerItem().setText(0, _translate("MainWindow", "ID"))
        self.statusTreeWidget.headerItem().setText(1, _translate("MainWindow", "Name"))
        self.statusTreeWidget.headerItem().setText(2, _translate("MainWindow", "Status"))
        self.statusUpdateInfoLabel.setText(_translate("MainWindow", "Last updated: "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Status"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Configuration"))
        self.label_6.setText(_translate("MainWindow", "Working driectory:"))
        self.archiveFolderInput.setText(_translate("MainWindow", "/tmp/"))
        self.selectArchiveFolderButton.setText(_translate("MainWindow", "Select..."))
        self.label_7.setText(_translate("MainWindow", "Filename prefix:"))
        self.archiveFilenamePrefixInput.setText(_translate("MainWindow", "daq_"))
        self.label_2.setText(_translate("MainWindow", "Buffer size:"))
        self.label_12.setText(_translate("MainWindow", "Max filesize (kB): "))
        self.enableArchingButton.setText(_translate("MainWindow", "Enable Archiving"))
        self.truncateArchivingButton.setText(_translate("MainWindow", "Truncate"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Status"))
        self.label_9.setText(_translate("MainWindow", "Packets sent:"))
        self.label_8.setText(_translate("MainWindow", "Current file:"))
        self.label_10.setText(_translate("MainWindow", "Packets Read:"))
        self.label_11.setText(_translate("MainWindow", "Archive:"))
        self.archiveStatusLabel.setText(_translate("MainWindow", "OFF"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabArchive), _translate("MainWindow", "Archive"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuSettings.setTitle(_translate("MainWindow", "&Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.label_3.setText(_translate("MainWindow", "Log"))
        self.actionIP.setText(_translate("MainWindow", "IP"))
        self.action_Exit.setText(_translate("MainWindow", "&Exit"))
        self.actionAbout.setText(_translate("MainWindow", "&About"))
        self.actionLogDock.setText(_translate("MainWindow", "Log docker"))
from core import mainwindow_rc5_rc
