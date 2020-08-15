#!/usr/local/bin/python
######################################################
# use the Python SMTP mail interface module to send
# email messages; this is just a simple one-shot 
# send script--see pymail.py for a client with more
# user interaction features, and popmail.py for a
# script which retrieves mail; smtp is used to 
# send mail, and runs on a socket using port 
# number 25 on the server machine, but Python's 
# smtplib hides all protocol details; to fetch 
# mail, use the poplib or imaplib modules instead;
# on some systems, you can also send email with: 
# os.popen('mail -s "xxx" a@b.c', 'w').write(text), 
# but smtp is more portable/powerful (see PyErrata);
# notes: could escape '\nFrom' in the body with '>'
# so as not to terminate the email, but this is
# probably superfluous here--servers do this too;
# smtplib raises an exception if nobody got the
# mail, else returns a dictionary containing any
# recipients that failed (empty if no errors);
######################################################

import smtplib, string, sys, time
mailserver = 'smtp.fnal.gov'         # ex: starship.python.net

From = string.strip(raw_input('From? '))       # ex: lutz@rmi.net
To   = string.strip(raw_input('To?   '))       # ex: python-list@python.org
To   = string.split(To, ';')                   # allow a list of recipients
Subj = string.strip(raw_input('Subj? '))

# prepend standard headers
date = time.ctime(time.time())
text = ('From: %s\nTo: %s\nDate: %s\nSubject: %s\n' 
                         % (From, string.join(To, ';'), date, Subj))
text = text + '\n'   # blank line between hdrs,body

print 'Type message text, end with line=(ctrl + D or Z)'
while 1:
    line = sys.stdin.readline()
    if not line: 
        break                        # exit on ctrl-d/z
  # if line[:4] == 'From':
  #     line = '>' + line            # servers escape for us
    text = text + line

if sys.platform[:3] == 'win': print
print 'Connecting...'
server = smtplib.SMTP(mailserver)              # connect, no login step
failed = server.sendmail(From, To, text)
server.quit() 
if failed:                                     # smtplib may raise exceptions
    print 'Failed recipients:', failed         # too, but let them pass here
else:
    print 'No errors.'
print 'Bye.'

