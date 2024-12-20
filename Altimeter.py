import bmpsensor
import time
"""
This is where the altimeter readings and functions are contained

A moving average is used to mitigate noise in the data

The average velocity is simply calculated by dividing the difference in 
height by the difference in time. 

The maximum height and maximum velocities are evaluated and stored here
"""





METERS_TO_FEET = 3.281
WINDOW_SIZE = 10

class Altimeter():
    def __init__(self):
        self.max_altitude = 0.0
        self.max_velocity = 0.0
        self.max_height = 0.0
        self.altitude = 0.0
        self.velocity = 0.0
        self.previous_altitude = 0.0
        self.altitude_readings = []*WINDOW_SIZE
        self.velocity_calculations = []*WINDOW_SIZE
        self.initial_altitude = bmpsensor.readBmp180()[2] * METERS_TO_FEET


    def update(self,dt):
        
        self.altitude_readings.append(bmpsensor.readBmp180()[2] * METERS_TO_FEET)

        #Purges the earliest value in the window
        if (len(self.altitude_readings) > WINDOW_SIZE):
            self.altitude_readings.pop(0)

        #Sets altitude variable equal to the average altitude over the window
        self.altitude = sum(self.altitude_readings) / len(self.altitude_readings)


        #Creates a moving average for velocity based on the moving average of altitude
        self.velocity_calculations.append((self.altitude - self.previous_altitude) / dt)

        if (len(self.velocity_calculations) > WINDOW_SIZE):
            self.velocity_calculations.pop(0)

        self.velocity = sum(self.velocity_calculations) / len(self.velocity_calculations)


        #Updates all maximum values if necessary
        if (self.altitude > self.max_altitude):
            self.max_altitude = self.altitude
        if (self.velocity > self.max_velocity):
            self.max_velocity = self.velocity
        if (self.getHeight() > self.max_height):
            self.max_height = self.getHeight()

        self.previous_altitude = self.altitude
    

    
    def getAltitude(self):
        return self.altitude
    
    def getHeight(self):
        return self.altitude - self.initial_altitude

    def getVelocity(self):
        return self.velocity
    
    def getMaxVelocity(self):
        return self.max_velocity
       
    def getMaxAltitude(self):
        return self.max_altitude

    def getMaxHeight(self):
        return self.max_height
    
    def setMaxVelocity(self, max_velo):
        self.max_velocity = max_velo

    def setMaxHeight(self, max_h):
        self.max_height = max_h
