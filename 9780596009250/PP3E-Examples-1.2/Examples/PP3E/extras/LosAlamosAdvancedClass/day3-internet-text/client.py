#############################################################
# Client side: use sockets to send data to the server, and 
# print server's reply to each message line; 'localhost' 
# means that the server is running on the same machine as 
# the client, which lets us test client and server on one 
# machine;  to test over the net, run server on a remote 
# machine, set serverHost to machine's domain name or IP addr;
#############################################################
 
import sys
from socket import *              # portable socket interface plus constants
serverHost = 'localhost'          # server name, or: 'starship.python.net'
serverPort = 50007                # non-reserved port used by the server
 
message = ['Hello network world']           # text to send to server
sockobj = socket(AF_INET, SOCK_STREAM)      # make a TCP/IP socket object
sockobj.connect((serverHost, serverPort))   # connect to serve and port

for line in message:
    sockobj.send(line)                      # send line to server over socket
    data = sockobj.recv(1024)               # receive from server: up to 1k
    print 'Client received:', `data`
 
sockobj.close()                             # close to send eof to server

