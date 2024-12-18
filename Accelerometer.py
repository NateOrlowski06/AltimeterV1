import board
import adafruit_bno055
import math


"""
This is where the accelerometer data is read and processed.
The BNO055 returns a tuple containing an x, y, and z acceleration reading
For the state machine purposes, we only care about the magnitude of the acceleration vector

A moving average is used to mitigate noise in the data

Sometimes the BNO055 returns a non float value and triggers an error if
math operations are attempted. A try/except block in the update function
catches those and replaces them with the most recent data point. 
"""



WINDOW_SIZE = 10
class Accelerometer():

    def __init__(self):
        self.i2c = board.I2C()
        self.sensor = adafruit_bno055.BNO055_I2C(self.i2c)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.acceleration = 0.0
        self.acceleration_readings = [0.0]
        self.max_acceleration = 0.0

    def update(self):
        
        self.x = self.sensor.linear_acceleration[0]
        self.y = self.sensor.linear_acceleration[1]
        self.z = self.sensor.linear_acceleration[2]
        if len(self.acceleration_readings)>WINDOW_SIZE:
            self.acceleration_readings.pop(0)
            self.acceleration = sum(self.acceleration_readings) / len(self.acceleration_readings) 

        try: #subtract 0.5 from the acceleration because the sensor reads roughly 0.5 sitting still
            self.acceleration_readings.append(math.sqrt(self.x**2 + self.y**2 + self.z**2)-0.5)
        except (TypeError, ValueError):
            self.acceleration_readings.append(self.acceleration_readings[-1])
        
        if self.acceleration > self.max_acceleration :
            self.max_acceleration = self.acceleration

        
    def getAcceleration(self):
        return self.acceleration

    def getMaxAcceleration(self):
        return self.max_acceleration

