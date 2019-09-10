import socket
import os
import stat

class serverDtp:
    def __init__(self, port, address):
        self.port = port
        self.address = address
        self.sock = None

        print(port)
        print(address)

        try:
            self.sock = socket.socket()
            self.sock.connect((address, port))

        except:
            print('Could not create server DTP')


    def listDir(self, direc):
        print('listing ' + direc)
        with os.scandir(direc) as dirs:
            data = ""
            for entry in dirs:
                fileInfo = entry.stat()
                print(stat.filemode(fileInfo.st_mode))
        
        if (len(data) > 0):
            self.sock.send(dirs.encode())
            return True
        
        return False