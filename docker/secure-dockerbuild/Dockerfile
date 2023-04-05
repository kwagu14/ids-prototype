FROM debian:latest

RUN apt-get update ; apt-get install docker.io -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install scipy 
RUN pip3 install soundfile 
RUN pip3 install matplotlib 
RUN pip3 install librosa 
RUN pip3 install wave 
RUN pip3 install dtw 
RUN apt-get install -y build-essential 
RUN apt-get install -y git
RUN apt-get install -y mosquitto-clients
RUN cd /home
RUN git clone https://github.com/kwagu14/ids-prototype.git
RUN cd ids-prototype/fingerprinting/New_Mem_Dumps/ir-sensor
RUN rm -rf t0 t1
RUN mkdir t0 t1
RUN mkdir t0/bin t1/bin
#CMD ["sh", "/home/ids-prototype/fingerprinting/mem-forensics.sh"]

