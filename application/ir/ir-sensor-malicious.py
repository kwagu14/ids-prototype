# This script is used in the IOT application environment to mimic the capture of sensor data

# It uses an IR sensor; the code captures data from the sensor and stores in a variable called state
import RPi.GPIO as GPIO
from time import sleep

message = "This is a malicious version of the application, so the similarity score should be different"
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN)
state=1

#store the state of the IR sensor
while True:
	state=GPIO.input(2)
	print(message)
	sleep(0.1)



