#!/usr/bin/env python3

import paho.mqtt.client as mqtt

#subscriber code:

def on_connect(client, userdata, flags, rc): 
	print("Connected with result code "+str(rc))
	client.subscribe("topic/test")

def on_message(client, userdata, msg): 
	if msg.payload.decode() == "Hello world!":
		print("Received payload: Hello world!")
		client.disconnect()

client = mqtt.Client()
client.connect("192.168.122.232", 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
