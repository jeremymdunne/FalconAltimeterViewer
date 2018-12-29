from PyQt5.QtWidgets import QWidget, QDesktopWidget,QLabel,QLayout, QLineEdit, QFileDialog, QMessageBox, QApplication, QPushButton, QGridLayout, QTabWidget, QMainWindow, QAction, qApp
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyqtgraph as pg

class SimulateFlight(QWidget):
    def __init__(self, tabWidget, simulateCallback, pauseCallback, resumeCallback):
        super(QWidget,self).__init__(tabWidget)
        self.pauseCallback = pauseCallback
        self.resumeCallback = resumeCallback
        self.callback = simulateCallback
        self.mainPlot = pg.PlotWidget()
        self.mainPlot.enableAutoRange()
        self.mainPlot.setLabel('left','Altitude',units = 'm')
        self.mainPlot.setLabel('bottom','Time',units = 'sec')
        #self.mainPlot.addLegend()
        self.optionsPane = QWidget(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.setColumnStretch(0,4)
        self.grid.setColumnStretch(1,1)
        self.grid.setRowStretch(0,4)
        self.grid.setRowStretch(1,1)
        self.grid.addWidget(self.mainPlot,0,0)
        self.grid.addWidget(self.optionsPane,0,1)
        self.initOptionsPane()
        #self.initSimulationStats()
        self.curve1 = self.mainPlot.plot()
        self.curve2 = self.mainPlot.plot()
        self.show()

    def graphSimulatedFlight(self, traveledPath, pathToTravel):
        #go open up the file for now
        #self.mainPlot.legend.items = []
        x1 = []
        y1 = []
        x2 = []
        y2 = []
        if traveledPath is not None:
            for a in traveledPath:
                x1.append(a[0])
                y1.append(a[1])
        if pathToTravel is not None:
            for a in pathToTravel:
                x2.append(a[0])
                y2.append(a[1])
        self.curve1.setData(x1,y1,pen='r')
        self.curve2.setData(x2,y2,pen='g',name='Path')

    def initOptionsPane(self):
        self.optionsGrid = QGridLayout()
        self.optionsGrid.setAlignment(Qt.AlignTop)
        self.optionsPane.setLayout(self.optionsGrid)
        self.runBtn = QPushButton("Run",self.optionsPane)
        self.pauseBtn = QPushButton("Pause",self.optionsPane)
        self.resumeBtn = QPushButton("Resume",self.optionsPane)
        self.runBtn.clicked.connect(self.callback)
        self.pauseBtn.clicked.connect(self.pauseCallback)
        self.resumeBtn.clicked.connect(self.resumeCallback)

        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        #self.optionsGrid.addWidget(self.runBtn, 8,0)
        rocketCharacteristics = QLabel("Rocket Characteristics")
        dryMass = QLabel("Rocket Dry Mass (Kg):")
        fuelWeight = QLabel("Propellant Mass (Kg):")
        averageThrust = QLabel("Average Thrust (N):")
        burnDuration = QLabel("Burn Duration (sec)")

        sensorCharacteristics = QLabel("Sensor Characterisitcs")
        startAltitude = QLabel("Starting Altitude")
        altitudeNoise = QLabel("Altitude Noise (m)")

        self.dryMassInput = QLineEdit('1')
        self.fuelWeightInput = QLineEdit('.1')
        self.averageThrustInput = QLineEdit('100')
        self.burnDurationInput = QLineEdit('1')
        self.startAltitudeInput = QLineEdit('1')
        self.altitudeNoiseInput = QLineEdit('1')
        self.optionsGrid.addWidget(rocketCharacteristics,0,0)
        self.optionsGrid.addWidget(dryMass, 1,0)
        self.optionsGrid.addWidget(self.dryMassInput, 1,1)
        self.optionsGrid.addWidget(fuelWeight, 2,0)
        self.optionsGrid.addWidget(self.fuelWeightInput,2,1)
        self.optionsGrid.addWidget(averageThrust,3,0)
        self.optionsGrid.addWidget(self.averageThrustInput,3,1)
        self.optionsGrid.addWidget(burnDuration,4,0)
        self.optionsGrid.addWidget(self.burnDurationInput,4,1)


        self.optionsGrid.addItem(verticalSpacer,5,0)
        self.optionsGrid.addWidget(sensorCharacteristics,6,0)
        self.optionsGrid.addWidget(startAltitude, 7,0)
        self.optionsGrid.addWidget(self.startAltitudeInput,7,1)
        self.optionsGrid.addWidget(altitudeNoise,8,0)
        self.optionsGrid.addWidget(self.altitudeNoiseInput,8,1)
        self.optionsGrid.addItem(verticalSpacer,9,0)
        self.optionsGrid.addWidget(self.runBtn, 10,0,1,2)
        self.optionsGrid.addWidget(self.pauseBtn, 11,0)
        self.optionsGrid.addWidget(self.resumeBtn, 11, 1)
        self.optionsGrid.addItem(verticalSpacer,12,0)




    def handleSimulateButton(self):
        self.callback()
