#!/usr/bin/env python3

#this script can subscribe to certain MQTT topics 
#once subscribed, they will receive all payloads broadcast under that topic

#usage: 
#    python3 mqtt_subscribe [topic]

import paho.mqtt.client as mqtt
import sys
import os

source = "[FROM MQTT_SUBSCRIBE] "

#check command line arguments before doing anything else

if(len(sys.argv) > 2 or len(sys.argv) < 2):
	print(source + " Wrong number of arguments entered. Correct usage is: python mqtt_subscribe.py [topic]")
	sys.exit(0)

topic = sys.argv[1]

def on_connect(client, userdata, flags, rc): 
	print(source + " Connected to control server with result code "+str(rc))
	client.subscribe(topic)

def on_message(client, userdata, msg): 
	result = msg.payload.decode()
	print(source + " Received payload from topic", topic, ": ", result)
	if topic == "security/alerts" and result == "COMPROMISE":
		print(source + " Compromise detected; Beginning secure boot process")
		os.system('sh /ids-prototype/secureboot/secure-boot.sh')
		print(source + " Finished boot process")

client = mqtt.Client()
client.connect("192.168.33.98", 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
