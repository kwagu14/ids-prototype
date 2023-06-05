'''
This RFID detector code reads the data from RFID tags or cards and alerts the user with an email notification.
'''


import time
import RPi.GPIO as GPIO  #GPIO has all functions needed to interact with GPIO pins 
from mfrc522 import SimpleMFRC522 #will enable communication with RFID RC522
import smtplib
from datetime import datetime
from time import sleep


reader = SimpleMFRC522() #creates a copy  of the SimpleMFRC522 as an object, runs its setup function, then stores it in reader variable

while True:
    reader = SimpleMFRC522()
    print("Place your RFID card near the reader.")
    id,text = reader.read()
    print(id)
    print(text)
    new_id = str(id)
    print("Read RFID complete.")
    sleep(2)    
