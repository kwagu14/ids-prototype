#!/bin/bash

#subscribe to alerts topic
python3 /ids-prototype/mqtt/mqtt_subscribe.py "security/alerts" &

#initialize values
app="ir-sensor"
cid=$(docker container ls --all --quiet --no-trunc --filter "name=appEnv")
pid=$(docker inspect -f '{{.State.Pid}}' $cid)
threshold=190000
echo "[FROM MEM-FORENSICS] cid and pid initialized"

#initialize t0 with a clean memdump
cd /ids-prototype/fingerprinting/New_Mem_Dumps/$app/t0/bin
./../../../../memfetch/memfetch $pid
echo "[FROM MEM-FORENSICS] t0 mem dump initialized"
 
while [ true ]
do
	#go into the t1 dir; last good fingerprint in t0
	cd /ids-prototype/fingerprinting/New_Mem_Dumps/$app/t1/bin
	#get a memory dump of the iot process into t1
	./../../../../memfetch/memfetch $pid
	echo "[FROM MEM-FORENSICS] finished getting mem dump for t1"
	#go into fingerprinting dir
	cd /ids-prototype/fingerprinting
	#run the fingerprinting script
	echo "[FROM MEM-FORENSICS] running fingerprinting script"
	python3 fingerprinting.py Intra $app
	#get the similarity score
	#similarity=191000
	similarity=$(cat similarity.txt)
	echo "[FROM MEM-FORENSICS] got the similarity score"
	
	if [ $similarity -gt $threshold ]
	then
		echo "[FROM MEM-FORENSICS] similarity found to be greater than threshold; beginning secure boot"
		echo "[FROM MEM-FORENSICS] Broadcasting alert to other devices"
		#Broadcast alert in network
		python3 /ids-prototype/mqtt/mqtt_publish.py "security/alerts" "COMPROMISE"
		#call secure boot
		echo "[FROM MEM-FORENSICS] calling secure boot"
		sh /ids-prototype/secureboot/secure-boot.sh
		#at this point, we have a clean instance; need to update cid, pid, and t0
		echo "[FROM MEM-FORENSICS] clean instance created; resetting variables"
		cid=$(docker container ls --all --quiet --no-trunc --filter "name=appEnv")
		pid=$(docker inspect -f '{{.State.Pid}}' $cid)
		cd /ids-prototype/fingerprinting/New_Mem_Dumps/$app
		#need to re-create blank t1 and t0 folders with empty bin dirs inside
		rm -r t0 t1
		mkdir t0 t1
		mkdir t0/bin t1/bin
		#make new t0 mem dump
		cd t0/bin
		echo "[FROM MEM-FORENSICS] making new t0 dump"
		./../../../../memfetch/memfetch $pid
		echo "[FROM MEM-FORENSICS] finished getting mem dump for t0"
		echo "[FROM MEM-FORENSICS] recovery process complete; resuming loop"
	else
		echo "[FROM MEM-FORENSICS] similarity score check passed"
		#remove t0
		cd /ids-prototype/fingerprinting/New_Mem_Dumps/$app
		rm -r t0
		echo "[FROM MEM-FORENSICS] setting t1 as the new t0"
		#make old t1 new t0
		mv t1 t0
		#create a new, empty t1
		mkdir t1
		mkdir t1/bin
		echo "[FROM MEM-FORENSICS] assessment complete; resuming loop"
	fi

done

