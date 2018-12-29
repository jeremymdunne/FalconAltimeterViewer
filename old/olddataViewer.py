import sys
import _thread
from tkinter import *
from tkinter import messagebox
import math
import matplotlib
import numpy as np
from tkinter import filedialog
#from Graph import Graph
#from HeadlessSerialMonitorGui import HeadlessSerialMonitorGui
#from ArduinoCommunicator import ArduinoCommunicator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
matplotlib.use('TkAgg')
from interpreter import FalconLogInterpreter


class FalconViewer:
    def __init__(self, master, argv):
        self.master = master
        self.initWindow()
        #variable init
        self.altitudeData = []
        self.gyroData = []
        self.accelData = []
        self.gpsData = []
        self.velocityEvent = []
        self.launchEvent = 0
        self.boostEvent = 0
        self.apogeeEvent = 0
        self.drogueEvent = 0
        self.mainChuteEvent = 0
        self.landingEvent = 0
        self.handleArgs(argv)
        #self.showError("Hello","Hello World!")

    def initWindow(self):
                self.master.columnconfigure(0,weight=4)
                #master.columnconfigure(1,weight=1)
                #master.columnconfigure(0,weight=1)
                self.graphingFrame = Frame(self.master)
                self.graphingFigure = Figure(figsize=(9,9), dpi=100)
                self.altitudeGraph = self.graphingFigure.add_subplot(111)

                self.altitudeGraph.grid(True)
                #self.graphingFrame.title("")
                #self.altitudeGraph = self.graphingFigure.add_axes( (0.05, .05, .90, .90), frameon=False)
                #self.graphingFigure.set_xlabel("Time")
                #self.graphingFigure.set_ylabel("Altitude")
                #self.altitudeGraph.grid(color='black',linestyle='-', linewidth=2)
                #configure the fraphs
                self.graphCanvas = FigureCanvasTkAgg(self.graphingFigure, self.graphingFrame)
                self.graphCanvas.draw()
                self.graphCanvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
                self.graphToolbar = NavigationToolbar2Tk(self.graphCanvas, self.graphingFrame)
                self.graphToolbar.update()
                self.graphCanvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
                self.graphingFrame.grid(row=0, column=0,padx = 5,pady = 5,sticky=N+W+E+S)

                self.optionsFrame = Frame(self.master)
                self.fileOpenButton = Button(self.optionsFrame, text = "Open Falcon Log", command = self.openLogFile)
                self.connectButton = Button(self.optionsFrame, text = "Connect to Falcon", command = self.connectToFalcon)
                self.fileOpenButton.grid(row=0,column=0)
                self.connectButton.grid(row=1, column=0)
                self.optionsFrame.grid(row=0,column=1,padx = 5)

                menu = Menu(self.master)
                self.master.config(menu=menu)

                # create the file object)
                file = Menu(menu)

                # adds a command to the menu option, calling it exit, and the
                # command it runs on event is client_exit
                file.add_command(label="Exit", command=self.exitGUI)

                #added "file" to our menu
                menu.add_cascade(label="File", menu=file)

                # create the file object)
                edit = Menu(menu)

                # adds a command to the menu option, calling it exit, and the
                # command it runs on event is client_exit
                edit.add_command(label="Undo")

                #added "file" to our menu
                menu.add_cascade(label="Edit", menu=edit)



    def showError(self, header, message):
        messagebox.showerror(header,message)

    def exitGUI(self):
        sys.exit()

    def handleArgs(self, argv):
        #handles any args given
        for i in range(1,len(argv)):
            flag = 0
            try:
                index = argv[i].index("-")
                #get the type
                end = -1
                try:
                    end = argv.index(" ",index + 1)
                except:
                    pass

                if end >= 0:
                    flag = argv[i][index+1:end]
                else:
                    flag = argv[i][index+1:len(argv[i])]
            except:
                pass
            if flag == "l":
                #open this log file
                #get the file name
                name = argv[i+1]
                i += 1
                self.openLogFile(name)

    def openLogFile(self, name = ""):
        #open and parse the file to display contents
        if name == "":
            name =  filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
            print(name)
        try:
            self.interpreter = FalconLogInterpreter(name)
        except:
            self.showError("File Open","Failed to open or parse!")
            return
        #go and grabe the datas
        self.altitudeData = self.interpreter.altitudeData;
        self.gyroData = self.interpreter.gyroData;
        self.accelData = self.interpreter.accelData;
        #lets go graph!
        self.updateGraphs()

    def updateGraphs(self):
        self.altitudeGraph.clear()
        time = [];
        altitude = [];
        for alt in self.altitudeData:
            time.append(alt[0]/1000)
            altitude.append(alt[1])
        self.altitudeGraph.plot(time,altitude,label='Alt Data', color='r')
        self.altitudeGraph.legend(loc = 'upper left')
        self.altitudeGraph.grid(True)
        self.graphCanvas.draw()
        self.graphToolbar.update()

    def connectToFalcon(self):
        #connect to the altimeter and get the log file
        self.showError("Connect To Falcon","TODO")
        #go and grab the file, save it to the local computer, then send it off to be parsed

class GuiController:
    def __init__(self, *argsv):
        self.root = Tk()
        self.root.title("Falcon Altimeter Visualizer")
        self.mainFrame = Frame()
        self.mainFrame.pack(side='top',fill='both',expand = True)
        self.mainFrame.grid_configure(0,weight=1)
        self.mainFrame.row_configure(0,weight=1)
        self.frames = {}
        frame = FalconViewer(self.mainFrame)

    def show(self, toShow):
        frame = self.frames[toShow]
        frame.tkraise()


def main():
    root = Tk()
    root.title("Falcon Altimeter Visualizer")
    gui = FalconViewer(root, sys.argv)
    root.mainloop()

if __name__ == "__main__":
    main()
