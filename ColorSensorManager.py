class ColorSensorManager:
    def __init__(self):
        self.colorSensors = []

    def addColorSensor(self, colorSensor):
        if colorSensor not in self.colorSensors:
            self.colorSensors.append(colorSensor)


    def getColorData(self):
        data = {}

        for colorSensor in self.colorSensors:
            data[colorSensor.location] = colorSensor.getColorData()

        return data