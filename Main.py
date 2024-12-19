import time
from Altimeter import Altimeter
from DataLogger import DataLogger
from Accelerometer import Accelerometer
from StateMachine import StateMachine

"""
This is where the sensors are initialized, the main loop runs, 
and where the timing of events is handled
"""

def main():

    altimeter = Altimeter()
    data_logger = DataLogger()
    accelerometer = Accelerometer()
    state_machine = StateMachine()

    state_dt = 0.1 #The time interval that the state is updated
    sensor_dt = 0.04 #Time interval that sensors are updated based on max polling rate for BMP180
    
    state_update_initial_time = time.time()
    sensor_update_initial_time = time.time()
   


    #while(str(state_machine.getState()) != "RocketState.LANDED"): This can be implemented once throrough testing of state changing is finished
    while(True):
        """
        The sensors are updated 10 times as fast as the state is checked. 
        The data is added to a moving average that is 10 datapoints wide that is updated every sensor_dt
        The state is checked every state_dt and data is logged 
        """

        current_time = time.time()
        
        if(current_time - sensor_update_initial_time >= sensor_dt):
            altimeter.update(sensor_dt) 
            accelerometer.update()
            sensor_update_initial_time = time.time()

        if(current_time - state_update_initial_time >= state_dt):
            state_machine.update(altimeter.getAltitude(), 
                                 accelerometer.getAcceleration(), 
                                 altimeter.getMaxAltitude(), 
                                 data_logger, 
                                 altimeter.getVelocity(),
                                 altimeter.getMaxVelocity(),
                                 current_time,
                                 altimeter.getHeight(),
                                 accelerometer.getMaxAcceleration(),
                                 altimeter.getMaxHeight())
            state_update_initial_time = time.time()
            print(altimeter.getAltitude())
if __name__ == "__main__":
    main()    











