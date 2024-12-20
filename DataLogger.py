import csv
import os.path
import math
import os

"""
This is where all csv file operations are contained.
Handles the creation, naming, writing and closing of the file.
"""

class DataLogger():
    def __init__(self):
        
        
        #Creates unique file name upon each time running Main.py
        i = 1
        while(os.path.exists('/home/nate/FlightComputerV1/data/flight' + str(i) + '.csv')):
            i = i+1

        self.new_file = open('/home/nate/FlightComputerV1/data/flight' + str(i) + '.csv', 'w')

        #Creates writer object under the generated file name with comma delimiter
        self.csv_writer = csv.writer(self.new_file,delimiter=',') 
        self.csv_writer.writerow(['Time', 'Altitude','Velocity', 'Acceleration', 'State']) #Writes initial title row

    self.flush_interval = 1
    self.last_flush_time = time.time()

    def log(self, log_time, alt, velo, accel, state):
        self.csv_writer.writerow([log_time, alt, velo, accel, state])
        
        current_time = time.time()
        if current_time - self.last_flush_time >= self.flush_interval:
            self.new_file.flush()
            os.fsync(self.new_file.fileno())
            self.last_flush_time = current_time

    def close(self):
        self.new_file.close()

    """
    This function logs the maximum flight statistics upon detection of coasting state.
    Logs one line into a text file formated like:
    Maximum height: 4000 feet   Maximum Velocity: 500 fps   Maximum Acceleration: 9 G
    """
    def logMaxStats(self, max_height, max_velocity, max_acceleration):
        i = 1
        while(os.path.exists('/home/nate/FlightComputerV1/data/flight' + str(i) + 'stats.txt')):
            i = i+1

        with open('/home/nate/FlightComputerV1/data/flight' + str(i) + 'stats.txt', 'w') as stats_page:
            line = f"Maximum height: {max_height}    Maximum Velocity: {max_velocity}    Maximum Acceleration: {max_acceleration}"

            stats_page.write(line + "\n") 
        


