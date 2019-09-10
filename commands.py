from abc import ABCMeta, abstractmethod

class commands(metaclass=ABCMeta):
    def __init__(self):
        self.com = {
            "user": self.user,
            "pass": self.pword,
            "quit": self.quitProgram,
            "port": self.portt,
            "pwd": self.pwd,
            "type": self.typeCode,       #ascii- TYPE A and binary is TYPE I
            # "pasv": self.pasv,
            "list": self.listDir,
            "mode": self.mode,
            "stru": self.structure,
            "retr": self.retrieve,
            "noop": self.noop,
            # "stor": self.store,
            "size": self.sizeFile,
            "cwd": self.CWD
        }

    def callMethod(self,str):
        print(str)
        self.com[str]()

    @abstractmethod

    def user(self, args):
        pass
    
    def pword(self, args):
        pass

    # def quitProgram(self, args):
    #     pass

    def portt(self, args):
        pass

    # def pwd(self, args):
    #     pass

    # def typeCode(self, args):
    #     pass

    # def pasv(self, args):
    #     pass

    def listDir(self, args):
        pass

    def mode(self, args):
        pass

    def structure(self, args):
        pass
    def noop (self,args):
        pass
    def sizeFile(self,args):
        pass
    def CWD(self,args):
        pass

    def retrieve(self, args):
        pass

    # def store(self, args):
    #     pass
    
