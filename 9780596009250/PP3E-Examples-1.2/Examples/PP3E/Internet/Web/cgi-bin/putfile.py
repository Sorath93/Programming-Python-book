#!/usr/bin/python
#######################################################
# extract file uploaded by http from web browser;
# users visit putfile.html to get the upload form 
# page, which then triggers this script on server;
# note: this is very powerful, and very dangerous:
# you will usually want to check the filename, etc.
# this may only work if file or dir is writeable;
# a unix 'chmod 777 uploads' command may suffice;
# file path names may arrive in client's path format;
#######################################################
     
import cgi, os, sys
import posixpath, ntpath, macpath      # for client paths
debugmode    = False                   # True=print form info
loadtextauto = False                   # True=read file at once
uploaddir    = './uploads'             # dir to store files
     
sys.stderr = sys.stdout                # show error msgs
form = cgi.FieldStorage()              # parse form data
print "Content-type: text/html\n"      # with blank line
if debugmode: cgi.print_form(form)     # print form fields
     
# html templates
     
html = """
<html><title>Putfile response page</title>
<body>
<h1>Putfile response page</h1>
%s
</html>"""
     
goodhtml = html % """
<p>Your file, '%s', has been saved on the server as '%s'. 
<p>An echo of the file's contents received and saved appears below.
</p><hr>
<p><pre>%s</pre>
</p><hr>
"""
     
# process form data
     
def splitpath(origpath):                              # get file at end
    for pathmodule in [posixpath, ntpath, macpath]:   # try all clients
        basename = pathmodule.split(origpath)[1]      # may be any server
        if basename != origpath:
            return basename                           # lets spaces pass
    return origpath                                   # failed or no dirs
    
def saveonserver(fileinfo):                           # use file input form data
    basename = splitpath(fileinfo.filename)           # name without dir path
    srvrname = os.path.join(uploaddir, basename)      # store in a dir if set
    if loadtextauto:
        filetext = fileinfo.value                     # reads text into string 
        open(srvrname, 'wb').write(filetext)          # save in server file
    else:
        srvrfile = open(srvrname, 'wb')               # else read line by line
        numlines, filetext = 0, ''                    # e.g., for huge files
        while 1:
            line = fileinfo.file.readline()
            if not line: break
            srvrfile.write(line)
            filetext = filetext + line
            numlines = numlines + 1
        filetext = ('[Lines=%d]\n' % numlines) + filetext
    os.chmod(srvrname, 0666)   # make writeable: owned by 'nobody'
    return filetext, srvrname
     
def main():
    if not form.has_key('clientfile'): 
        print html % "Error: no file was received"
    elif not form['clientfile'].filename:
        print html % "Error: filename is missing"
    else:
        fileinfo = form['clientfile']
        try: 
            filetext, srvrname = saveonserver(fileinfo)
        except:
            errmsg = '<h2>Error</h2><p>%s<p>%s' % tuple(sys.exc_info()[:2])
            print html % errmsg
        else:
            print goodhtml % (cgi.escape(fileinfo.filename), 
                              cgi.escape(srvrname), 
                              cgi.escape(filetext))
main()
