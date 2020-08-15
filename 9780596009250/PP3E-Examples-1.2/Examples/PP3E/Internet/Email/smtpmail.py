#!/usr/local/bin/python
###########################################################################
# use the Python SMTP mail interface module to send email messages; this 
# is just a simple one-shot send script--see pymail, PyMailGUI, and 
# PyMailCGI for clients with more user interaction features; also see
# popmail.py for a script which retrieves mail, and the mailtools pkg
# for attachments and formatting with the newer std lib email package;
###########################################################################
     
import smtplib, sys, time, mailconfig
mailserver = mailconfig.smtpservername         # ex: starship.python.net
     
From = raw_input('From? ').strip()             # ex: lutz@rmi.net
To   = raw_input('To?   ').strip()             # ex: python-list@python.org
To   = To.split(';')                           # allow a list of recipients
Subj = raw_input('Subj? ').strip()
     
# standard headers, followed by blank line, followed by text
date = time.ctime(time.time())
text = ('From: %s\nTo: %s\nDate: %s\nSubject: %s\n\n'
                         % (From, ';'.join(To), date, Subj))
     
print 'Type message text, end with line=(ctrl + D or Z)'
while 1:
    line = sys.stdin.readline()
    if not line: 
        break                        # exit on ctrl-d/z
  # if line[:4] == 'From':
  #     line = '>' + line            # servers escape for us
    text = text + line
     
print 'Connecting...'
server = smtplib.SMTP(mailserver)              # connect, no login step
failed = server.sendmail(From, To, text)
server.quit() 
if failed:                                     # smtplib may raise exceptions
    print 'Failed recipients:', failed         # too, but let them pass here
else:
    print 'No errors.'
print 'Bye.' 
