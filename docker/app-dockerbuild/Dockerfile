FROM debian:latest
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y wget
#Mirai Dependencies
RUN apt-get install -y gcc golang electric-fence sudo
RUN apt-get install -y mysql-server mysql-client
RUN pip3 install RPi.GPIO
ADD application/IR-sensor.py /home/
CMD ["python3", "/home/IR-sensor.py"]
