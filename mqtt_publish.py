#!/usr/bin/env python3

import paho.mqtt.client as mqtt

#Publisher code: 

client = mqtt.Client()
client.connect("192.168.122.232", 1883, 60)
client.publish("topic/test", "Hello world!");
client.disconnect();
