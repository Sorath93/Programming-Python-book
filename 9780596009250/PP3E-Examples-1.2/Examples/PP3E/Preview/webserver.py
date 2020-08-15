######################################################################
# implement HTTP web server in Python which knows how to run server
# side CGI scripts;  serves files/scripts from current working dir;
# python scripts must be stored in webdir\cgi-bin or webdir\htbin;
######################################################################

webdir = '.'   # where your html files and cgi-bin script directory live
port   = 80    # default http://localhost/, else use http://localhost:xxxx/

import os, sys
from BaseHTTPServer import HTTPServer
from CGIHTTPServer  import CGIHTTPRequestHandler

# hack for Windows: os.environ not propogated
# to subprocess by os.popen2, force in-process
if sys.platform[:3] == 'win':
    CGIHTTPRequestHandler.have_popen2 = False
    CGIHTTPRequestHandler.have_popen3 = False

os.chdir(webdir)                                       # run in html root dir
srvraddr = ("", port)                                  # my hostname, portnumber
srvrobj  = HTTPServer(srvraddr, CGIHTTPRequestHandler)
srvrobj.serve_forever()                                # run as perpetual demon
