FROM debian:latest

RUN apt-get update ; apt-get install docker.io -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install scipy soundfile matplotlib librosa wave dtw timeit json
RUN apt-get install -y build-essential 
RUN apt-get install -y git
RUN apt-get install -y mosquitto-clients
RUN cd /home
RUN git clone https://github.com/kwagu14/ids-prototype.git
RUN cd ids-prototype
RUN rm -r application docker
RUN cd fingerprinting/New_Mem_Dumps/ir-sensor
RUN rm -r t0 t1
RUN mkdir t0 t1
RUN mkdir t0/bin t1/bin
CMD ["sh", "/home/ids-prototype/fingerprinting/mem-forensics.sh"]

