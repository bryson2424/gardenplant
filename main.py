from Camera import camThread
from SensorUARTData import Sensor
from ColorSensor import ColorSensor
from ColorSensorManager import ColorSensorManager
from Robot import Robot
from IoTConnection import IoTConnection
from Plant import Plant
import cv2

class Main:
    def __init__(self):
        self.plantList = []
        self.cameraList = []
        self.colorSensorMan = ColorSensorManager()
        self.robot = None

        self.sensor = Sensor("/dev/ttyACM0")

        self.IoTConn = IoTConnection()


    def setupCameras(self):
        cameraIndices = self.__getAllCameraIndices()

        for cameraIndex in cameraIndices:
            self.cameraList.append(camThread(camID=cameraIndex))

    def setupColorSensors(self):
        leftSensor = ColorSensor(location="left")
        middleSensor = ColorSensor(extended=True, extendedI2CValue=3, location="middle")
        rightSensor = ColorSensor(extended=True, extendedI2CValue=4, location="right")

        self.colorSensorMan.addColorSensor(leftSensor)
        self.colorSensorMan.addColorSensor(middleSensor)
        self.colorSensorMan.addColorSensor(rightSensor)

        print(self.colorSensorMan.getColorData())

    def setupRobot(self):
        self.robot = Robot(self.colorSensorMan)

    def followUntilPointOfInterest(self):
        POIfound, color = self.robot.followLine()

        if POIfound:
            if color == "red":
                print("Red found")
                self.robot.turnLeft(90)
                self.followUntilPlantReached()

    def followUntilPlantReached(self):
        POIfound, color = self.robot.followLine()

        if POIfound:
            if color == "blue":
                print("Blue found")
                self.robot.stop()
                self.collectData()

    def collectData(self):
        self.robot.insertSoilSensor()

        sensorData = self.sensor.getSerialData()

        for camera in self.cameraList:
            # Only grabs from one camera atm
            im_b64 = camera.baes64Image

        # Doesn't identify plants atm
        # identifyPlant
        plant = Plant(name="Plant0")
        self.IoTConn.createFeed(plant)

        data = {"base64Image": im_b64, "temp": sensorData["bmpTemp"], "moisture": "soilMoisture"}

        self.IoTConn.uploadData(plant, data)

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


#print(data)

m.setupColorSensors()


