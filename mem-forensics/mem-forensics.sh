#!/bin/bash

#subscribe to alerts topic
python3 /ids-prototype/networking/mqtt_subscribe.py "security/alerts" &

#initialize values
#proof of concept will use the RFID application as benign memory
app=$1
cid=$(docker container ls --all --quiet --no-trunc --filter "name=appEnv")
pid=$(docker inspect -f '{{.State.Pid}}' $cid)
echo "[FROM MEM-FORENSICS] cid and pid initialized"

#periodic memory forensics; runs as long as the device is running
while [ true ]
do
	#go into the rfid application folder; this is where memdumps will be stored
	cd /ids-prototype/mem-forensics/memDumps/"$app"/t0
	#get a memory dump of the iot process 
	../../../memfetch/memfetch $pid
	echo "[FROM MEM-FORENSICS] finished getting mem dump"
	#convert the dump into a wav file; source is current directory; dest is audioFiles
	python3 ../../../wav-gen.py /ids-prototype/mem-forensics/memDumps/"$app" $app 
	#send the file to the classifier
	echo "[FROM MEM-FORENSICS] passing the audio file to the classifier server"
	python3 ../../../../networking/file_client.py iot_dev_1 fileTransfer $app-0.wav
	#get the similarity score from the classifier
	python3 ../../../../networking/file_client.py iot_dev_1 getSimularity $app-0.wav 
	similarity=$(cat similarity.txt)
	echo "[FROM MEM-FORENSICS] got the similarity score: $simularity"
	
	#in this case, we have a malicious memory
	if [ $similarity="0" ]
	then
		echo "[FROM MEM-FORENSICS] similarity check failed; broadcasting alert to other devices"
		#Broadcast alert in network
		python3 /ids-prototype/networking/mqtt_publish.py "security/alerts" "COMPROMISE"
		#call secure boot
		echo "[FROM MEM-FORENSICS] initiating secure boot"
		sh /ids-prototype/secureboot/secure-boot.sh
		#at this point, we have a clean instance; need to update cid, pid, and t0
		echo "[FROM MEM-FORENSICS] IoT environment cleaned; resetting variables"
		cid=$(docker container ls --all --quiet --no-trunc --filter "name=appEnv")
		pid=$(docker inspect -f '{{.State.Pid}}' $cid)
		#the memDumps/[app-name]/t0 folder needs to be emptied
		cd /ids-prototype/mem-forensics/memDumps/"$app"
		rm -r t0
		mkdir t0
		echo "[FROM MEM-FORENSICS] recovery process complete; resuming loop"
	else
		echo "[FROM MEM-FORENSICS] similarity score check passed; cleaning up..."
		#We need to clean out the memDumps/[app-name] folder so it can hold a new dump
		cd /ids-prototype/mem-forensics/memDumps/"$app"
		rm -r t0
		mkdir t0
		echo "[FROM MEM-FORENSICS] environment clean; Resuming loop"
	fi

done


