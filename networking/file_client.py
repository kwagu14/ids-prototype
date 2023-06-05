import socket
import tqdm
import os
import sys

#USAGE: 
# Running the script: 
#	--> python3 file_client.py [identity] [operation] [fileName]

# identity= name of IoT device
# operation= fileTransfer or getSimularity
# fileName= the path that the wav file should go to on the server or
#           the path of the wav file to find simularity


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

#this is the server's IP and port
host = "192.168.33.98"
port = 5001


def sendFile(s, filename):

    filesize = os.path.getsize(filename)
    s.send(str(filesize).encode())

    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
        print("[FROM FILE CLIENT]: Done sending file.")


def receiveScore(s):
    simularity = s.recv(BUFFER_SIZE).decode()
    retFile = open("simularity.txt", "w")
    retFile.write(simularity)
    retFile.close()

def sendRequest(s, identity, operation, filePath):
    request = identity + SEPARATOR + operation + SEPARATOR + filePath
    s.send(request.encode())
    print("[FROM FILE CLIENT]: Request sent to server.")



### MAIN PROG

# we'll get the arguments
identity = sys.argv[1]
operation = sys.argv[2]
filename = sys.argv[3]


#now we need to check the operaton and call appropriate code
if operation == "fileTransfer":
    s = socket.socket()
    s.connect((host, port))
    sendRequest(s, identity, operation, filename)
    sendFile(s, filename)
    s.close()
elif operation == "getSimularity":
    s = socket.socket()
    s.connect((host, port))
    sendRequest(s, identity, operation, filename)
    #after sending the request, we need to let the socket know we're done writing
    s.shutdown(socket.SHUT_WR)
    receiveScore(s)
    s.close()
    
else:
    print("Unsupported operation; see usage notes")
