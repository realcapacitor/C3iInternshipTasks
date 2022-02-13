#!/usr/bin/python2 
import socket 

def client():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '172.20.10.3' #Server's ip address
        port = 1234
        s.connect((host, port))
        print "Connection established successfully"
        #Getting file info
        fileData = s.recv(400).split() #Approx 50 bytes of buffer for receving file info.
        file = open(fileData[0].strip() , 'wb') #file will be saved as the string comming.
        s.close()

        #Getting actual file
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        filesize = int(fileData[1]) +100    #keeping +100 bits of buffer for safety.
        s.connect((host, port))
        fileData1 = s.recv(filesize)
        file.write(fileData1)
        file.close()
        s.close()
        print "File Received Successfully\n",fileData[0].strip(),"\t\t\t",(int(fileData[1])-100)/8,"Bytes\n"," Go check"

if __name__ == '__main__':
    client()