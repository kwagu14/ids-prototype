FROM debian:latest

RUN apt-get update ; apt-get install docker.io -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install tqdm paho-mqtt scipy soundfile matplotlib librosa wave dtw
RUN apt-get install -y build-essential 
RUN apt-get install -y git
RUN apt-get install -y mosquitto-clients
RUN git clone https://github.com/kwagu14/ids-prototype.git
RUN apt-get install libsndfile1
#set up the directory structure required of the fingerprinting script
RUN mkdir /ids-prototype/mem-forensics/memDumps
RUN mkdir /ids-prototype/mem-forensics/memDumps/ir-app
RUN mkdir /ids-prototype/mem-forensics/memDumps/ir-app/t0
#CMD ["sh", "/home/ids-prototype/fingerprinting/mem-forensics.sh"]

