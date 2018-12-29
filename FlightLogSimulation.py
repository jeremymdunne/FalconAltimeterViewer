from PyQt5.QtWidgets import QWidget, QDesktopWidget,QLabel,QLayout, QLineEdit, QFileDialog, QMessageBox, QApplication, QPushButton, QGridLayout, QTabWidget, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
import pyqtgraph as pg

class FlightLogSimulation(QWidget):
    def __init__(self, tabWidget, runSimulationCallback, openLogCallback, connectCallback):
        super(QWidget,self).__init__(tabWidget)
        self.runSimulationCallback = runSimulationCallback
        self.openCallback = openLogCallback
        self.connectCallback = connectCallback
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.runSimulationBtn = QPushButton("Run Simulation")
        self.runSimulationBtn.clicked.connect(self.runSimulationCallback)
        self.openLogBtn = QPushButton("Open Log")
        self.openLogBtn.clicked.connect(self.handleOpenCallback)
        self.connectBtn = QPushButton("Connect to Falcon")
        self.connectBtn.clicked.connect(self.handleConnectCallback)
        self.grid.addWidget(self.runSimulationBtn,0,0,1,2)
        self.grid.addWidget(self.openLogBtn,1,0)
        self.grid.addWidget(self.connectBtn,1,1)

    def handleConnectCallback(self):
        self.connectCallback()

    def handleOpenCallback(self):
        self.openCallback()
