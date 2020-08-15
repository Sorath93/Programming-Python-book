Note: in the book, the example titles of imported module files
give their paths as this directory, not cgi-bin/.  As shipped
here, though, all modules are in cgi-bin/ along with the CGI
scripts that use them.  The latter structure is more portable, 
because CGI scripts spawned as processes on other platforms will
have their current working directory set to cgi-bin/ for imports.

With the server used in the text, this is irrelevent when 
running scripts in-process on Windows.  The webserver runs in 
this directory (current dir for imports), but also adds cgi-bin/
to sys.path manually, to emulate a spawned script's current dir
for imports.  Imports will look in both places, but cgi-bin, or
manual sys.path configuration, is usually better.
