import time
import board
import adafruit_tcs34725
from adafruit_extended_bus import ExtendedI2C as I2C


class ColorSensor:
    def __init__(self, extended=False, extendedI2CValue=None, location=None):
        if (extended) and (extendedI2CValue is not None):
            self.i2c = I2C(extendedI2CValue)
        else:
            self.i2c = board.I2C()
            print(self.i2c)

        self.sensor = adafruit_tcs34725.TCS34725(self.i2c)

        self.sensor.gain = 16

        self.location = location

    def getColorData(self):
        color_rgb = self.sensor.color_rgb_bytes

        return(color_rgb)