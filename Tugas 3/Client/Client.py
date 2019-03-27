import socket
import glob
import time

ADDRESS = ('127.0.0.1', 9000)
BLOCK_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Connecting to %s port %s" % ADDRESS
sock.connect(ADDRESS)
sock.sendto("READY", (ADDRESS))

def checkFiles():
    files = []
    files.extend(glob.glob('*'))
    return files

def uploadFile(filename):
    sock.sendto("START {}".format(filename), (ADDRESS))
    fp = open(filename, 'rb')
    file = fp.read()
    sent = 0
    for a in file:
        sock.sendto(a, (ADDRESS))
        sent+1
    time.sleep(1)
    sock.sendto("SUCCESS", (ADDRESS))
    time.sleep(1)
    fp.close
    sock.sendto("DONE", (ADDRESS))

def receiveFile():
    while True:
        data, addr = sock.recvfrom(1024)
        if(data=="REJECTED"):
            print "File doesn't exist. Terminating..."
            break
        elif(data[0:5]=="START"):
            print "Downloading file",data[6:]
            fp = open(data[6:],'wb+')
        elif(data=="SUCCESS"):
            fp.close()
        elif(data=="DONE"):
            print "Download success."
            break
        else:
            # print "blok ", len(data), data[0:10]
            fp.write(data)

def receiveFileInfo():
    arr = []
    while True:
        data, addr = sock.recvfrom(1024)
        if(data=="CHECKDONE"):
            print "File checking done."
            break
        arr.append(data)
    for x in range(len(arr)):
        print arr[x]
    print "File checking done. Choose the option :\n1. Download a file\n2. Upload a file\n"

while True:
    data, addr = sock.recvfrom(1024)
    if(data=="CHECK"):
        print "Checking Files. Please Wait."
        receiveFileInfo()
        option = raw_input()
        if(option == "1"):
            sock.sendto("DOWNLOAD", (ADDRESS))
            request = raw_input()
            sock.sendto(request, (ADDRESS))
            receiveFile()
            break
        elif(option == "2"):
            sock.sendto("UPLOAD", (ADDRESS))
            request = raw_input()
            files = checkFiles()
            print request
            flag = 0
            for a in files:
                if(request == a):
                    flag = 1
                    uploadFile(request)
                    data = sock.recvfrom(1024)
                    if(data=="UPLOADDONE"):
                        print "Upload Successful."
            if(flag == 0):
                print "File doesn't exist. Terminating..."
                break