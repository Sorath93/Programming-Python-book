###############################################################################
# Implementation of mail-server and save-file message list main windows:
# one class per kind.  Code is factored here for reuse: server and file
# list windows are customized versions of the PyMaiCommon list window class;
# the server window maps actions to mail transfered from a server, and the
# file window applies actions to a local file.  List windows create View,
# Write, Reply, and Forward windows on user actions.  The server list window
# is the main window opened on program start-up by the top-level file;  file
# list windows are opened on demand via server and file list window "Open".
# Msgnums may be temporarily out of synch with server if pop inbox changes.
#
# Changes here in 2.1:
# -now checks on deletes and loads to see if msg nums in synch with server
# -added up to N attachment direct-access buttons on view windows
# -threaded save-mail file loads, to avoid N-second pause for big files
# -also threads save-mail file deletes so file write doesn't pause gui
# TBD:
# -save-mail file saves still not threaded: may pause gui briefly, but
#  uncommon - unlike load and delete, save/send only appends the local file.
# -implementation of local save-mail files as text files with separators
#  is mostly a prototype: it loads all full mails into memory, and so limits
#  the practical size of these files; better alternative: use 2 dbm keyed
#  access files for hdrs and fulltext, plus a list to map keys to position;
#  in this scheme save-mail files become directories, no longer readable.
###############################################################################

from SharedNames import *     # program-wide global objects
from ViewWindows import ViewWindow, WriteWindow, ReplyWindow, ForwardWindow


###############################################################################
# main frame - general structure for both file and server message lists
###############################################################################


