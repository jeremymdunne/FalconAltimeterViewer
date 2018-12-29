from ArduinoCommunicator import ArduinoCommunicator
import time
import sys

"""
Handles encoding and decoding a message
"""

coms = 0
possiblePorts = ["COM4","COM5"]

def requestData(message, checkSumRequired = False):
    #encode the message
    message = "@" + message
    if checkSumRequired:
        message += checksum(message)
    coms.write(message)

def checksum(data):
    storedData = " ".join("{:02X}".format(ord(c)) for c in data)
    splitData = storedData.split()
    hexData = []
    for i in splitData:
        hexData.append(int(i, 16))
    cs = 0
    for x in hexData:
        cs ^= x
    toReturn = "{:02X}".format(cs)
    return toReturn

def getFile():
    coms = ArduinoCommunicator("COM5",115200)
    coms.write("@ST\n")
    print("Command sent")
    recievedConf = False;
    coms.write("@SF:1\n")
    while(recievedConf == False):
        while(coms.available() == False):
            pass
        message = coms.read()
        if "SF" in message:
            print("Confirmation recieved");
            recievedConf = True
        else:
            print(message)
    doneReadingFile = False
    writeFile = open("data.txt","w")
    while(doneReadingFile  == False):
        while(coms.available() == False):
            pass
        message = coms.read();
        if "END" in message:
            print("End of File");
            doneReadingFile = True
        else:
            print(message)
            if "#" in message:
                if "*" in message:
                    start = message.index("#") + 1
                    end = message.index("*")
                    writeFile.write(message[start:end] + "\n");
        #coms.write("ACK\n")
    writeFile.close();

def attemptConnect():
    for i in possiblePorts:
        try:
            coms = ArduinoCommunicator(i,115200)
            return True
        except:
            pass
    return False

def main():
    if attemptConnect() == False:
        print("Unable to connect! Check Connection")
        sys.exit()
    print("Hello, World!")
    #attemptConnect()
    #getFile()

if __name__ == "__main__":
    main()
