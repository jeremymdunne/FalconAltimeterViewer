from PyQt5.QtWidgets import QWidget, QDesktopWidget,QLabel,QLayout, QLineEdit, QFileDialog, QMessageBox, QApplication, QPushButton, QGridLayout, QTabWidget, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
import pyqtgraph as pg

class Programmer(QWidget):
    def __init__(self, tabWidget):
        super(QWidget,self).__init__(tabWidget)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.pushButton = QPushButton("Run Simulation")
        self.saveSimulation = QPushButton("Save Simulation Settings")
        self.grid.addWidget(self.pushButton,0,0)
        self.show()
