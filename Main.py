import time
from Altimeter import Altimeter
from DataLogger import DataLogger
from Accelerometer import Accelerometer
from StateMachine import StateMachine





def main():

    altimeter = Altimeter()
    data_logger = DataLogger()
    accelerometer = Accelerometer()
    state_machine = StateMachine()

    state_dt = 0.1 #The time interval that the loop runs on
    sensor_dt = 0.01    
    state_update_initial_time = time.time()
    sensor_update_initial_time = time.time()

    #while(str(state_machine.getState()) != "RocketState.LANDED"): This can be implemented once through testing of state machine is finished
    while(True):
        """
        Using this time if statement, the code is executed on exact time intervals without
        halting the main loop. 
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
                                 current_time)
            state_update_initial_time = time.time()


if __name__ == "__main__":
    main()    










