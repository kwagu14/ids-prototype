#!/bin/bash

while [ true ]
do
	app=ir-sensor
	pid=0
	threshold = 0.3

	cd ~/ids-prototype/fingerprinting/New_Mem_Dumps/$(app)/t1
	./../../../memfetch/memfetch $(pid)
	cd ~/ids-prototype/fingerprinting
	similarity = python3 fingerprinting.py Intra $(app)
	
	if [ similarity >= threshold ]
	then
		#Broadcast alert
		python3 ~/ids-prototype/mqtt/mqtt_publish.py "security/alerts" "COMPROMISE"
		#call secure boot
		sh ~/ids-prototype/secure-boot/secure-boot.sh
	fi

done