class PyMailCommon(mailtools.MailParser):
    """
    a widget package, with main mail listbox
    mixed in with a Tk, Toplevel, or Frame
    must be customized with actions() and other
    creates view and write windows: MailSenders
    """
    # class attrs shared by all list windows
    threadLoopStarted = False                     # started by first window

    # all windows use same dialogs: remember last dirs
    openDialog = Open(title=appname + ': Open Mail File')
    saveDialog = SaveAs(title=appname + ': Append Mail File')

    def __init__(self):
        self.makeWidgets()                        # draw my contents: list,tools
        if not PyMailCommon.threadLoopStarted:    # server,file can both thread
            PyMailCommon.threadLoopStarted = True # start thread exit check loop
            threadtools.threadChecker(self)       # just one for all windows
        
    def makeWidgets(self):
        # add all/none checkbtn at bottom
        tools = Frame(self)
        tools.pack(side=BOTTOM, fill=X)
        self.allModeVar = IntVar()
        chk = Checkbutton(tools, text="All")
        chk.config(variable=self.allModeVar, command=self.onCheckAll)
        chk.pack(side=RIGHT)

        # add main buttons at bottom
        for (title, callback) in self.actions():
            Button(tools, text=title, command=callback).pack(side=LEFT, fill=X)

        # add multi-select listbox with scrollbars
        mails    = Frame(self)
        vscroll  = Scrollbar(mails)
        hscroll  = Scrollbar(mails, orient='horizontal')
        fontsz   = (sys.platform[:3] == 'win' and 8) or 10      # defaults
        listbg   = mailconfig.listbg   or 'white'
        listfg   = mailconfig.listfg   or 'black'
        listfont = mailconfig.listfont or ('courier', fontsz, 'normal')
        listbox  = Listbox(mails, bg=listbg, fg=listfg, font=listfont)
        listbox.config(selectmode=EXTENDED)
        listbox.bind('<Double-1>', (lambda event: self.onViewRawMail()))

        # crosslink listbox and scrollbars
        vscroll.config(command=listbox.yview, relief=SUNKEN)
        hscroll.config(command=listbox.xview, relief=SUNKEN)
        listbox.config(yscrollcommand=vscroll.set, relief=SUNKEN)
        listbox.config(xscrollcommand=hscroll.set)

        # pack last = clip first
        mails.pack(side=TOP, expand=YES, fill=BOTH)
        vscroll.pack(side=RIGHT,  fill=BOTH)
        hscroll.pack(side=BOTTOM, fill=BOTH)
        listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        self.listBox = listbox

    #################
    # event handlers
    #################
    
    def onCheckAll(self):
        # all or none click
        if self.allModeVar.get():
            self.listBox.select_set(0, END)
        else:
            self.listBox.select_clear(0, END)

    def onViewRawMail(self):
        # possibly threaded: view selected messages - raw text headers, body
        msgnums = self.verifySelectedMsgs()
        if msgnums:
            self.getMessages(msgnums, after=lambda: self.contViewRaw(msgnums))

    def contViewRaw(self, msgnums):
        for msgnum in msgnums:                       # could be a nested def 
            fulltext = self.getMessage(msgnum)       # put in ScrolledText
            from ScrolledText import ScrolledText    # dont need full TextEditor
            window  = windows.QuietPopupWindow(appname, 'raw message viewer')
            browser = ScrolledText(window)
            browser.insert('0.0', fulltext)
            browser.pack(expand=YES, fill=BOTH)

    def onViewFormatMail(self):
        """
        possibly threaded: view selected messages - popup formatted display                
        not threaded if in savefile list, or messages are already loaded
        the after action runs only if getMessages prefetch allowed and worked
        """
        msgnums = self.verifySelectedMsgs()
        if msgnums:
            self.getMessages(msgnums, after=lambda: self.contViewFmt(msgnums))

    def contViewFmt(self, msgnums):
        for msgnum in msgnums:
            fulltext = self.getMessage(msgnum)
            message  = self.parseMessage(fulltext)
            type, content = self.findMainText(message)
            content  = wraplines.wrapText1(content, mailconfig.wrapsz)
            ViewWindow(headermap   = message,
                       showtext    = content,
                       origmessage = message)

            # non-multipart, content-type text/html (rude but true!)
            # can also be opened manually from Split or part button
            # if non-multipart, other: must open part manually with
            # Split or part button; no verify if mailconfig says so;
            
            if type == 'text/html':
                if ((not mailconfig.verifyHTMLTextOpen) or
                    askyesno(appname, 'Open message text in browser?')):
                    try:
                        from tempfile import gettempdir # or a Tk html viewer?
                        tempname = os.path.join(gettempdir(), 'pymailgui.html')
                        open(tempname, 'w').write(content)
                        webbrowser.open_new('file://' + tempname)
                    except:
                        show_error(appname, 'Cannot open in browser')

    def onWriteMail(self):
        # compose new email
        starttext = '\n'                         # use auto signature text
        if mailconfig.mysignature:
            starttext += '%s\n' % mailconfig.mysignature
        WriteWindow(starttext = starttext,
                    headermap = {'From': mailconfig.myaddress})
                       
    def onReplyMail(self):
        # possibly threaded: reply to selected emails
        msgnums = self.verifySelectedMsgs()
        if msgnums:
            self.getMessages(msgnums, after=lambda: self.contReply(msgnums))

    def contReply(self, msgnums):
        for msgnum in msgnums:
            # drop attachments, quote with '>', add signature
            fulltext = self.getMessage(msgnum)
            message  = self.parseMessage(fulltext)         # may fail: error obj
            maintext = self.findMainText(message)[1]
            maintext = wraplines.wrapText1(maintext, mailconfig.wrapsz-2)   # >
            maintext = self.quoteOrigText(maintext, message) 
            if mailconfig.mysignature:
                maintext = ('\n%s\n' % mailconfig.mysignature) + maintext

            # preset initial to/from values from mail or config
            # don't use original To for From: may be many or listname
            # To keeps name+<addr> format unless any ';' present: separator
            # ideally, send should fully parse instead of splitting on ';'
            # send changes ';' to ',' required by servers; ',' common in name
            
            origfrom = message.get('From', '')
            ToPair   = email.Utils.parseaddr(origfrom)     # 1st (name, addr)
            ToStr    = email.Utils.formataddr(ToPair)      # ignore Reply-to
            From     = mailconfig.myaddress                # don't try 'To'
            Subj     = message.get('Subject', '(no subject)')
            if not Subj.startswith('Re:'):
                Subj = 'Re: ' + Subj
            if ';' not in ToStr:                           # uses separator?
                To = ToStr                                 # use name+addr
            else:
                To = ToPair[1]                             # use just addr
            ReplyWindow(starttext = maintext,
                        headermap = {'From': From, 'To': To, 'Subject': Subj})

    def onFwdMail(self):
        # possibly threaded: forward selected emails
        msgnums = self.verifySelectedMsgs()
        if msgnums:
            self.getMessages(msgnums, after=lambda: self.contFwd(msgnums))

    def contFwd(self, msgnums):
        for msgnum in msgnums:
            # drop attachments, quote with '>', add signature
            fulltext = self.getMessage(msgnum)
            message  = self.parseMessage(fulltext)
            maintext = self.findMainText(message)[1]
            maintext = wraplines.wrapText1(maintext, mailconfig.wrapsz-2)
            maintext = self.quoteOrigText(maintext, message)
            if mailconfig.mysignature:
                maintext = ('\n%s\n' % mailconfig.mysignature) + maintext

            # initial from value from config, not mail
            From = mailconfig.myaddress
            Subj = message.get('Subject', '(no subject)')
            if not Subj.startswith('Fwd: '):
                Subj = 'Fwd: ' + Subj
            ForwardWindow(starttext = maintext,
                          headermap = {'From': From, 'Subject': Subj})
            
    def onSaveMailFile(self): 
        """
        save selected emails for offline viewing
        disabled if target file load/delete is in progress
        disabled by getMessages if self is a busy file too
        contSave not threaded: disables all other actions
        """
        msgnums = self.selectedMsgs()
        if not msgnums:
            showerror(appname, 'No message selected')
        else:
            # caveat: dialog warns about replacing file
            filename = self.saveDialog.show()             # shared class attr
            if filename:                                  # dont verify num msgs
                filename = os.path.abspath(filename)      # normalize / to \ 
                self.getMessages(msgnums,
                        after=lambda: self.contSave(msgnums, filename))

    def contSave(self, msgnums, filename):
        # test busy now, after poss srvr msgs load
        if (filename in openSaveFiles.keys() and           # viewing this file?
            openSaveFiles[filename].openFileBusy):         # load/del occurring?
            showerror(appname, 'Target file busy - cannot save')
        else:
            try:
                fulltextlist = []
                mailfile = open(filename, 'a')             # caveat:not threaded
                for msgnum in msgnums:                     # < 1sec for N megs
                    fulltext = self.getMessage(msgnum)     # but poss many msgs
                    if fulltext[-1] != '\n': fulltext += '\n'
                    mailfile.write(saveMailSeparator)
                    mailfile.write(fulltext)
                    fulltextlist.append(fulltext)
                mailfile.close()
            except:
                showerror(appname, 'Error during save')
                printStack(sys.exc_info())
            else:                                          # why .keys(): EIBTI
                if filename in openSaveFiles.keys():       # viewing this file?
                    window = openSaveFiles[filename]       # update list, raise
                    window.addSavedMails(fulltextlist)     # avoid file reload
                    #window.loadMailFileThread()           # this was very slow

    def onOpenMailFile(self, filename=None):
        # process saved mail offline
        filename = filename or self.openDialog.show()      # shared class attr
        if filename:
            filename = os.path.abspath(filename)           # match on full name 
            if openSaveFiles.has_key(filename):            # only 1 win per file
                openSaveFiles[filename].lift()             # raise file's window
                showinfo(appname, 'File already open')     # else deletes odd
            else:
                from PyMailGui2 import PyMailFileWindow    # avoid duplicate win
                popup = PyMailFileWindow(filename)         # new list window
                openSaveFiles[filename] = popup            # removed in quit
                popup.loadMailFileThread()                 # try load in thread

    def onDeleteMail(self):
        # delete selected mails from server or file
        msgnums = self.selectedMsgs()                      # subclass: fillIndex
        if not msgnums:                                    # always verify here
            showerror(appname, 'No message selected')
        else:
            if askyesno(appname, 'Verify delete %d mails?' % len(msgnums)):
                self.doDelete(msgnums)
                
    ##################
    # utility methods
    ##################
    
    def selectedMsgs(self):
        # get messages selected in main listbox
        selections = self.listBox.curselection()  # tuple of digit strs, 0..N-1
        return [int(x)+1 for x in selections]     # convert to ints, make 1..N

    warningLimit = 15
    def verifySelectedMsgs(self):
        msgnums = self.selectedMsgs()
        if not msgnums:
            showerror(appname, 'No message selected')
        else:
            numselects = len(msgnums)
            if numselects > self.warningLimit:
                if not askyesno(appname, 'Open %d selections?' % numselects):
                    msgnums = []
        return msgnums

    def fillIndex(self, maxhdrsize=25):
        # fill all of main listbox
        hdrmaps  = self.headersMaps()                   # may be empty
        showhdrs = ('Subject', 'From', 'Date', 'To')    # default hdrs to show
        if hasattr(mailconfig, 'listheaders'):          # mailconfig customizes
            showhdrs = mailconfig.listheaders or showhdrs

        # compute max field sizes <= hdrsize
        maxsize = {}
        for key in showhdrs:
            allLens = [len(msg.get(key, '')) for msg in hdrmaps]
            if not allLens: allLens = [1]
            maxsize[key] = min(maxhdrsize, max(allLens))         

        # populate listbox with fixed-width left-justified fields
        self.listBox.delete(0, END)                     # show multiparts with *
        for (ix, msg) in enumerate(hdrmaps):            # via content-type hdr     
            msgtype = msg.get_content_maintype()        # no is_multipart yet
            msgline = (msgtype == 'multipart' and '*') or ' '
            msgline += '%03d' % (ix+1)
            for key in showhdrs:
                mysize  = maxsize[key]
                keytext = msg.get(key, ' ')
                msgline += ' | %-*s' % (mysize, keytext[:mysize])
            msgline += '| %.1fK' % (self.mailSize(ix+1) / 1024.0)
            self.listBox.insert(END, msgline)
        self.listBox.see(END)         # show most recent mail=last line 

    def quoteOrigText(self, maintext, message):
        quoted   = '\n-----Original Message-----\n'
        for hdr in ('From', 'To', 'Subject', 'Date'):
            quoted += '%s: %s\n' % (hdr, message.get(hdr, '?'))
        quoted   = quoted + '\n' + maintext
        quoted   = '\n' + quoted.replace('\n', '\n> ')
        return quoted

    ########################
    # subclass requirements
    ########################

    def getMessages(self, msgnums, after):        # used by view,save,reply,fwd
        after()                                   # redef if cache, thread test 

    # plus okayToQuit?, any unique actions
    def getMessage(self, msgnum): assert False    # used by many: full mail text 
    def headersMaps(self): assert False           # fillIndex: hdr mappings list
    def mailSize(self, msgnum): assert False      # fillIndex: size of msgnum
    def doDelete(self): assert False              # onDeleteMail: delete button


