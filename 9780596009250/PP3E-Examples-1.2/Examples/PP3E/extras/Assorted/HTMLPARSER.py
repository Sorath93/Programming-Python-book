from htmllib import HTMLParser
from urllib import urlopen
siteurl = 'http://10.0.1.5:9000'

text = urlopen(siteurl).read()
class MyParser(HTMLParser):
    def __init__(self):
        self.result = []
      

parser = MyParser()
parser.feed(text)
parser.close()
print parser.result


