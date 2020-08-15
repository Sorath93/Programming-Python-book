Various XML and XML-RPC examples.  bookhandler
and dombook process the XML code in books.xml,
using SAX and DOM, respectively.  xmlrpc.py is 
a self-contained example file.

XML SAX parsers and DOM clients require Python 
2.0 or later; XML-RPC was added to Python in 2.2.

- SAX is an event/callback-base API for tapping
  into an XML document parsing process.

- DOM provides access to a complete and (usually)
  fully-parsed XML document object.

- XML-RPC marshals data between client and server
  over HTTP using XML as the message format.

- Many additional supported XML APIs are not 
  shown in these examples.

See also: Python library manual, and the O'Reilly
books "Python & XML" and "Python Standard Library".
