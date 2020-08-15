#####################################################
# scan pop email box, fetching just headers, allowing
# deletions without downloading the complete message
#####################################################

import poplib, getpass, sys

mailserver = 'pop.earthlink.net'
mailuser   = 'pp3e'
mailpasswd = getpass.getpass('Password for %s?' % mailserver)

print 'Connecting...'
server = poplib.POP3(mailserver)
server.user(mailuser)                      
server.pass_(mailpasswd)                   

try:
    print server.getwelcome()
    msgCount, mboxSize = server.stat()
    print 'There are', msgCount, 'mail messages, size ', mboxSize
    msginfo = server.list()
    print msginfo
    for i in range(msgCount):
        msgnum  = i+1
        msgsize = msginfo[1][i].split()[1]
        resp, hdrlines, octets = server.top(msgnum, 0)         # get hdrs only
        print '-'*80
        print '[%d: octets=%d, size=%s]' % (msgnum, octets, msgsize) 
        for line in hdrlines: print line

        if raw_input('Print?') in ['y', 'Y']:
            for line in server.retr(msgnum)[1]: print line     # get whole msg
        if raw_input('Delete?') in ['y', 'Y']:
            print 'deleting'
            server.dele(msgnum)                                # delete on srvr
        else:
            print 'skipping'
finally: 
    server.quit()                                  # make sure we unlock mbox
raw_input('Bye.')                                  # keep window up on windows


