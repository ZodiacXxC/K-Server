import socket
import threading
import datetime
connections = []
total_connections = 0


x = datetime.datetime.now()
xdate = str(x.day) + "/" + str(x.month)  + "/" + str(x.year)
currentTime = ''
class Client(threading.Thread):
    x = datetime.datetime.now()
    xdate = str(x.day) + "/" + str(x.month)  + "/" + str(x.year)
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)

    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
                data_en = data.decode('utf-8')
            except:
                currentDateAndTime1 = datetime.datetime.now()
                currentTime1 = currentDateAndTime1.strftime("%H:%M:%S")
                print("Client " + str(self.address) + " has disconnected "+ ": "+ currentTime1 + " - " + xdate)
                self.signal = False
                connections.remove(self)
                break
            if data != "":
                print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                for client in connections:
                    if client.id != self.id:
                        xdata = str(self.id) + " : " + str(data)
                        print(data_en)
                        client.socket.sendall(data_en.encode("utf-8"))


def newConnections(socket):
    while True:
        currentDateAndTime = datetime.datetime.now()
        currentTime = currentDateAndTime.strftime("%H:%M:%S")
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]) + ": "+ currentTime + " - " + xdate)
        total_connections += 1

def main():
    #Get host and port
    host = "0.0.0.0"
    port = 12345
    #Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    #Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start()

    
    



main()
