import socket
import threading
import signal
import sys
from commands import commands
from serverDtp import serverDtp
import copy
import os

class serverPiThread(threading.Thread, commands):
    def __init__(self, sock, address):
        threading.Thread.__init__(self)
        commands.__init__(self)
        self.sock = sock
        self.address = address

        self.active = True
        self.userName = ""
        self.dir = os.getcwd() + "/server"
        self.dataPort = 20
        self.dtp = None

    def run(self):
        print("Client: " + self.address[0] + " connected")

        #connection confirmation
        reply = "220 Successfully connected to server\r\n"
        self.sock.send(reply.encode())

        self.handleCommands()
        return

    def user(self, args):
        print("User " + args[1] + " connected.")
        self.userName = args[1]
        reply = "331 Username ok, password required\r\n"
        self.sock.send(reply.encode())
        return

    def pword(self, args):
        print("User logged in.")
        # password checking
        reply = "230 User logged in\r\n"
        self.sock.send(reply.encode())
        return

    def port(self, args):
        prt = args[1].split(',')
        print(hex(int(prt[4])))
        print(hex(int(prt[5])))
        prt = hex(int(prt[4])) + hex(int(prt[5])).split('x')[-1]
        print(prt)
        self.dataPort = int(prt, 16)
        reply = "200 Data port changed to " + args[1] + "\r\n"
        self.sock.send(reply.encode())
        return

    def pwd(self, args):
        # print(os.listdir(self.dir))
        reply = "257 " + "/" + self.userName + "\r\n"
        self.sock.send(reply.encode())
        return

    def retrieve(self, args):
        #instantiate DTP
        #if file status ok using DTP
        reply = "150 File status ok; about to open data connection \r\n"
        self.sock.send(reply.encode())
        #create data connection using DTP and send
        return

    def typeCode(self, args):
        # deal with arguments
        reply = "200 Command ok \r\n"
        self.sock.send(reply.encode())
        return

    # def pasv(self, args):
    #     # instantiate DTP and make it listen on a port (return host and port)
    #     # dtp = DTP(true) # true since passive mode
    #     # prt = dtp.port()
    #     self.dtp = 'Yes'
    #     addr = self.address.split(".")
    #     reply = "227 " + addr[0] + "," + addr[1] + "," + addr[2] + "," + addr[3] + ",4,35" + "\r\n"
    #     self.sock.send(reply.encode())
    #     return

    def listDir(self, args):
        if(not self.dtp):
            print('Create new dtp')
            self.dtp = serverDtp(self.dataPort, self.address[0])

        if(len(args) > 1):
            print(args[1])
        else:
            print('Current dir')
            resp = self.dtp.listDir(self.dir + "/" + self.userName)
            
            if (not resp):
                reply = "550 No files in directory"
                self.sock.send(reply.encode())


    def quitProgram(self, args):
        self.active = False
        print("Closing connection with " + self.address[0])
        reply = "200 Closing connection\r\n"
        self.sock.send(reply.encode())
        return

    def handleCommands(self):
        while(self.active):
            data = self.sock.recv(4096)
            decodeData = str(bytes.decode(data))
            clientComm = decodeData.lower()
            clientComm = clientComm.split()

            try:
                print(clientComm)
                self.com[clientComm[0]](clientComm)
            except:
                reply = "500 Command not recognised\r\n"
                self.sock.send(reply.encode())

        return

class serverPi():
    def __init__(self):
        self.port = 21              
        self.address = "localhost"
        self.sock = None

        signal.signal(signal.SIGINT, self.exitHandler)

    def exitHandler(self, sig, frame):
        print("\nServer stopping...")
        if (self.sock):
            self.sock.close()
        sys.exit(0)
        return


    def listen(self):
        print("Server starting...")

        try:
            self.sock = socket.socket()
            self.sock.bind((self.address, self.port))

            print("Server started on port: " + str(self.port))

            self.sock.listen()

            threads = []
            threadCount = -1
        except:
            print("Error: Could not create socket to listen for connections")

        while (True and self.sock) :

            clientSock, clientAddress = self.sock.accept()

            if clientSock:
                # new thread for this client
                threads.append(serverPiThread(clientSock, clientAddress))
                threadCount += 1
                threads[threadCount].start()
            
        print("Server stopping...")

        if self.sock:
            self.sock.close()

        return


    def user(self):
        print("worked")
        pass
