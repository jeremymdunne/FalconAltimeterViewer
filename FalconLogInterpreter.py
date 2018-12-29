import sys

#data then timestamp



ALTITUDE_DATA_PREFIX = 3
GYRO_DATA_PREFIX = 2
ACCEL_DATA_PREFIX = 1

class FalconLogInterpreter:
    def __init__(self, fileName):
        #try to open the file
        try:
            self.file = open(fileName, "r")
        except Exception as e:
            print("Failed to open the file: " + str(e))
            return -1
        #init everything
        self.altitudeData = []
        self.gyroData = []
        self.accelData = []
        self.launchEvent = []
        self.apogeeEvent = []
        self.readFile(self.file)

    def handleAltitudeData(self,data):
        #we expect 3 members
        if(len(data) != 3):
            print("Altitude data not proper size!")
            return -1;
        #in order: prefix,timestamp,altitude
        newData = [];
        newData.append(float(data[1]))
        newData.append(float(data[2]))
        self.altitudeData.append(newData)

    def handleGyroData(self, data):
        #we expect 3 members
        if(len(data) != 5):
            print("Gyro data not proper size!")
            return -1;
        #in order: prefix,timestamp,altitude
        newData = [];
        newData.append(float(data[1]))
        newData.append(float(data[2]))
        newData.append(float(data[3]))
        newData.append(float(data[4]))
        self.gyroData.append(newData)

    def handleAccelData(self,data):
        #we expect 3 members
        if(len(data) != 5):
            print("Accel data not proper size!")
            return -1;
        #in order: prefix,timestamp,altitude
        newData = [];
        newData.append(float(data[1]))
        newData.append(float(data[2]))
        newData.append(float(data[3]))
        newData.append(float(data[4]))
        self.accelData.append(newData)

    def extractData(self,line):
        shouldContinue = True
        lastEnd = 0;
        nextEnd = 0;
        data=[]
        try:
            safety = line.index("#")
            if safety == 0:
                print("Safety stop")
                return -1;
        except:
            pass;
        while(shouldContinue == True):
            try:
                nextEnd = line.index(",",lastEnd)
            except:
                shouldContinue = False
                nextEnd = len(line)
            data.append(line[lastEnd:nextEnd])
            lastEnd = nextEnd + 1;
        """
        print("Extracted Data: ","")
        for l in data:
            print(" " + str(l) + " ","");
        """
        return data

    """
    Gets the string inbetween the start index and the deliminator, checks if it is an ending delim as well
    """

    def parseLineForData(self, line, deliminator):
        try:
            end = line.index(deliminator)
            return line[0:end]
        except:
            try:
                end = len(line)
                return line[0,end]
            except:
                print("Parsing error")
                return("")

    def parseLine(self, line):
        global ALTITUDE_DATA_PREFIX, GYRO_DATA_PREFIX, ACCEL_DATA_PREFIX
        #look at the first index
        prefix = "#"
        prefix = parseLineForData(line,",")
        if(prefix == ""):
            print("error")
            return -1
        #now go and get the timeStamp
        timeStamp = 0
        #timeStamp =
        #now we're gonna parse it
        #store in the global arrays
        if(int(prefix) == ALTITUDE_DATA_PREFIX):
            #altitude line, now parse it
            #expect 2 extra data
            print("Alt line")
        return 0;


    def readFile(self, file):
        #make sure file opened successfully
        global ALTITUDE_DATA_PREFIX, ACCEL_DATA_PREFIX, GYRO_DATA_PREFIX
        lineNumber = 0;
        for line in file:
            #print("Line: " + str(lineNumber) + ":" + str(line));
            lineNumber += 1;
            data = self.extractData(str(line))
            if data != -1:
                if(int(data[0]) == ALTITUDE_DATA_PREFIX):
                    self.handleAltitudeData(data)

def main():
    print();
    print("Hello, world!");
    if len(sys.argv) < 2:
        print("Usage: program.py file")
        sys.exit(1)
    else:
        print("success")
    file = 0
    interpreter = FalconLogInterpreter(sys.argv[1])
    print(interpreter.altitudeData)

if __name__ == "__main__":
    main()
