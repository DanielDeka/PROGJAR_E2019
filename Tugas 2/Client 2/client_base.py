import socket


SERVER_IP = '127.0.0.1'
SERVER_PORT = 9000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto("READY", (SERVER_IP, SERVER_PORT))
counter=1

def getImage():
    while True:
        data, addr = sock.recvfrom(1024)
        if(data[0:5]=="START"):
            print data[6:]
            fp = open(data[6:],'wb+')
            ditulis=0
        elif(data=="SUCCESS"):
            fp.close()
        elif(data=="DONE"):
            break
        else:
            # print "blok ", len(data), data[0:10]
            fp.write(data)

while counter==1:
    data, addr = sock.recvfrom(1024)
    if(data=="SENDING"):
        getImage()
        counter = 0
