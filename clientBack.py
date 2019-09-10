from commands import commands
import socket
import threading
import signal
import sys
import tkinter


#Anon loogin??

class clientBack():

	def __init__(self):
		self.port = 21
		self.address = "demo.wftpserver.com"
		# self.address = "gnu.mirror.iweb.com"
		self.localAddress = ''     ##Put your IP HERE!!!
		self.sock = None
		self.portData=3002
		self.test=None

		self.sockData=None
		self.listData=''
		self.initData=False
		self.v=""
		self.codeString=""
		self.codeResp=""
		self.window = tkinter.Tk()
		self.frame = tkinter.Frame(self.window )
		self.actionText=tkinter.Label(self.window, text = "adress of ftp server: ").grid(row = 0) 
		self.entry=tkinter.Entry(self.window,textvariable=self.v)
		self.entry.grid(row = 0, column = 1) 
		self.button=tkinter.Button(self.window, text = "Connect: ", command = self.recordInput).grid(row=3, column=0, pady=4)
		self.code=tkinter.Label(self.window, text = "")
		self.code.grid(row =7, column = 0) 
		

		self.window.title("FTP Client")
		commands.__init__(self)
		signal.signal(signal.SIGINT, self.exitHandler)


	def userName(self):
		code=self.user(["USER", self.entryUser.get()])
		if ('331' in code):
			code=self.pword(["PASS", self.entryPass.get()])
			self.code.config(text=code)
			if('230' in code ):
				self.sendDataControl('SYST\r\n')
				code=self.listenControl()
				print((code))
				self.sendDataControl('FEAT\r\n')
				code=self.listenControl()
				print((code))
				self.sendDataControl('PWD\r\n')
				code=self.listenControl()
				print((code))
				for child in self.frame.winfo_children():
					if child != self.code:
						child.destroy()
				list = self.window.grid_slaves()
				for l in list:
					if l !=self.code:
						l.destroy()

				self.NewText=tkinter.Label(self.window, text = "Enter What you want to send to the server: ").grid(row = 0) 
				self.entryCommand=tkinter.Entry(self.window)
				self.entryCommand.grid(row = 0, column = 1) 
				self.buttonSend=tkinter.Button(self.window, text = "Send: ", command = self.handleInput).grid(row=2, column=0, pady=4)
				self.currentDir=tkinter.Label(self.window, text = "")
				self.currentDir.grid(row =9, column = 0) 
		else :
			self.code.config(text=code)



	def recordInput(self):
		self.address =self.entry.get()
		responce=''
		responce=self.connectControl()
		self.code.config(text=responce)
		if ('220' in responce):
			self.codeResp=responce

			for child in self.frame.winfo_children():
				if child != self.code:
					child.destroy()
			self.actionText=tkinter.Label(self.window, text = "Enter your username: ").grid(row = 0) 
			self.entryUser=tkinter.Entry(self.window)
			self.entryUser.grid(row = 0, column = 1) 
			self.actionText=tkinter.Label(self.window, text = "Enter your Password: ").grid(row = 1, column = 0) 
			self.entryPass=tkinter.Entry(self.window)
			self.entryPass.grid(row = 1, column = 1) 
			self.buttonLogin=tkinter.Button(self.window, text = "Login to server: ", command = self.userName).grid(row=3, column=0, pady=4)


	def run(self):



		self.window.mainloop()

		while (1):
			self.handleInput()


	def connectControl(self):						# If can't connect put contingency so cant send, will be ITO responce code
		print("Connecting to FTP server")
		try:
			self.sock = socket.socket()
			self.sock.connect((self.address,self.port))

			print("Server connected on port: " + str(self.port))
			code=self.listenControl()
			print(code)
			return code
			
		except:
			print("Error: Could not create socket to listen for connections")


	def sendDataControl(self,data):

		print(data)
		self.sock.send(data.encode())


	def connectData(self):						# If can't connect put contingency so cant send, will be ITO responce code
		print("Connecting to FTP server")
		try:
			self.sockData = socket.socket()
			self.sockData.connect((self.address,self.portData))

			print("Data Server connected on port: " + str(self.portData))

			
		except:
			print("Error: Could not create socket to listen for connections")
	

	def exitHandler(self, sig, frame):
		print("\Client stopping...")
		if (self.sock):
			self.sock.close()
		sys.exit(0)
		return

	def listenControl(self):
		try:

			data=self.sock.recv(1024).decode()
			print("Code recieved from server: "+ data)
		except:

			pass
		return data
	def listenForData(self,ip):
		print(ip)

		try:
			self.sockData = socket.socket()
			self.sockData.bind((ip, self.portData))

			# print("Server started on port: " + str(self.port))

			self.sockData.listen()

		except:
			print("Error: Could not create socket to listen for connections")
		while (True and not self.test) :
			print("Accepting")

			self.test, clientAddress = self.sockData.accept()
		print ("out")

	def listenData(self,input):
		print("listen")
		counter=0
		try:
			data='-'
			if('list' in input[0]):
				self.listData=''
				while (data!=''):
					data=self.test.recv(1448).decode()
					
					self.listData=self.listData+data
			if('file' in input[0]):

				print(input)

				with open (input[1],'wb') as remote:
					while (counter<input[2]):
						# print("inside")

						rec = self.sockData.recv(1448)
						remote.write(rec)

						counter+=1448

				fout.close()


		except:

			pass
		return data

	def pword(self,inputData):

		self.sendDataControl('PASS '+inputData[1]+"\r\n")
		code=self.listenControl()
		print((code))
		return code


	def user(self,inputData):
		print("worked!!")
		# print(inputData[1])
		# print("---")
		self.sendDataControl('USER'+' '+inputData[1]+"\r\n")
		# print("---")
		code=self.listenControl()
		print(code)
		return (code)


	def useInput(self,input):

		self.com[input[0]]()
		print(input[1])

	def portt(self, inputData):            #Check how to send!
		# print("here")
		portInfo=inputData[1].split(",")
		# portNumber="0x"+portInfo[4]+portInfo[5]
		print(portInfo)
		portHex= hex(int(portInfo[4])) + hex(int(portInfo[5]))
		print(hex(int(portInfo[4])))
		print(portHex)
		portDec = int('0x'+str(portHex), 16)
		# self.portData=portDec    #change which port data connection is one, IP can't change
		self.sendDataControl('PORT'+' '+inputData[1]+"\r\n")
		code=self.listenControl()
		print(code)
		self.localAddress=(portInfo[0]+'.'+portInfo[1]+'.'+portInfo[2]+'.'+portInfo[3])
		# code=self.listenControl()
		# print(code)
		print(self.portData)
		return (code)
		# self.portData=20



	def handleInput(self):

		inData=self.entryCommand.get()
		terms=inData.split(" ")
		code =''
		print(terms[0].lower())
		try:
			code=self.com[terms[0].lower()](terms)
		except: 
			# print(terms[0])
			# print ("Command entered is not recognised")
			pass
		self.code.config(text=self.codeString)
		self.currentDir.config(text=self.listData)
		

	def quitProgram(self, args):
		self.sendDataControl("QUIT\r\n")
		code=self.listenControl()
		self.codeString= code
		pass



	def pwd(self, args):
		pass

	def sizeFile(self,inputData):
		print("sizing")
		self.sendDataControl('SIZE '+"manual_en.pdf"+"\r\n")
		code=self.listenControl().split(" ")
		self.codeString= code
		return code[1]
		
		pass

	def typeCode(self, inputData): #ascii- TYPE A and binary is TYPE I
		self.sendDataControl('TYPE '+inputData[1]+"\r\n")
		code=self.listenControl()
		print((code))
		self.codeString= code
		pass

	def mode(self, inputData):          # S, B or C
		self.sendDataControl('MODE '+inputData[1]+"\r\n")
		code=self.listenControl()
		print((code))
		self.codeString= code
		pass

	def structure(self, inputData):
		self.sendDataControl('STRU '+inputData[1]+"\r\n")
		code=self.listenControl()
		print((code))
		self.codeString= code
		 

	def retrieve(self, inputData):

		sizeFile=self.com["size"](inputData)

		self.sendDataControl("TYPE A\r\n") 
		print(self.listenControl())

		self.sendDataControl("EPSV\r\n")
		code=self.listenControl()
		print (code)
		test=code.split("|")
		print(test)
		self.portData=int(test[3])
		self.connectData() 
		self.sendDataControl("RETR " + inputData[1] + "\r\n")
		code=self.listenControl()
		print (code)
		self.codeString= code
		if('150' in code):
			self.code.config(text=code)
			self.listenData(['file',inputData[1],int(sizeFile)])
			code=self.listenControl()
			print (code)
			self.codeString= code

		

	def store(self, args):
		pass


	def listDir(self,inputData):
		print("listing")

		# self.sendDataControl("EPSV\r\n")
		# code=self.listenControl()
		# print (code)
		# test=code.split("|")
		# print(test)
		# self.portData=int(test[3])
		# self.connectData()
		self.sendDataControl("LIST"+"\r\n")
		code=self.listenControl()
		print (code) 
		self.listenForData(self.localAddress)
		# code=self.listenControl()
		# print (code) 
		self.listenData(["list"])
		print(self.listData)
		code=self.listenControl()
		print (code) 
		self.codeString= code

	def noop(self,inputData):
		self.sendDataControl("NOOP\r\n")
		code=self.listenControl()
		print((code))
		self.codeString= code

	def CWD(self,inputData):
		self.sendDataControl('CWD '+inputData[1]+"\r\n")
		codeCW=self.listenControl()
		print((codeCW))
		self.listDir(inputData)
		print(codeCW)
		self.codeString= codeCW
		print(codeCW)



		
		


		