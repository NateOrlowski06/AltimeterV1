import bmpsensor
WINDOW_SIZE = 10
class Altimeter():
    def __init__(self):
        self.max_altitude = 0.0
        self.altitude = 0.0
        self.velocity = 0.0
        self.max_velocity = 0.0
        self.altitude_readings = [0]*10



    def update(self,dt):
        
        self.altitude_readings.append(bmpsensor.readBmp180()[2])

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

    def getVelocity(self):
        return self.velocity
    
    def getMaxVelocity(self):
        return self.max_velocity
       
    def getMaxAltitude(self):
        return self.max_altitude
