from threading import Thread
import socket
import glob
import os
import time

#address stting
ADDRESS = ('127.0.0.1', 9000)
BLOCK_SIZE = 1024

#socket setting
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(ADDRESS)
print "Starting up on %s port %s" % ADDRESS
sock.listen(1)

def checkFiles():
	files = []
	files.extend(glob.glob('*'))
	return files

def processRequest(filename, ip, port):
	connection.sendto("START {}".format(filename), (ip, port))
	fp = open(filename, 'rb')
	file = fp.read()
	sent = 0
	for a in file:
		connection.sendto(a, (ip, port))
		sent+1
	time.sleep(1)
	connection.sendto("SUCCESS", (ip, port))
	time.sleep(1)
	fp.close
	connection.sendto("DONE", (ip, port))

def checkList(ip, port):
	connection.sendto("CHECK", (ip, port))
	files = checkFiles()
	for f in files:
		connection.sendto(f, (ip,port))
	time.sleep(1)
	connection.sendto("CHECKDONE", (ip, port))
	data, addr = connection.recvfrom(1024)
	if(data == "DOWNLOAD"):
		flag = 0
		while True:
			req = connection.recv(1024)
			if(req == "done"):
				connection.close()
				break
			for a in files:
				if(req == a):
					flag = 1
					# connection.sendto("ACCEPTED", (ip, port))
					# time.sleep(1)
					processRequest(req, ip, port)

			if(flag == 0):
				connection.sendto("REJECTED", (ip, port))
			flag = 0
	elif(data == "UPLOAD"):
		time.sleep(0.5)
		while True:
		    data, addr = connection.recvfrom(1024)
		    if(data[0:5]=="START"):
		        print "Uploading file",data[6:]
		        fp = open(data[6:],'wb+')
		    elif(data=="SUCCESS"):
		        fp.close()
		    elif(data=="DONE"):
		        print "Upload success."
		        connection.sendto("UPLOADDONE", (ip, port))
		        break
		    else:
		        # print "blok ", len(data), data[0:10]
		        fp.write(data)

while True:
   print "Waiting for connection . . ."
   connection, client_address = sock.accept()
   data = connection.recv(1024)
   #getting signal from client
   if (data=="READY"):
      print "Connected to", client_address[0], client_address[1]
      thread = Thread(target=checkList, args=client_address)
      thread.start()