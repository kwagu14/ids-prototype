#!/usr/bin/env python

import RPi.GPIO as GPIO  #GPIO has all functions needed to interact with GPIO pins 
from mfrc522 import SimpleMFRC522 #will enable communication with RFID RC522

reader = SimpleMFRC522() #creates a copy  of the SimpleMFRC522 as an object, runs its setup function, then stores it in reader variable

try:
    text = input('New data:')
    print("Place your tag to write")
    reader.write(text)
    print("Written!")
    
finally:
    GPIO.cleanup() #exit script
          
