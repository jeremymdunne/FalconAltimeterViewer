import tkinter as tk
import sys
import _thread
from tkinter import messagebox
import math
import matplotlib
import numpy as np
from tkinter import filedialog
from interpreter import FalconLogInterpreter
from tkinter import ttk
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
#matplotlib.use('TkAgg')



class SeaofBTCapp(tk.Tk):

    """
    Handles the pages in the GUI
    Pages as follow:
        1. Data Recall/veiwing
        2. Programming
        3. About Page

    this controller handles the threading and actual IO operations
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(side='top', fill='both', expand=True)
        self.mainFrame.grid_rowconfigure(0, weight=1)
        self.mainFrame.grid_columnconfigure(0, weight=1)
        self.frames = {}
        frame = FalconDataViewer(self.mainFrame, self)
        self.frames[FalconDataViewer] = frame
        frame.grid(row=0, column=0, sticky="NSEW")
        self.show_frame(FalconDataViewer)
        #self.openLogFile()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def exitGUI(self):
        sys.exit()

    def showError(self, header, message):
        messagebox.showerror(header,message)

    def connectToFalcon(self):
        #connect to the altimeter and get the log file
        self.showError("Connect To Falcon","TODO")
        #go and grab the file, save it to the local computer, then send it off to be parsed


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


class FalconDataViewer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.initWindow()

    def initWindow(self):
        self.columnconfigure(0,weight=4)
        #master.columnconfigure(1,weight=1)
        #master.columnconfigure(0,weight=1)
        self.graphingFrame = tk.Frame(self)
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
        self.graphCanvas.get_tk_widget().pack(side='bottom', fill='both', expand=True)
        self.graphToolbar = NavigationToolbar2Tk(self.graphCanvas, self.graphingFrame)
        self.graphToolbar.update()
        self.graphCanvas._tkcanvas.pack(side='top', fill='both', expand=True)
        self.graphingFrame.grid(row=0, column=0,padx = 5,pady = 5,sticky='nsew')

        self.optionsFrame = tk.Frame(self)
        self.fileOpenButton = tk.Button(self.optionsFrame, text = "Open Falcon Log", command = self.controller.openLogFile)
        self.connectButton = tk.Button(self.optionsFrame, text = "Connect to Falcon", command = self.controller.connectToFalcon)
        self.fileOpenButton.grid(row=0,column=0)
        self.connectButton.grid(row=1, column=0)
        self.optionsFrame.grid(row=0,column=1,padx = 5)


app = SeaofBTCapp()
app.mainloop()
