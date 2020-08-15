#############################################################################
# manage message and header loads and context, but not GUI
# a MailFetcher, with a list of already-loaded headers and messages
# the caller must handle any required threading or GUI interfaces
#############################################################################

from PP3E.Internet.Email import mailtools
from popuputil import askPasswordWindow


class MessageInfo:
    """
    an item in the mail cache list
    """
    def __init__(self, hdrtext, size):
        self.hdrtext  = hdrtext            # fulltext is cached msg
        self.fullsize = size               # hdrtext is just the hdrs
        self.fulltext = None               # fulltext=hdrtext if no TOP


class MessageCache(mailtools.MailFetcher):
    """
    keep track of already-loaded headers and messages
    inherits server transfer methods from MailFetcher
    useful in other apps: no GUI or thread assumptions
    """
    def __init__(self):
        mailtools.MailFetcher.__init__(self)
        self.msglist = []

    def loadHeaders(self, forceReloads, progress=None):
        """
        three cases to handle here: the initial full load,
        load newly-arrived, and forced reload after delete;
        don't refetch viewed msgs if hdrs list same or extended;
        retains cached msgs after a delete unless delete fails;
        2.1: does quick check to see if msgnums still in sync
        """
        if forceReloads:
            loadfrom = 1
            self.msglist = []                         # msg nums have chaged   
        else:
            loadfrom = len(self.msglist)+1            # continue from last load

        # only if loading newly-arrived
        if loadfrom != 1:
            self.checkSynchError(self.allHdrs())      # raises except if bad
        
        # get all or newly-arrived msgs
        reply = self.downloadAllHeaders(progress, loadfrom)
        headersList, msgSizes, loadedFull = reply

        for (hdrs, size) in zip(headersList, msgSizes):
            newmsg = MessageInfo(hdrs, size)
            if loadedFull:                            # zip result may be empty
                newmsg.fulltext = hdrs                # got full msg if no 'top'      
            self.msglist.append(newmsg)
 
    def getMessage(self, msgnum):                     # get raw msg text
        if not self.msglist[msgnum-1].fulltext:       # add to cache if fetched
            fulltext = self.downloadMessage(msgnum)   # harmless if threaded
            self.msglist[msgnum-1].fulltext = fulltext
        return self.msglist[msgnum-1].fulltext

    def getMessages(self, msgnums, progress=None):
        """
        prefetch full raw text of multiple messages, in thread;
        2.1: does quick check to see if msgnums still in sync;
        we can't get here unless the index list already loaded;
        """
        self.checkSynchError(self.allHdrs())          # raises except if bad
        nummsgs = len(msgnums)                        # adds messages to cache
        for (ix, msgnum) in enumerate(msgnums):       # some poss already there
             if progress: progress(ix+1, nummsgs)     # only connects if needed
             self.getMessage(msgnum)                  # but may connect > once

    def getSize(self, msgnum):                        # encapsulate cache struct
        return self.msglist[msgnum-1].fullsize        # it changed once already!

    def isLoaded(self, msgnum):
        return self.msglist[msgnum-1].fulltext

    def allHdrs(self):
        return [msg.hdrtext for msg in self.msglist]
    
    def deleteMessages(self, msgnums, progress=None):
        """
        if delete of all msgnums works, remove deleted entries
        from mail cache, but don't reload either the headers list
        or already-viewed mails text: cache list will reflect the
        changed msg nums on server;  if delete fails for any reason,
        caller should forceably reload all hdrs next, because _some_
        server msg nums may have changed, in unpredictable ways;
        2.1: this now checks msg hdrs to detect out of synch msg
        numbers, if TOP supported by mail server; runs in thread
        """
        try:
            self.deleteMessagesSafely(msgnums, self.allHdrs(), progress)
        except mailtools.TopNotSupported:
            mailtools.MailFetcher.deleteMessages(self, msgnums, progress)

        # no errors: update index list
        indexed = enumerate(self.msglist)
        self.msglist = [msg for (ix, msg) in indexed if ix+1 not in msgnums]


class GuiMessageCache(MessageCache):
    """
    add any gui-specific calls here so cache usable in non-gui apps
    """

    def setPopPassword(self, appname):
        """
        get password from gui here, in main thread
        forceably called from gui to avoid popups in threads
        """
        if not self.popPassword:
            prompt = 'Password for %s on %s?' % (self.popUser, self.popServer)
            self.popPassword = askPasswordWindow(appname, prompt)
                            
    def askPopPassword(self):
        """
        but don't use gui popup here: i am run in a thread!
        when tried popup in thread, caused GUI to hang;
        may be called by MailFetcher superclass, but only
        if passwd is still empty string due to dialog close
        """
        return self.popPassword
