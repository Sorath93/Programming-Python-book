#!/usr/local/bin/python
##########################################################################
# pymail - a simple console email interface client in Python; uses Python 
# POP3 mail interface module to view pop email account messages; uses 
# email package modules to extract mail message headers (not rfc822); 
##########################################################################
     
import poplib, smtplib, email.Utils
from email.Parser  import Parser
from email.Message import Message

def inputmessage():
    import sys
    From = raw_input('From? ').strip()             
    To   = raw_input('To?   ').strip()       # datetime hdr set auto         
    To   = To.split(';')                          
    Subj = raw_input('Subj? ').strip()    
    print 'Type message text, end with line="."'
    text = ''
    while True:
        line = sys.stdin.readline()
        if line == '.\n': break
        text += line
    return From, To, Subj, text

def sendmessage():
    From, To, Subj, text = inputmessage()
    msg = Message()
    msg['From']    = From
    msg['To']      = ';'.join(To)
    msg['Subject'] = Subj
    msg['Date']    = email.Utils.formatdate()          # curr datetime, rfc2822
    msg.set_payload(text)
    server = smtplib.SMTP(mailconfig.smtpservername)
    try:
        failed = server.sendmail(From, To, str(msg))   # may also raise exc
    except:
        print 'Error - send failed'
    else:
        if failed: print 'Failed:', failed
         
def connect(servername, user, passwd):
    print 'Connecting...'
    server = poplib.POP3(servername)
    server.user(user)                    # connect, login to mail server
    server.pass_(passwd)                 # pass is a reserved word
    print server.getwelcome()            # print returned greeting message 
    return server
     
def loadmessages(servername, user, passwd, loadfrom=1):
    server = connect(servername, user, passwd)
    try:
        print server.list()
        (msgCount, msgBytes) = server.stat()
        print 'There are', msgCount, 'mail messages in', msgBytes, 'bytes'
        print 'Retrieving:',
        msgList = []
        for i in range(loadfrom, msgCount+1):            # empty if low >= high
            print i,                                     # fetch mail now
            (hdr, message, octets) = server.retr(i)      # save text on list
            msgList.append('\n'.join(message))           # leave mail on server 
        print
    finally:
        server.quit()                                    # unlock the mail box
    assert len(msgList) == (msgCount - loadfrom) + 1     # msg nums start at 1
    return msgList
     
def deletemessages(servername, user, passwd, toDelete, verify=1):
    print 'To be deleted:', toDelete
    if verify and raw_input('Delete?')[:1] not in ['y', 'Y']:
        print 'Delete cancelled.'
    else:
        server = connect(servername, user, passwd)
        try:
            print 'Deleting messages from server.'
            for msgnum in toDelete:                 # reconnect to delete mail
                server.dele(msgnum)                 # mbox locked until quit()
        finally:
            server.quit()
     
def showindex(msgList):
    count = 0                                # show some mail headers
    for msgtext in msgList:
        msghdrs = Parser().parsestr(msgtext, headersonly=True)
        count   = count + 1
        print '%d:\t%d bytes' % (count, len(msgtext))
        for hdr in ('From', 'Date', 'Subject'):
            try:
                print '\t%s=>%s' % (hdr, msghdrs[hdr])
            except KeyError:
                print '\t%s=>(unknown)' % hdr
            #print '\n\t%s=>%s' % (hdr, msghdrs.get(hdr, '(unknown)')
        if count % 5 == 0:
            raw_input('[Press Enter key]')  # pause after each 5 
     
def showmessage(i, msgList):
    if 1 <= i <= len(msgList):
        print '-'*80
        msg = Parser().parsestr(msgList[i-1])
        print msg.get_payload()         # prints payload: string, or [Messages]
       #print msgList[i-1]              # old: prints entire mail--hdrs+text
        print '-'*80                    # to get text only, call file.read()
    else:                               # after rfc822.Message reads hdr lines
        print 'Bad message number'
     
def savemessage(i, mailfile, msgList):
    if 1 <= i <= len(msgList):
        open(mailfile, 'a').write('\n' + msgList[i-1] + '-'*80 + '\n')
    else:
        print 'Bad message number'
     
def msgnum(command):
    try:
        return int(command.split()[1])
    except:
        return -1   # assume this is bad
     
helptext = """
Available commands:
i     - index display
l n?  - list all messages (or just message n)
d n?  - mark all messages for deletion (or just message n)
s n?  - save all messages to a file (or just message n)
m     - compose and send a new mail message
q     - quit pymail
?     - display this help text
"""
     
def interact(msgList, mailfile):
    showindex(msgList)
    toDelete = []
    while 1:
        try:
            command = raw_input('[Pymail] Action? (i, l, d, s, m, q, ?) ')
        except EOFError:
            command = 'q'
     
        # quit
        if not command or command == 'q': 
            break
     
        # index
        elif command[0] == 'i':          
            showindex(msgList)
     
        # list
        elif command[0] == 'l':         
            if len(command) == 1:
                for i in range(1, len(msgList)+1): 
                    showmessage(i, msgList)
            else:
                showmessage(msgnum(command), msgList)
     
        # save
        elif command[0] == 's':        
            if len(command) == 1:
                for i in range(1, len(msgList)+1): 
                    savemessage(i, mailfile, msgList)
            else:
                savemessage(msgnum(command), mailfile, msgList)
     
        # delete 
        elif command[0] == 'd':               
            if len(command) == 1:
                toDelete = range(1, len(msgList)+1)     # delete all later
            else:
                delnum = msgnum(command)
                if (1 <= delnum <= len(msgList)) and (delnum not in toDelete):
                    toDelete.append(delnum)
                else:
                    print 'Bad message number'
     
        # mail
        elif command[0] == 'm':                # send a new mail via smtp
            sendmessage()
            #execfile('smtpmail.py', {})       # alt: run file in own namespace
                 
        elif command[0] == '?':
            print helptext
        else:
            print 'What? -- type "?" for commands help'
    return toDelete
     
if __name__ == '__main__':
    import getpass, mailconfig
    mailserver = mailconfig.popservername        # ex: 'starship.python.net'
    mailuser   = mailconfig.popusername          # ex: 'lutz'
    mailfile   = mailconfig.savemailfile         # ex:  r'c:\stuff\savemail'
    mailpswd   = getpass.getpass('Password for %s?' % mailserver)
    print '[Pymail email client]'
    msgList    = loadmessages(mailserver, mailuser, mailpswd)     # load all
    toDelete   = interact(msgList, mailfile)
    if toDelete: deletemessages(mailserver, mailuser, mailpswd, toDelete)
    print 'Bye.'
