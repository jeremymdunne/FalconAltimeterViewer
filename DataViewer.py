from PyQt5.QtWidgets import QWidget, QDesktopWidget,QLabel,QLayout, QLineEdit, QFileDialog, QMessageBox, QApplication, QPushButton, QGridLayout, QTabWidget, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
import pyqtgraph as pg


class DataViewer(QWidget):
    def __init__(self, tabWidget, openLogCallback, connectCallback):
        super(QWidget,self).__init__(tabWidget)
        self.openCallback = openLogCallback
        self.connectCallback = connectCallback
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        pg.setConfigOption('background', 'w')
        self.mainPlot = pg.PlotWidget()
        self.mainPlot.enableAutoRange()
        self.mainPlot.setLabel('left','Altitude',units = 'm')
        self.mainPlot.setLabel('bottom','Time',units = 'sec')
        self.mainPlot.addLegend()
        self.mainPlot.setWindowTitle('Altitude Graph')
        self.openLogBtn = QPushButton("Open Log")
        self.openLogBtn.clicked.connect(self.handleOpenCallback)
        self.connectBtn = QPushButton("Connect to Falcon")
        self.connectBtn.clicked.connect(self.handleConnectCallback)
        self.grid.addWidget(self.mainPlot,0,0,1,2)
        self.grid.addWidget(self.openLogBtn,1,0)
        self.grid.addWidget(self.connectBtn,1,1)
        self.show()

    def handleConnectCallback(self):
        self.connectCallback()

    def handleOpenCallback(self):
        self.openCallback()

    def graph(self,data):
        #go open up the file for now
        x=[]
        y=[]
        for a in data:
            x.append(a[0]/1000.0)
            y.append(a[1])
        self.mainPlot.plot(x,y, pen='b',name='Altitude')


    def graphData(data, type):
        pass
