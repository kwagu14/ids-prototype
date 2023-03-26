#!/bin/bash

while [ true ]
do
	app=ir-sensor
	pid=0
	threshold = 0.3

	cd /home/karleywa/ids-prototype/fingerprinting/New_Mem_Dumps/$(app)/t1
	./../../../memfetch/memfetch $(pid)
	cd /home/karleywa/ids-prototype/fingerprinting
	similarity = python3 fingerprinting.py Intra $(app)
	
	if [ similarity >= threshold ]
	then
		#Broadcast alert
		
		#call secure boot
		sh /home/karleywa/ids-prototype/secure-boot/secure-boot.sh
	fi

done
