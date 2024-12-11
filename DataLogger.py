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
        while(os.path.exists('data/flight' + str(i) + '.csv')):
            i = i+1

        self.new_file = open('data/flight' + str(i) + '.csv', 'w') #Creates unique file name


        self.csv_writer = csv.writer(self.new_file,delimiter=',') #Creates writer object under the generated file name with comma delimiter
        self.csv_writer.writerow(['Time', 'Altitude','Velocity', 'Acceleration', 'State']) #Writes initial row of titles

   

    def log(self, time, alt, velo, accel, state):
        
        self.csv_writer.writerow([time, alt, velo, accel, state])
        
    def close(self):
        self.new_file.close()

