###############################################################################
# send messages, add attachments (see __init__ for docs, test)
###############################################################################

import mailconfig                                      # client's mailconfig
import smtplib, os, mimetypes                          # mime: name to type
import email.Utils, email.Encoders                     # date string, base64
from mailTool import MailTool, SilentMailTool

from email.Message       import Message                # general message
from email.MIMEMultipart import MIMEMultipart          # type-specific messages
from email.MIMEAudio     import MIMEAudio
from email.MIMEImage     import MIMEImage
from email.MIMEText      import MIMEText
from email.MIMEBase      import MIMEBase

class MailSender(MailTool):
    """
    send mail: format message, interface with SMTP server
    works on any machine with Python+Inet, doesn't use cmdline mail
    a non-authenticating client: see MailSenderAuth if login required
    """
    def __init__(self, smtpserver=None):
        self.smtpServerName  = smtpserver or mailconfig.smtpservername

    def sendMessage(self, From, To, Subj, extrahdrs, bodytext, attaches,
                                            saveMailSeparator=(('='*80)+'PY\n')):
        """
        format,send mail: blocks caller, thread me in a gui
        bodytext is main text part, attaches is list of filenames
        extrahdrs is list of (name, value) tuples to be added
        raises uncaught exception if send fails for any reason
        saves sent message text in a local file if successful
        
        assumes that To, Cc, Bcc hdr values are lists of 1 or more already
        stripped addresses (possibly in full name+<addr> format); client
        must split these on delimiters, parse, or use multi-line input;
        note that smtp allows full name+<addr> format in recipients
        """
        if not attaches:
            msg = Message()
            msg.set_payload(bodytext)
        else:
            msg = MIMEMultipart()
            self.addAttachments(msg, bodytext, attaches)

        recip = To
        msg['From']    = From
        msg['To']      = ', '.join(To)              # poss many: addr list
        msg['Subject'] = Subj                       # servers reject ';' sept
        msg['Date']    = email.Utils.formatdate()   # curr datetime, rfc2822 utc
        for name, value in extrahdrs:               # Cc, Bcc, X-Mailer, etc.
            if value:
                if name.lower() not in ['cc', 'bcc']:
                    msg[name] = value
                else:
                    msg[name] = ', '.join(value)    # add commas between
                    recip += value                  # some servers reject ['']
        fullText = msg.as_string()                  # generate formatted msg

        # sendmail call raises except if all Tos failed,
        # or returns failed Tos dict for any that failed
        
        self.trace('Sending to...'+ str(recip))
        self.trace(fullText[:256])
        server = smtplib.SMTP(self.smtpServerName)           # this may fail too
        self.getPassword()                                   # if srvr requires
        self.authenticateServer(server)                      # login in subclass
        try:
            failed = server.sendmail(From, recip, fullText)  # except or dict
        finally:
            server.quit()                                    # iff connect okay
        if failed:
            class SomeAddrsFailed(Exception): pass
            raise SomeAddrsFailed('Failed addrs:%s\n' % failed)
        self.saveSentMessage(fullText, saveMailSeparator)
        self.trace('Send exit')
        
    def addAttachments(self, mainmsg, bodytext, attaches):
        # format a multi-part message with attachments
        msg = MIMEText(bodytext)                 # add main text/plain part
        mainmsg.attach(msg)
        for filename in attaches:                # absolute or relative paths
            if not os.path.isfile(filename):     # skip dirs, etc.
                continue
            
            # guess content type from file extension, ignore encoding
            contype, encoding = mimetypes.guess_type(filename)
            if contype is None or encoding is not None:  # no guess, compressed?
                contype = 'application/octet-stream'     # use generic default
            self.trace('Adding ' + contype)

            # build sub-Message of apropriate kind
            maintype, subtype = contype.split('/', 1)
            if maintype == 'text':
                data = open(filename, 'r')
                msg  = MIMEText(data.read(), _subtype=subtype)
                data.close()
            elif maintype == 'image':
                data = open(filename, 'rb')
                msg  = MIMEImage(data.read(), _subtype=subtype)
                data.close()
            elif maintype == 'audio':
                data = open(filename, 'rb')
                msg  = MIMEAudio(data.read(), _subtype=subtype)
                data.close()
            else:
                data = open(filename, 'rb')
                msg  = MIMEBase(maintype, subtype)
                msg.set_payload(data.read())
                data.close()                            # make generic type
                email.Encoders.encode_base64(msg)       # encode using Base64

            # set filename and attach to container
            basename = os.path.basename(filename)
            msg.add_header('Content-Disposition',
                           'attachment', filename=basename)
            mainmsg.attach(msg)

        # text outside mime structure, seen by non-MIME mail readers
        mainmsg.preamble = 'A multi-part MIME format message.\n'
        mainmsg.epilogue = ''  # make sure message ends with a newline

    def saveSentMessage(self, fullText, saveMailSeparator):
        # append sent message to local file if worked
        # client: pass separator used for your app, splits
        # caveat: user may change file at same time (unlikely)
        try:
            sentfile = open(mailconfig.sentmailfile, 'a')
            if fullText[-1] != '\n': fullText += '\n'
            sentfile.write(saveMailSeparator)
            sentfile.write(fullText)
            sentfile.close()
        except:
            self.trace('Could not save sent message')    # not a show-stopper

    def authenticateServer(self, server):
        pass  # no login required for this server/class

    def getPassword(self): 
        pass  # no login required for this server/class


################################################################################
# specialized subclasses
################################################################################

class MailSenderAuth(MailSender):
    """
    use for servers that require login authorization;
    client: choose MailSender or MailSenderAuth super
    class based on mailconfig.smtpuser setting (None?)
    """
    def __init__(self, smtpserver=None, smtpuser=None):
        MailSender.__init__(self, smtpserver)
        self.smtpUser = smtpuser or mailconfig.smtpuser
        self.smtpPassword = None
        
    def authenticateServer(self, server):
        server.login(self.smtpUser, self.smtpPassword)
        
    def getPassword(self):
        """
        get smtp auth password if not yet known;
        may be called by superclass auto, or client manual:
        not needed until send, but don't run in GUI thread;
        get from client-side file or subclass method
        """
        if not self.smtpPassword:
            try:
                localfile = open(mailconfig.smtppasswdfile)
                self.smtpPassword = localfile.readline()[:-1]
                self.trace('local file password' + repr(self.smtpPassword))
            except:
                self.smtpPassword = self.askSmtpPassword()

    def askSmtpPassword(self):
        assert False, 'Subclass must define method'

class MailSenderAuthConsole(MailSender):
    def askSmtpPassword(self):
        import getpass
        prompt = 'Password for %s on %s?' % (self.smtpUser, self.smtpServerName)
        return getpass.getpass(prompt)

class SilentMailSender(SilentMailTool, MailSender):
    pass   # replaces trace
