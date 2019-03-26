from socket import *
import socket
import threading
import thread
import time
import sys

#address stting
ADDRESS = ('127.0.0.1', 9000)

#socket setting
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ADDRESS)

#img files
images = ["1.jpg", "2.jpg", "3.png", "4.png"]

def UDPServer(ip, port):
   sock.sendto("SENDING", (ip, port))
   for a in images:
      sock.sendto("START {}".format(i), (ip, port))
      size = os.stat(a).st_size
      fp = open(a, 'rb')
      img = fp.read()
      sent = 0
      for b in img:
         sock.sendto(b, (ip, port))
         sent+=1
         print "\r {} of {} images sent" . format(sent, size)
      sock.sendto("SUCCESS", (ip, port))
      fp.close
   sock.sendto("DONE", (ip, port))

while True:
   print "Waiting for connection . . ."
   data, address = sock.recvfrom(1024)
   #getting signal from client
   if (data=="READY") == "cmd_connect":
      thread = Thread(target=UDPServer, args=address)
      thread.start()