import serial

class ArduinoCommunicator():
    def __init__(self, port, baud = 115200):
        self.ser = serial.Serial(port, baud)

    def available(self):
        if(self.ser.in_waiting >= 1):
            return True
        return False

    def read(self):
        try:
            return self.ser.readline().decode('utf-8')
        except Exception as e:
            print(e)

    def isOpen(self):
        return self.ser.isOpen()

    def write(self, data):
        return self.ser.write(data.encode('utf-8'))

    def close(self):
        self.ser.close()
