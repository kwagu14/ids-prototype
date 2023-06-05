#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import sys

#Publisher code: 

if(len(sys.argv) < 3 or len(sys.argv) > 3):
	print("Wrong number of arguments entered. Correct usage is: python publish.py [topic] [payload]")
	sys.exit(0)

topic = sys.argv[1]
payload = sys.argv[2]

client = mqtt.Client()
client.connect("192.168.33.98", 1883, 60)
print("[FROM MQTT_PUBLISH] sending payload " + payload + " under topic " + topic + " to broker.")
client.publish(topic, payload);
client.disconnect();
