import socket
import os
from _thread import *
import signal
import sys
#this will "import" the python file into the code
exec(open("./cnn-model.py", "rb").read())


#This is the server IP address; we'll use our public address
SERVER_HOST = "192.168.33.98"
#The port that clients have to enter 
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"



#code for handling each client that connects
def receiveFile(client_socket, identity, filename):
    path = identity + "/" + filename
    #this is for getting the file size sent by client
    filesize = client_socket.recv(BUFFER_SIZE).decode()
    filename = os.path.basename(path)
    filesize = int(filesize)
    progress = tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(path, "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
    
    
def sendSimularity(client_socket, identity, filename):
    path = identity + "/" + filename
    print("[FROM FILESERVER]: Passing file to classifier...")
    simularity = classify(path)
    print("[FROM FILESERVER]: Simularity found to be ", simularity)
    #send to the client
    client_socket.send(simularity.encode())



#this function will be used every time a new connection request comes in
def clientThread(client_socket, identity, op, filePath):
    
    #here the client is trying to send us a file
    if op == "fileTransfer":
        receiveFile(client_socket, identity, filePath)      
    #here it is requesting the simularity for a specific file
    elif op == "getSimularity":
        sendSimularity(client_socket, identity, filePath)
    #In this case, an invalid operation was supplied
    else:    
        print("[FROM FILESERVER]: Bad reqest received from client.")
        #when done, close connection

    client_socket.close()

    
#code for exiting gracefully upon ctrl+C signal
def sig_handler(sig, frame):
    print("[FROM FILESERVER]: Received SIGINT. Shutting down server...")
    global s
    s.close()
    sys.exit(0)
    
    
    
#install the signal handler
signal.signal(signal.SIGINT, sig_handler)

#create the server socket
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
#start listening for clients
s.listen(10)
print(f"[FROM FILESERVER]: Listening as {SERVER_HOST}:{SERVER_PORT}")


#create a separate thread for each connection
while(True):
    
    #problem: we have multiple sockets trying to receive stuff at once
    #and things don't know where to go; need to find some way to coordinate this
    
    #first, we need to get the client's request
    print("[FROM FILESERVER]: Waiting for the client to specify the request... ")
    client_socket, address = s.accept()
    print(f"[FROM FILESERVER]: {address} is connected.")
    received = client_socket.recv(BUFFER_SIZE).decode()
    print(received)
    identity, op, filePath = received.split(SEPARATOR)
    print("REQUEST: identity: ", identity, "operation: ", op, "file path: ", filePath)    
    #Once gotten, use that socket to handle the request

    start_new_thread(clientThread, (client_socket, identity, op, filePath, ))
    
    
