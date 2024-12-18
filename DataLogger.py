import csv
import os.path
import math

"""
This is where all csv file operations are contained.
Handles the creation, naming, writing and closing of the file.
"""

class DataLogger():
    def __init__(self):
        
        """
        Checks for unique file name upon each time running Main.py
        """
        i = 1
        while(os.path.exists('/home/nate/FlightComputerV1/data/flight' + str(i) + '.csv')):
            i = i+1

        self.new_file = open('/home/nate/FlightComputerV1/data/flight' + str(i) + '.csv', 'w') #Creates unique file name


        self.csv_writer = csv.writer(self.new_file,delimiter=',') #Creates writer object under the generated file name with comma delimiter
        self.csv_writer.writerow(['Time', 'Altitude','Velocity', 'Acceleration', 'State']) #Writes initial row of titles

   

    def log(self, time, alt, velo, accel, state):
        
        self.csv_writer.writerow([time, alt, velo, accel, state])
        
    def close(self):
        self.new_file.close()

    """
    This function logs the maximum flight statistics upon detection of coasting phase.
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
        