###############################################################################
# main window - when viewing messages in local save file (or sent-mail file)
###############################################################################


class PyMailFile(PyMailCommon):
    """
    customize for viewing saved-mail file offline
    a Tk, Toplevel, or Frame, with main mail listbox
    opens and deletes run in threads for large files
    
    save and send not threaded, because only append to
    file; save is disabled if source or target file busy
    with load/delete; save disables load, delete, save
    just because it is not run in a thread (blocks gui);
    
    TBD: may need thread and o/s file locks if saves ever
    do run in threads: saves could disable other threads
    with openFileBusy, but file may not be open in gui;
    file locks not sufficient, because gui updated too;
    TBD: appends to sent-mail file may require o/s locks:
    as is, user gets error popup if sent during load/del;
    """
    def actions(self):
        return [ ('View',   self.onViewFormatMail),
                 ('Delete', self.onDeleteMail),
                 ('Write',  self.onWriteMail), 
                 ('Reply',  self.onReplyMail), 
                 ('Fwd',    self.onFwdMail),
                 ('Save',   self.onSaveMailFile),  
                 ('Open',   self.onOpenMailFile),
                 ('Quit',   self.quit) ]
    
    def __init__(self, filename):
        # caller: do loadMailFileThread next
        PyMailCommon.__init__(self)
        self.filename = filename
        self.openFileBusy = threadtools.ThreadCounter()      # one per window
        
    def loadMailFileThread(self):
        """
        Load or reload file and update window index list;
        called on Open, startup, and possibly on Send if
        sent-mail file appended is currently open;  there
        is always a bogus first item after the text split;
        alt: [self.parseHeaders(m) for m in self.msglist];
        could popup a busy dialog, but quick for small files;

        2.1: this is now threaded--else runs < 1sec for N meg
        files, but can pause gui N seconds if very large file;
        Save now uses addSavedMails to append msg lists for
        speed, not this reload;  still called from Send just
        because msg text unavailable - requires refactoring;
        delete threaded too: prevent open and delete overlap;
        """
        if self.openFileBusy:
            # dont allow parallel open/delete changes
            errmsg = 'Cannot load, file is busy:\n"%s"' % self.filename
            showerror(appname, errmsg)
        else:
            #self.listBox.insert(END, 'loading...')      # error if user clicks
            savetitle = self.title()                     # set by window class
            self.title(appname + ' - ' + 'Loading...')
            self.openFileBusy.incr()
            threadtools.startThread(
                action     = self.loadMailFile,
                args       = (),
                context    = (savetitle,),
                onExit     = self.onLoadMailFileExit,
                onFail     = self.onLoadMailFileFail)

    def loadMailFile(self):
        # run in a thread while gui is active
        # open, read, parser may all raise excs
        allmsgs = open(self.filename).read()
        self.msglist  = allmsgs.split(saveMailSeparator)[1:]      # full text
        self.hdrlist  = map(self.parseHeaders, self.msglist)      # msg objects

    def onLoadMailFileExit(self, savetitle):
        # on thread success
        self.title(savetitle)         # reset window title to filename
        self.fillIndex()              # updates gui: do in main thread
        self.lift()                   # raise my window
        self.openFileBusy.decr()

    def onLoadMailFileFail(self, exc_info, savetitle):
        # on thread exception
        showerror(appname, 'Error opening "%s"\n%s\n%s' %
                           ((self.filename,) +  exc_info[:2]))
        printStack(exc_info)
        self.destroy()                # always close my window?
        self.openFileBusy.decr()      # not needed if destroy

    def addSavedMails(self, fulltextlist):
        """
        optimization: extend loaded file lists for mails
        newly saved to this window's file; in past called
        loadMailThread to reload entire file on save - slow;
        must be called in main GUI thread only: updates GUI;
        sends still reloads sent file if open: no msg text;
        """
        self.msglist.extend(fulltextlist)
        self.hdrlist.extend(map(self.parseHeaders, fulltextlist))
        self.fillIndex()
        self.lift()
        
    def doDelete(self, msgnums):
        """
        simple-minded, but sufficient: rewrite all
        non-deleted mails to file; can't just delete
        from self.msglist in-place: changes item indexes;
        Py2.3 enumerate(L) same as zip(range(len(L)), L)
        2.1: now threaded, else N sec pause for large files
        """
        if self.openFileBusy:
            # dont allow parallel open/delete changes
            errmsg = 'Cannot delete, file is busy:\n"%s"' % self.filename
            showerror(appname, errmsg)
        else:
            savetitle = self.title()
            self.title(appname + ' - ' + 'Deleting...')
            self.openFileBusy.incr()
            threadtools.startThread(
                action     = self.deleteMailFile,
                args       = (msgnums,),
                context    = (savetitle,),
                onExit     = self.onDeleteMailFileExit,
                onFail     = self.onDeleteMailFileFail)

    def deleteMailFile(self, msgnums):
        # run in a thread while gui active
        indexed = enumerate(self.msglist)
        keepers = [msg for (ix, msg) in indexed if ix+1 not in msgnums]
        allmsgs = saveMailSeparator.join([''] + keepers)
        open(self.filename, 'w').write(allmsgs)
        self.msglist = keepers
        self.hdrlist = map(self.parseHeaders, self.msglist)

    def onDeleteMailFileExit(self, savetitle):
        self.title(savetitle)
        self.fillIndex()              # updates gui: do in main thread
        self.lift()                   # reset my title, raise my window
        self.openFileBusy.decr()

    def onDeleteMailFileFail(self, exc_info, savetitle):
        showerror(appname, 'Error deleting "%s"\n%s\n%s' %
                           ((self.filename,) +  exc_info[:2]))
        printStack(exc_info)
        self.destroy()                # always close my window?
        self.openFileBusy.decr()      # not needed if destroy
                                                  
    def getMessages(self, msgnums, after):
        """
        used by view,save,reply,fwd: file load and delete
        threads may change the msg and hdr lists, so disable
        all other operations that depend on them to be safe;
        this test is for self: saves also test target file;
        """
        if self.openFileBusy:
            errmsg = 'Cannot fetch, file is busy:\n"%s"' % self.filename
            showerror(appname, errmsg)
        else:
            after()                      # mail already loaded 

    def getMessage(self, msgnum):
        return self.msglist[msgnum-1]    # full text of 1 mail

    def headersMaps(self):
        return self.hdrlist              # email.Message objects
    
    def mailSize(self, msgnum):
        return len(self.msglist[msgnum-1])

    def quit(self):
        # dont destroy during update: fillIndex next
        if self.openFileBusy:   
            showerror(appname, 'Cannot quit during load or delete')
        else:
            if askyesno(appname, 'Verify Quit Window?'):
                # delete file from open list
                del openSaveFiles[self.filename]
                Toplevel.destroy(self)


