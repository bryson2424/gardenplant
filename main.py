from Camera import Camera
from SensorUARTData import Sensor
from ColorSensor import ColorSensor
from ColorSensorManager import ColorSensorManager
#import cv2

class Main:
    def __init__(self):
        self.plantList = []
        self.cameraList = []
        self.colorSensorMan = ColorSensorManager()

    def setupCameras(self):
        cameraIndices = self.__getAllCameraIndices()

        for cameraIndex in cameraIndices:
            self.cameraList.append(Camera(cameraIndex))

    def setupColorSensors(self):
        leftSensor = ColorSensor(location="left")
        middleSensor = ColorSensor(extended=True, extendedI2CValue=3, location="middle")
        rightSensor = ColorSensor(extended=True, extendedI2CValue=4, location="right")

        self.colorSensorMan.addColorSensor(leftSensor)
        self.colorSensorMan.addColorSensor(middleSensor)
        self.colorSensorMan.addColorSensor(rightSensor)

        print(self.colorSensorMan.getColorData())

    def __getAllCameraIndices(self):
        # checks the first 10 indexes.
        index = 0
        arr = []
        i = 31
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
            i -= 1
        return arr

def startup():
    print("Starting robot")

def followTrack():
    pass

def collectSensorData():
    pass


def wait():
    pass

def searchAndCenter():
    pass

def findPlant():
    pass


m = Main()
#m.setupCameras()

#print(m.cameraList)


#sensor = Sensor("COM3")

#data = sensor.getSerialData()

#print(data)

m.setupColorSensors()



