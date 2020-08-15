######################################
# xml-rpc marshals data over HTTP, as 
# XML text; provides a simple remote 
# procedure call client interface
######################################

# simple test program (from XML-RPC specification)
# server = Server("http://localhost:8000") # local server

from xmlrpclib import Server

server = Server("http://betty.userland.com")
print server

try:
    print server.examples.getStateName(41)       
except Error, v:
    print "ERROR", v

########################################
# See also: SimpleXMLRPCServer module:
# provides a basic server framework for 
# XML-RPC servers written in Python
########################################
