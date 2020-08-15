################################
# SAX is a callback-based API 
# for intercepting parser events
################################

import xml.sax.handler

class BookHandler(xml.sax.handler.ContentHandler):
  def __init__(self):
    self.inTitle = 0                                # handle xml parser events
    self.mapping = {}                               # a state machine model

  def startElement(self, name, attributes):
    if name == "book":                              # on start book tag
      self.buffer = ""                              # save isbn for dict key
      self.isbn = attributes["isbn"]              
    elif name == "title":                           # on start title tag
      self.inTitle = 1                              # save title text to follow

  def characters(self, data):
    if self.inTitle:                                # on text within tag
      self.buffer += data                           # save text if in title

  def endElement(self, name):
    if name == "title":
      self.inTitle = 0                              # on end title tag
      self.mapping[self.isbn] = self.buffer         # store title text in dict
