#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import sys

#subscriber code:

#check command line arguments before doing anything else

if(len(sys.argv) > 2 or len(sys.argv) < 2):
	print("Wrong number of arguments entered. Correct usage is: python mqtt_subscribe.py [topic]")
	sys.exit(0)

topic = sys.argv[1]

def on_connect(client, userdata, flags, rc): 
	print("Connected with result code "+str(rc))
	client.subscribe(topic)

def on_message(client, userdata, msg): 
	result = msg.payload.decode()
	print("Received payload from topic", topic, ": ", result)

client = mqtt.Client()
client.connect("192.168.122.232", 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
