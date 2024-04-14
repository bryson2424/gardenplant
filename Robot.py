class Robot:
    def __init__(self, colorSensorMan):
        self.colorSensorMan = colorSensorMan

    def followLine(self):
        count = 0
        while True:
            data = self.colorSensorMan.getColorData()

            # (R, G, B)
            leftRGB = data["left"]
            middleRGB = data["middle"]
            rightRGB = data["right"]

            # If we see red
            if middleRGB[0] > 60 :
                #Color found
                return True, "red"

            # main line is green
            if middleRGB[1] > 60:
                # currently seeing green
                self.moveForward()
            elif leftRGB[1] > 60:
                # skewing right a bit, move left
                self.turnLeft(10)
            elif rightRGB[1] > 60:
                # skewing left a bit, move right
                self.turnRight(10)

            if count >= 1000000:
                print("Exceeded count. Stopping")
                return False, None

    def moveForward(self):
        pass

    def moveBackward(self):
        pass

    def turnLeft(self, degrees):
        pass

    def turnRight(self, degrees):
        pass

    def stop(self):
        # Stop all movement
        pass