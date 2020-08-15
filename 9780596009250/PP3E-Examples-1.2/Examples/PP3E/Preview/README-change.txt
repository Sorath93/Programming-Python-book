Change from book: changes the for actions in cgi101.html
and peoplecgi.html to be GET instead of POST, because the
Internet Explorer browser on Windows has problems with POST
when using the webserver.py script.  Firefox, the browser
used to test exampples, handles POST fine.  

IE will likely have issues with POST in other book examples
too, when running the book's Python-coded web server; use 
GET in HTML files instead.