FROM debian:latest

RUN apt-get update ; apt-get install docker.io -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install scipy matplotlib librosa wave dtw paho-mqtt
RUN apt-get install -y build-essential 
RUN apt-get install -y git
RUN apt-get install -y mosquitto-clients
RUN git clone https://github.com/kwagu14/ids-prototype.git
#set up the directory structure required of the fingerprinting script
RUN mkdir /ids-prototype/fingerprinting/New_Mem_Dumps
RUN mkdir /ids-prototype/fingerprinting/New_Mem_Dumps/ir-sensor
RUN mkdir /ids-prototype/fingerprinting/New_Mem_Dumps/ir-sensor/t0
RUN mkdir /ids-prototype/fingerprinting/New_Mem_Dumps/ir-sensor/t1
RUN mkdir /ids-prototype/fingerprinting/New_Mem_Dumps/ir-sensor/t0/bin
RUN mkdir /ids-prototype/fingerprinting/New_Mem_Dumps/ir-sensor/t1/bin
#CMD ["sh", "/home/ids-prototype/fingerprinting/mem-forensics.sh"]

