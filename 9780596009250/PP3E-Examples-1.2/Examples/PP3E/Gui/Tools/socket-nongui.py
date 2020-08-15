import time, sys
from socket import *

# gui interface
port = 50008                             # i am client: use GUI server port
host = 'localhost'                       # or start me after GUI started
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((host, port))
file = sock.makefile('w', 0)             # file interface wrapper, unbuffered
sys.stdout = file                        # make prints go to sock.send

# non-gui code
while 1:                                 # print data to stdout
    print time.asctime()                 # sent to GUI process
    time.sleep(2.0)
