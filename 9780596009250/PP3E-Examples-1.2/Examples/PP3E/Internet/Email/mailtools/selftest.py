###############################################################################
# self-test when this file is run as a program
###############################################################################

#
# mailconfig normally comes from the client's source directory or
# sys.path; for testing, get it from Email directory one level up
#
import sys
sys.path.append('..')
import mailconfig
print 'config:', mailconfig.__file__

# get these from __init__
from mailtools import MailFetcherConsole, MailSender, MailSenderAuthConsole

if not mailconfig.smtpuser:
    sender = MailSender()
else:
    sender = MailSenderAuthConsole()
    
sender.sendMessage(From      = mailconfig.myaddress,
                   To        = [mailconfig.myaddress],
                   Subj      = 'testing 123',
                   extrahdrs = [('X-Mailer', 'mailtools')],
                   bodytext  = 'Here is my source code',
                   attaches  = ['selftest.py'])

fetcher = MailFetcherConsole()
def status(*args): print args

hdrs, sizes, loadedall = fetcher.downloadAllHeaders(status)
for num, hdr in enumerate(hdrs[:5]):
    print hdr
    if raw_input('load mail?') in ['y', 'Y']:
        print fetcher.downloadMessage(num+1), '\n', '-'*70

last5 = len(hdrs)-4
msgs, sizes, loadedall = fetcher.downloadAllMessages(status, loadfrom=last5)
for msg in msgs:
    print msg[:200], '\n', '-'*70
raw_input('Press Enter to exit')
