#################################################
# implement HTTP server in Python which 
# knows how to run server-side CGI scripts;
# serves files/scripts from current working dir;
# scripts must be in webdir\cgi-bin or htbin
#################################################
 
webdir = '.'
import os, sys
from BaseHTTPServer import HTTPServer
from CGIHTTPServer  import CGIHTTPRequestHandler
 
# hack for Windows: os.environ not propogated
# to subprocess by os.popen2, force in-process
if sys.platform[:3] == 'win':
    CGIHTTPRequestHandler.have_popen2 = False
    CGIHTTPRequestHandler.have_popen3 = False
 
os.chdir(webdir)                  # run in html root dir
srvraddr = ("", 8080)             # my hostname, portnumber
srvrobj  = HTTPServer(srvraddr, CGIHTTPRequestHandler)
srvrobj.serve_forever()           # run as perpetual demon
