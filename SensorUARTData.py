import serial
import time


class Sensor:
    def __init__(self, COM):
        self.COM = COM

    def getSerialData(self):
        try:
            ser = serial.Serial(port=self.COM, baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        except serial.serialutil.SerialException as e:
            print(e)
            print("Failed to connect to serial port", flush=True)
            return

        print("Connected!")

        bmpPressureData = []
        bmpTempData = []
        soilTempData = []
        soilMoistureData = []

        count = 0
        while True:
            if (ser.in_waiting > 0):
                serial_read = ser.readline().strip().decode()
                bmpPressure, bmpTemp, soilTemp, soilMoisture = serial_read.split(',')

                bmpPressureData.append(float(bmpPressure))
                bmpTempData.append(float(bmpTemp))
                soilTempData.append(float(soilTemp))
                soilMoistureData.append(float(soilMoisture))

                print(serial_read)
                """
                pressure, temp = serial_read.split(',')
                pressure = float(pressure) * 0.000987
                pressure = '%.3f' % (pressure)
                print(pressure, temp)
                """
                count += 1

            if count == 5:
                print("Done!")
                return {
                    "bmpPressure": sum(bmpPressureData)/(len(bmpPressureData)),
                    "bmpTemp": sum(bmpTempData) / (len(bmpTempData)),
                    "soilTemp": sum(soilTempData) / (len(soilTempData)),
                    "soilMoisture": sum(soilMoistureData) / (len(soilMoistureData))
                }


