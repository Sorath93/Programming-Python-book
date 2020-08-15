import urllib
reply = urllib.urlopen('http://localhost:8080/cgi-bin/cgi101.py?user=Guido').read()
print reply
