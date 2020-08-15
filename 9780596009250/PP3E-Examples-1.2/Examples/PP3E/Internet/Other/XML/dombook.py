#####################################
# DOM gives the whole document to the
# application as a traversable object
#####################################

import pprint
import xml.dom.minidom
from xml.dom.minidom import Node

doc = xml.dom.minidom.parse("books.xml")          # load doc into object
                                                  # usually parsed up front
mapping = {}
for node in doc.getElementsByTagName("book"):     # traverse doc object
  isbn = node.getAttribute("isbn")                # via dom object api
  L = node.getElementsByTagName("title")
  for node2 in L:
    title = ""
    for node3 in node2.childNodes:
      if node3.nodeType == Node.TEXT_NODE:
        title += node3.data
    mapping[isbn] = title

# mapping now has the same value as in the SAX example
pprint.pprint(mapping)
