FROM debian:latest
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y wget
RUN apt-get install -y gcc golang electric-fence sudo
RUN pip3 install RPi.GPIO mfrc522
ADD application/ir/decToBin.py /home/
CMD ["python3", "/home/decToBin.py"]
