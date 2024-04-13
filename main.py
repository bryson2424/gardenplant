from Camera import Camera
from SensorUARTData import Sensor
import cv2

class Main:
    def __init__(self):
        self.plantList = []
        self.cameraList = []

    def setupCameras(self):
        cameraIndices = self.__getAllCameraIndices()

        for cameraIndex in cameraIndices:
            self.cameraList.append(Camera(cameraIndex))



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

print(m.cameraList)


sensor = Sensor("COM3")

data = sensor.getSerialData()

print(data)

