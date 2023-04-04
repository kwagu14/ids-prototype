# This script is used in the IOT application environment to mimic the capture of sensor data

# It uses an IR sensor; the code captures data from the sensor and stores 100 data points in 
# memory at a timee

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN)

data_list = []

#store the first 100 data values inside of the buffer
for x in range(0, 101):
	data_list.append(GPIO.input(2))
	sleep(0.1)

#then for successive values, pop a value and add the new one
while True:
	data_list.pop(0)
	data_list.append(GPIO.input(2))
	sleep(0.1)