###############################################################################
# main window - when viewing messages on the mail server
###############################################################################


class PyMailServer(PyMailCommon):
    """
    customize for viewing mail still on server
    a Tk, Toplevel, or Frame, with main mail listbox
    maps load, fetch, delete actions to server inbox
    embeds a MessageCache, which is a MailFetcher
    """
    def actions(self):
        return [ ('Load',   self.onLoadServer),  
                 ('View',   self.onViewFormatMail),
                 ('Delete', self.onDeleteMail),
                 ('Write',  self.onWriteMail), 
                 ('Reply',  self.onReplyMail), 
                 ('Fwd',    self.onFwdMail),
                 ('Save',   self.onSaveMailFile),  
                 ('Open',   self.onOpenMailFile),
                 ('Quit',   self.quit) ]

    def __init__(self):
        PyMailCommon.__init__(self)
        self.cache = messagecache.GuiMessageCache()    # embedded, not inherited
       #self.listBox.insert(END, 'Press Load to fetch mail')
        
    def makeWidgets(self):                             # help bar: main win only
        self.addHelp()
        PyMailCommon.makeWidgets(self)

    def addHelp(self):
        msg = 'PyMailGUI - a Python/Tkinter email client  (help)'
        title = Button(self, text=msg)
        title.config(bg='steelblue', fg='white', relief=RIDGE)
        title.config(command=self.onShowHelp)
        title.pack(fill=X)

    def onShowHelp(self):
        """
        load,show text block string
        could use HTML and webbrowser module here too
        but that adds an external dependency
        """
        from PyMailGuiHelp import helptext
        popuputil.HelpPopup(appname, helptext, showsource=self.onShowMySource)

    def onShowMySource(self, showAsMail=False):
        # display my sourcecode file, plus imported modules here & elsewhere
        import PyMailGui2, ListWindows, ViewWindows, SharedNames
        from PP3E.Internet.Email.mailtools import (    # mailtools now a pkg
             mailSender, mailFetcher, mailParser)      # can't use * in def
        mymods = (
            PyMailGui2, ListWindows, ViewWindows, SharedNames,
            PyMailGuiHelp, popuputil, messagecache, wraplines,
            mailtools, mailFetcher, mailSender, mailParser,
            mailconfig, threadtools, windows, textEditor)
        for mod in mymods:
            source = mod.__file__
            if source.endswith('.pyc'):
                source = source[:-4] + '.py'       # assume in same dir, .py
            if showAsMail:
                # this is a bit cheesey...
                code   = open(source).read()
                user   = mailconfig.myaddress
                hdrmap = {'From': appname, 'To': user, 'Subject': mod.__name__}
                ViewWindow(showtext=code,
                           headermap=hdrmap,
                           origmessage=email.Message.Message())
            else:
                # more useful text editor
                wintitle = ' - ' + mod.__name__
                textEditor.TextEditorMainPopup(self, source, wintitle)

    def onLoadServer(self, forceReload=False):
        """
        threaded: load or reload mail headers list on request
        Exit,Fail,Progress run by threadChecker after callback via queue
        may overlap with sends, disables all but send
        could overlap with loadingmsgs, but may change msg cache list
        forceReload on delete/synch fail, else loads recent arrivals only;
        2.1: cache.loadHeaders may do quick check to see if msgnums
        in synch with server, if we are loading just newly-arrived hdrs;
        """
        if loadingHdrsBusy or deletingBusy or loadingMsgsBusy:
            showerror(appname, 'Cannot load headers during load or delete')
        else:
            loadingHdrsBusy.incr()
            self.cache.setPopPassword(appname) # don't update gui in the thread!
            popup = popuputil.BusyBoxNowait(appname, 'Loading message headers')
            threadtools.startThread(
                action     = self.cache.loadHeaders,
                args       = (forceReload,),
                context    = (popup,),
                onExit     = self.onLoadHdrsExit,
                onFail     = self.onLoadHdrsFail,
                onProgress = self.onLoadHdrsProgress)

    def onLoadHdrsExit(self, popup):
        self.fillIndex()
        popup.quit()
        self.lift()
        loadingHdrsBusy.decr()

    def onLoadHdrsFail(self, exc_info, popup):
        popup.quit()
        showerror(appname, 'Load failed: \n%s\n%s' % exc_info[:2])
        printStack(exc_info)                       # send stack trace to stdout
        loadingHdrsBusy.decr()
        if exc_info[0] == mailtools.MessageSynchError:    # synch inbox/index 
            self.onLoadServer(forceReload=True)           # new thread: reload
        else:
            self.cache.popPassword = None          # force re-input next time
            
    def onLoadHdrsProgress(self, i, n, popup):
        popup.changeText('%d of %d' % (i, n))

    def doDelete(self, msgnumlist):
        """
        threaded: delete from server now - changes msg nums;
        may overlap with sends only, disables all except sends;
        2.1: cache.deleteMessages now checks TOP result to see
        if headers match selected mails, in case msgnums out of
        synch with mail server: poss if mail deleted by other client,
        or server deletes inbox mail automatically - some isps may
        move a mail from inbox to undeliverable on load failure;
        """
        if loadingHdrsBusy or deletingBusy or loadingMsgsBusy:
            showerror(appname, 'Cannot delete during load or delete')
        else:
            deletingBusy.incr()
            popup = popuputil.BusyBoxNowait(appname, 'Deleting selected mails')
            threadtools.startThread(
                action     = self.cache.deleteMessages,
                args       = (msgnumlist,),
                context    = (popup,),
                onExit     = self.onDeleteExit,
                onFail     = self.onDeleteFail,
                onProgress = self.onDeleteProgress)

    def onDeleteExit(self, popup):
        self.fillIndex()                     # no need to reload from server
        popup.quit()                         # refill index with updated cache
        self.lift()                          # raise index window, release lock
        deletingBusy.decr()                   
        
    def onDeleteFail(self, exc_info, popup):
        popup.quit()
        showerror(appname, 'Delete failed: \n%s\n%s' % exc_info[:2])
        printStack(exc_info)
        deletingBusy.decr()                  # delete or synch check failure
        self.onLoadServer(forceReload=True)  # new thread: some msgnums changed

    def onDeleteProgress(self, i, n, popup):
        popup.changeText('%d of %d' % (i, n))

    def getMessages(self, msgnums, after):
        """
        threaded: prefetch all selected messages into cache now
        used by save, view, reply, and forward to prefill cache
        may overlap with other loadmsgs and sends, disables delete
        only runs "after" action if the fetch allowed and successful;
        2.1: cache.getMessages tests if index in synch with server,
        but we only test if we have to go to server, not if cached;
        """
        if loadingHdrsBusy or deletingBusy:
            showerror(appname, 'Cannot fetch message during load or delete')
        else:
            toLoad = [num for num in msgnums if not self.cache.isLoaded(num)]
            if not toLoad:
                after()         # all already loaded
                return          # process now, no wait popup
            else:
                loadingMsgsBusy.incr()
                from popuputil import BusyBoxNowait
                popup = BusyBoxNowait(appname, 'Fetching message contents')
                threadtools.startThread(
                    action     = self.cache.getMessages,
                    args       = (toLoad,),
                    context    = (after, popup),
                    onExit     = self.onLoadMsgsExit,
                    onFail     = self.onLoadMsgsFail,
                    onProgress = self.onLoadMsgsProgress)

    def onLoadMsgsExit(self, after, popup):
        popup.quit()
        after()
        loadingMsgsBusy.decr()    # allow others after afterExit done

    def onLoadMsgsFail(self, exc_info, after, popup):
        popup.quit()
        showerror(appname, 'Fetch failed: \n%s\n%s' % exc_info[:2])
        printStack(exc_info)
        loadingMsgsBusy.decr()
        if exc_info[0] == mailtools.MessageSynchError:      # synch inbox/index 
            self.onLoadServer(forceReload=True)             # new thread: reload
        
    def onLoadMsgsProgress(self, i, n, after, popup):
        popup.changeText('%d of %d' % (i, n))

    def getMessage(self, msgnum):
        return self.cache.getMessage(msgnum)                # full mail text

    def headersMaps(self):
        return map(self.parseHeaders, self.cache.allHdrs()) # email.Message objs

    def mailSize(self, msgnum):
        return self.cache.getSize(msgnum)
        
    def okayToQuit(self):
        # any threads still running?
        filesbusy = [win for win in openSaveFiles.values() if win.openFileBusy]
        busy = loadingHdrsBusy or deletingBusy or sendingBusy or loadingMsgsBusy
        busy = busy or filesbusy
        return not busy
