import sys
import time
from threading import Thread
from PyQt5.QtWidgets import QWidget, QDesktopWidget,QLabel,QLayout, QLineEdit, QFileDialog, QMessageBox, QApplication, QPushButton, QGridLayout, QTabWidget, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
import pyqtgraph as pg
from FalconLogInterpreter import FalconLogInterpreter
from FlightLogSimulation import FlightLogSimulation
from DataViewer import DataViewer
from Programmer import Programmer
from SimulateFlight import SimulateFlight
from ParabolicKinematicEngine import ParabolicKinematicEngine

class FalconCommunicator():

    def __init__(self):
        pass

    def initComs(self, port):
        pass

    def program(self):
        pass

    #get the data, save to file
    def getFile(self, index, locToSave, callback):
        pass

    def getFileTable(self, callback):
        pass 

class Controller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.connectedToFalcon = False
        self.openedFile = False


    def initUI(self):

        """
        Main UI Layout:
        Menu bars to open a file, connect to the falcon, etc.
        tabs for the main windows:
            Data Veiwer
            Programmer
            About
        Status bar in the bottom left telling info
        """
        self.initMenu()

        #self.setGeometry(600, 600, 300, 200)
        self.setWindowTitle('Simple menu')
        self.tabs = QTabWidget()
    #    self.tabs.resize(500,500)
        self.dataViewerTab = DataViewer(self, lambda: self.openLogFile(), lambda: self.connectToFalcon())
        self.programmingTab = Programmer(self)
        self.logSimulationTab = FlightLogSimulation(self, lambda: self.simulateFlightFromLog(), lambda: self.openLogFile(), lambda: self.connectToFalcon())
        self.flightSimulationTab = SimulateFlight(self, lambda: self.runFlightSimulation(), lambda: self.pause(), lambda: self.resume())
        self.tabs.addTab(self.dataViewerTab,"Veiw Data")
        self.tabs.addTab(self.logSimulationTab,"Flight Log Simulation")
        self.tabs.addTab(self.programmingTab,"Program")
        self.tabs.addTab(self.flightSimulationTab, "Simulate Flight")
        self.setCentralWidget(self.tabs)
        self.showMaximized()
        self.show()

    def initMenu(self):
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        openFileAct = QAction(QIcon('open.png'), '&Open',self)
        openFileAct.setShortcut('Ctrl+O')
        openFileAct.setStatusTip('Open Log File')
        openFileAct.triggered.connect(self.openLogFile)

        connectAct = QAction(QIcon('connect.png'), '&Connect',self)
        connectAct.setShortcut('Ctrl+F')
        connectAct.setStatusTip('Connect to Altimeter to get Logs')
        connectAct.triggered.connect(self.connectToFalcon)


        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        fileMenu.addAction(openFileAct)
        fileMenu.addAction(connectAct)

    def pause(self):
        self.reportError(title="Pause", bodytext="TODO")

    def resume(self):
        self.reportError(title="Resume", bodytext="TODO")


    def runFlightSimulation(self):
        #go generate the parabolic flight
        thread = Thread(target=self.flightSimulationThread).start()
        #self.reportError(title="Not Yet Supported", bodytext="TODO")

    def flightSimulationThread(self):
        try:
            p = ParabolicKinematicEngine(0,9.9,.01)
            print(self.flightSimulationTab.dryMassInput.text())
            data = p.compute(float(self.flightSimulationTab.startAltitudeInput.text()),float(self.flightSimulationTab.dryMassInput.text()),float(self.flightSimulationTab.fuelWeightInput.text()),float(self.flightSimulationTab.averageThrustInput.text()),float(self.flightSimulationTab.burnDurationInput.text()),.5,.1)
            self.flightSimulationTab.graphSimulatedFlight(None, data)
            traveled = []
            path = data
            for i in range(0,int(len(data)/10)):
                time.sleep(.1)
                for i in range(0,10):
                    traveled.append(path[0])
                    del path[0]
                self.flightSimulationTab.graphSimulatedFlight(traveled, path)
                QApplication.processEvents()
        except Exception as e:
            print(e)

    def simulateFlightFromLog(self):
        if self.openedFile == False:
            self.reportError(title="No File Opened", bodytext="Please open a log or connect to the altimeter")
        self.reportError(title="Not Yet Supported", bodytext="TODO")

    def openLogFile(self):
        #fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        name = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Log Files (*.txt);;All Files (*)")[0]
        print(name)
        if name is None or name == '':
            return
        try:
            self.interpreter = FalconLogInterpreter(name)
        except Exception as e:
            self.reportError(title="File Open",bodytext="Failed to open or parse!")
            print(e)
            return
        #go and grabe the datas
        self.altitudeData = self.interpreter.altitudeData;
        self.gyroData = self.interpreter.gyroData;
        self.accelData = self.interpreter.accelData;
        self.dataViewerTab.graph(self.altitudeData)
        self.openedFile = True

    def connectToFalcon(self):
        self.reportError('TODO')

    def reportError(self, type=None, title = "", bodytext=""):
        msg = QMessageBox()
        if(type==None):
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle(title)
            msg.setText(bodytext)
        else:
            if type == 'TODO':
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("TODO")
                msg.setText("Not Yet Implemented")
            elif type == 'GENERAL':
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error")
                msg.setText("Critical")
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Controller()
    sys.exit(app.exec_())
