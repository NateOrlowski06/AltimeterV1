import bmpsensor

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
        self.altitude = 0.0
        self.velocity = 0.0
        self.max_velocity = 0.0
        self.altitude_readings = [0]*10
        self.initial_altitude = bmpsensor.readBmp180()[2] * METERS_TO_FEET


    def update(self,dt):
        
        self.altitude_readings.append(bmpsensor.readBmp180()[2] * METERS_TO_FEET)

        if (len(self.altitude_readings) > WINDOW_SIZE):
            self.altitude_readings.pop(0)
        
        self.altitude = sum(self.altitude_readings) / len(self.altitude_readings)
        
        

        self.velocity = (self.altitude_readings[-1] - self.altitude_readings[0])  / (dt * WINDOW_SIZE)






        if (self.altitude > self.max_altitude):
            self.max_altitude = self.altitude
        if (self.velocity > self.max_velocity):
            self.max_velocity = self.velocity
    

    
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
