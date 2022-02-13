#!/usr/bin/python2 
import socket
import os

s = socket.socket()
host = '172.20.10.3' #host/server ip
port = 1234
s.bind((host, port))
s.listen(True)

def server():
    while True:
        print "host", host, "is listening on port", port

        #getting file info
        tobesend = raw_input("Enter name file you want to send : ")
        file_size = os.stat(tobesend)
        buffer_size = file_size.st_size  +100
        print "File :", tobesend, "\t\t\t\t", file_size.st_size/8, "Bytes\nWaiting for Client"

        #Sending file info to the client
        conn, addr = s.accept()
        print "Connection from", addr[0], "on port",addr[1]
        filedata= tobesend+" "+ str(buffer_size)
        conn.send(filedata)
        conn.close()

        #Sending actual file
        conn, addr = s.accept()
        file= open(tobesend, 'rb')
        fileData = file.read(buffer_size) #Reading data from file with buffer_size( for safety +100 bits)
        conn.send(fileData)
        conn.close()
        print "File sent successfully"
        
if __name__ == '__main__':
    server()