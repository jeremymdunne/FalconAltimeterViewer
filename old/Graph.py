from tkinter import *
import datetime
import math
import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
matplotlib.use('TkAgg')

class Graph():

    def __init__(self, master, xTag = 'Time (s)', yTag = 'Height (m)', numAxis = 1, colors = ['r'], autoScaleY = True, yMinValue = 0, yMaxValue = 1):
        self.master = master
        self.createGraph(xTag, yTag)
        self.numGraphs = numAxis
        self.autoScaleY = autoScaleY
        self.minYvalue = yMinValue
        self.maxYvalue = yMaxValue
        self.points = []
        self.colors = []
        self.numGraphs = 0
        for i in range(0,numAxis):
            self.points.append([])
            self.colors.append(colors[i])

    def addPoint(self, point, axis = 0, graphNow = False):
        #self.points[axis].append(point[0])
        self.points[axis].append(point)
        #check size
        if self.points[axis][-1][0] - self.points[axis][0][0] > 5:
            del self.points[axis][0]
        if(graphNow == True):
            start = datetime.datetime.now()
            self.regraph()
            end = datetime.datetime.now()
            elapsed = end - start
            print("Elapsed Time",0)
            print(elapsed)


    def graph(self,points):
        self.graphingCanvas.delete("all")
        #get min max\
        if(len(points[0]) < 2):
            return

        xMax = points[0][0][0]
        xMin = points[0][0][0]
        yMax = points[0][0][1]
        yMin = points[0][0][1]
        for p in points:
            for x in p:
                if x[0] < xMin:
                    xMin = x[0]
                elif x[0] > xMax:
                    xMax = x[0]
                if x[1] < yMin:
                    yMin = x[1]
                elif x[1] > yMax:
                    yMax = x[1]
        yMax += abs((yMax-yMin)/20)
        yMin += yMin/abs(yMin)*abs((yMax - yMin)/20)
        if(self.autoScaleY == False):
            yMax = self.maxYvalue
            yMin = self.minYvalue
        #print(xMax)
        #print(yMax)
        xScale = 500/(xMax-xMin)
        if(yMax - yMin == 0):
            yScale = 500/(yMax)
        else:
            yScale = 500/(yMax-yMin)
        xMid = (xMax + yMin) / 2
        yMid = (yMax + yMin) / 2
        #draw a grid
        for i in range(0,5):
            #horizontal and vertical
            self.graphingCanvas.create_line(0, 500/5 * i,500,500/5 * i,fill='black')
            self.graphingCanvas.create_text(500/5 * i, 500, anchor=W, font="Purisa",
            text=round((xMin + ((xMax - xMin)/5 * i)),2))
            self.graphingCanvas.create_line(500/5*i, 0, 500/5*i ,500,fill='black')
            self.graphingCanvas.create_text(5, 500/5 * i, anchor=W, font="Purisa",
            text=round((yMax - ((yMax - yMin)/5 * i)),2))

        #print(xScale)
        #print(yScale)
        #print(xMid)
        #print(yMid)
        #don't forget to normalize!
        for type in range(0,len(points)):
            for point in range(0,len(points[type]) - 1):
                #print((points[type][point][0] - xMin) *xScale)
                #print((points[type][point+1][0] - xMin)*xScale)
                #print((points[type][point][1] - yMin) * yScale)
                #print((points[type][point+1][1] - yMin) * yScale)
                #print()

                self.graphingCanvas.create_line((points[type][point][0]-xMin)*xScale, -(points[type][point][1] - yMid)*yScale + 250,(points[type][point+1][0] - xMin)*xScale,-(points[type][point+1][1] - yMid)*yScale + 250, fill=self.colors[type])



    def regraph(self):
        #print(self.points)
        self.graph(self.points)


    def createGraph(self, xTag, yTag):
        self.graphingCanvas = Canvas(self.master,bg='white',width = 600, height = 600);
        self.graphingCanvas.pack(fill=BOTH,expand=True)
        #self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame )
        #self.toolbar.grid(column = 0, row = 2, columnspan=2)
        #self.toolbar.update()
