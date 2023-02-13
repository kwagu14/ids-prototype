#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import sys

#Publisher code: 

if(len(sys.argv) < 2 or len(sys.argv) > 2):
	print("Wrong number of arguments entered. Correct usage is: python publish.py [topic] [payload]")
	sys.exit(0)

topic = sys.argv[1]
payload = sys.argv[2]

client = mqtt.Client()
client.connect("192.168.122.232", 1883, 60)
client.publish(topic, payload);
client.disconnect();
