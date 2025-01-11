from enum import Enum, auto

"""
States are evaluated, updated, and handled here.
Data is logged during mid-air flight states
Five states; STANDBY, BOOST, COAST, FREEFALL, and LANDED 
are updated based on sensor data passed through the update() funciton
called in the main loop.
The if statement logic creates a way to only move forward in the states
and allows for simpler logic between state changes. 
"""

class RocketState(Enum):
    STANDBY = auto()
    BOOST = auto()
    COAST = auto()
    FREEFALL = auto()
    LANDED = auto()
    
class StateMachine():
    def __init__(self):
        self.state = RocketState.STANDBY
        self.start_time = 0

    def update(self,
               altimeter,
               accelerometer,
               logger,
               seconds):
        
        if(self.state == RocketState.STANDBY):
            
            #Nothing to do in standby
            #Switches to boost state if acceleration is bigger than 0.25 Gs roughly 3 m/s/s
            if (accelerometer.getAcceleration() > 0.25): 
                self.state = RocketState.BOOST
                self.start_time = seconds
                altimeter.setMaxHeight(0)
                altimeter.setMaxVelocity(0) 
                """
                Since velocity is calulated based on difference in altitude, sometimes when the data jumps around
                there is a high calcuated velocity on the pad. Therefore, the max velocity variable is reset upon detection
                of takeoff because it is known the velocity was not at a local maximum on the pad. 
                """


        elif(self.state == RocketState.BOOST):
            
            logger.log(seconds - self.start_time, 
                       altimeter.getHeight(), 
                       altimeter.getVelocity(), 
                       accelerometer.getAcceleration(), 
                       self.state)

            #Coasting starts after velocity reaches maximum
            if(altimeter.getVelocity()< 0.9 * altimeter.getMaxVelocity()):
                self.state = RocketState.COAST

                """
                If there is a bump to the rocket on the pad, the accelerometer will detect
                takeoff but then instantly detect the ending of boost stage. 
                Therefore, if there is an instant detection of boost ending, i.e. under 10 feet AGL, 
                then we will assume this was a faulty state change and return to standby
                """
                if(altimeter.getAltitude()<10):
                    self.state = RocketState.STANDBY


        elif(self.state == RocketState.COAST):

            logger.log(seconds - self.start_time, 
                       altimeter.getHeight(), 
                       altimeter.getVelocity(), 
                       accelerometer.getAcceleration(), 
                       self.state)

            #Apoggee occurs after the altitude drops significantly below the maximum
            if (altimeter.getAltitude() + 5 < altimeter.getMaxAltitude()):
                self.state = RocketState.FREEFALL
                logger.logMaxStats(altimeter.getMaxHeight(), altimeter.getMaxVelocity(), accelerometer.getMaxAcceleration())


        elif(self.state == RocketState.FREEFALL):

            logger.log(seconds - self.start_time, 
                       altimeter.getHeight(), 
                       altimeter.getVelocity(), 
                       accelerometer.getAcceleration(), 
                       self.state)
            
            if(accelerometer.getAcceleration()<=0.1 and altimeter.getAltitude()<10):
                self.state = RocketState.LANDED


        elif(self.state == RocketState.LANDED):
            
            logger.log(seconds - self.start_time, 
                       altimeter.getHeight(), 
                       altimeter.getVelocity(), 
                       accelerometer.getAcceleration(), 
                       self.state)
            logger.close()
            

    def getState(self):
        return self.state




"""
Condition for coast -> freefall 
Freefall starts when height < maxheight
From BMP180 Datasheet, the maximum noise is +/- 0.06 hPa which corelates to +/- 1.66 feet at 5000 ft ASL
Formula: Altutude = 44330*(1-(p-p0)^0.1903) meters. 0 meters ASL is 1013.25 hPa
Therefore, altitude plus double the deviation must be less than the recorded max altitude to detect apogee
This would result in 3.32 feet but I am choosing 5 feet for a larger in case of spikes in boost phase.
"""
