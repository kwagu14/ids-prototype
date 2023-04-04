#!/bin/bash

#initialize values
app="ir-sensor"
cid=$(docker container ls --all --quiet --no-trunc --filter "name=appEnv")
pid=$(docker inspect -f '{{.State.Pid}}' $(cid))
threshold = 190000

while [ true ]
do
	
	#go into the t1 dir; last good fingerprint in t0
	cd ~/ids-prototype/fingerprinting/New_Mem_Dumps/$(app)/t1
	#get a memory dump of the iot process into t1
	./../../../memfetch/memfetch $(pid)
	#go into fingerprinting dir
	cd ~/ids-prototype/fingerprinting
	#run the fingerprinting script
	python3 fingerprinting.py Intra $(app)
	#get the similarity score
	similarity=$(cat similarity.txt)
	
	if [ similarity > threshold ]
	then
		#Broadcast alert in network
		python3 ~/ids-prototype/mqtt/mqtt_publish.py "security/alerts" "COMPROMISE"
		#call secure boot
		sh ~/ids-prototype/secure-boot/secure-boot.sh
		#at this point, we have a clean instance; need to update cid, pid, and t0
		cid=$(docker container ls --all --quiet --no-trunc --filter "name=appEnv")
		pid=$(docker inspect -f '{{.State.Pid}}' $(cid))
		#remove old t0
		cd ~/ids-prototype/fingerprinting/New_Mem_Dumps/$(app)
		rm -r t0
		#make new t0 and get fresh mem dump
		mkdir t0
		cd t0
		./../../../memfetch/memfetch $(pid)
		cd ..
		#remove old t1
		rm -r t1
		#create new, empty t1
		mkdir t1
	else
		#remove t0
		cd ~/ids-prototype/fingerprinting/New_Mem_Dumps/$(app)
		rm -r t0
		#make old t1 new t0
		mv t1 t0
		#create a new, empty t1
		mkdir t1
	fi

done
