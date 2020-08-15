###############################################################################
# Implementation of View, Write, Reply, Forward windows: one class per kind.
# Code is factored here for reuse: a Write window is a cusomized View window,
# and Reply and Forward are custom Write windows.  Windows defined in this
# file are created by the list windows, in response to user actions.  Caveat:
# the 'split' pop-ups for opening parts/attachments feel a bit non-intuitive.
# 2.1: this caveat was addressed, by adding quick-access attachment buttons.
# TBD: could avoid verifying quits unless text area modified (like PyEdit2.0),
# but these windows are larger, and would not catch headers already changed.
# TBD: should Open dialog in write windows be program-wide? (per-window now).
# CHANGE NOV '06: use more platform-neutral grid() for mail headers, not pack()
###############################################################################

from SharedNames import *     # program-wide global objects


###############################################################################
# message view window - also a superclass of write, reply, forward
###############################################################################


class ViewWindow(windows.PopupWindow, mailtools.MailParser):
    """
    a custom Toplevel, with embedded TextEditor
    inherits saveParts,partsList from mailtools.MailParser
    """
    # class attributes
    modelabel       = 'View'                   # used in window titles
    from mailconfig import okayToOpenParts     # open any attachments at all?
    from mailconfig import verifyPartOpens     # ask before open each part?
    from mailconfig import maxPartButtons      # show up to this many + '...'
    tempPartDir     = 'TempParts'              # where 1 selected part saved

    # all view windows use same dialog: remembers last dir
    partsDialog = Directory(title=appname + ': Select parts save directory')

    def __init__(self, headermap, showtext, origmessage=None):
        """
        header map is origmessage, or custom hdr dict for writing;
        showtext is main text part of the message: parsed or custom;
        origmessage is parsed email.Message for view mail windows
        """
        windows.PopupWindow.__init__(self, appname, self.modelabel)
        self.origMessage = origmessage
        self.makeWidgets(headermap, showtext)
        
    def makeWidgets(self, headermap, showtext):
        """
        add headers, actions, attachments, text editor
        """
        actionsframe = self.makeHeaders(headermap)
        if self.origMessage and self.okayToOpenParts:
            self.makePartButtons()
        self.editor  = textEditor.TextEditorComponentMinimal(self)
        myactions    = self.actionButtons()
        for (label, callback) in myactions:
            b = Button(actionsframe, text=label, command=callback)
            b.config(bg='beige', relief=RIDGE, bd=2)
            b.pack(side=TOP, expand=YES, fill=BOTH)
        
        # body text, pack last=clip first
        self.editor.pack(side=BOTTOM)               # may be multiple editors
        self.editor.setAllText(showtext)            # each has own content
        lines = len(showtext.splitlines())
        lines = min(lines + 3, mailconfig.viewheight or 20)
        self.editor.setHeight(lines)                # else height=24, width=80
        self.editor.setWidth(80)                    # or from PyEdit textConfig
        if mailconfig.viewbg:
            self.editor.setBg(mailconfig.viewbg)    # colors, font in mailconfig
        if mailconfig.viewfg:
            self.editor.setFg(mailconfig.viewfg)
        if mailconfig.viewfont:                     # also via editor Tools menu
            self.editor.setFont(mailconfig.viewfont)


################################################################################
##    Changed Nov '06 to use grid() instead of pack() for more
##    platform-neutral headers layout; original code in book:
##
##    def makeHeaders(self, headermap):
##        """
##        add header entry fields, return action buttons frame
##        """
##        top    = Frame(self); top.pack   (side=TOP,   fill=X)
##        left   = Frame(top);  left.pack  (side=LEFT,  expand=NO,  fill=BOTH)
##        middle = Frame(top);  middle.pack(side=LEFT,  expand=NO,  fill=NONE)
##        right  = Frame(top);  right.pack (side=RIGHT, expand=YES, fill=BOTH)
##
##        # headers set may be extended in mailconfig (Bcc)
##        self.userHdrs = ()
##        showhdrs = ('From', 'To', 'Cc', 'Subject')
##        if hasattr(mailconfig, 'viewheaders') and mailconfig.viewheaders:
##            self.userHdrs = mailconfig.viewheaders
##            showhdrs += self.userHdrs
##            
##        self.hdrFields = []
##        for header in showhdrs:
##            lab = Label(middle, text=header+':', justify=LEFT)
##            ent = Entry(right)
##            lab.pack(side=TOP, expand=YES, fill=X)
##            ent.pack(side=TOP, expand=YES, fill=X)
##            ent.insert('0', headermap.get(header, '?'))
##            self.hdrFields.append(ent)             # order matters in onSend
##        return left
################################################################################


    def makeHeaders(self, headermap):
        """
        add header entry fields, return action buttons frame
        """
        top    = Frame(self); top.pack   (side=TOP,   fill=X)
        left   = Frame(top);  left.pack  (side=LEFT,  expand=NO,  fill=BOTH)
        middle = Frame(top);  middle.pack(side=LEFT,  expand=YES, fill=BOTH)

        # headers set may be extended in mailconfig (Bcc)
        self.userHdrs = ()
        showhdrs = ('From', 'To', 'Cc', 'Subject')
        if hasattr(mailconfig, 'viewheaders') and mailconfig.viewheaders:
            self.userHdrs = mailconfig.viewheaders
            showhdrs += self.userHdrs
            
        self.hdrFields = []
        for (i, header) in enumerate(showhdrs):
            lab = Label(middle, text=header+':', justify=LEFT)
            ent = Entry(middle)
            lab.grid(row=i, column=0, sticky=EW)
            ent.grid(row=i, column=1, sticky=EW)
            middle.rowconfigure(i, weight=1)
            ent.insert('0', headermap.get(header, '?'))
            self.hdrFields.append(ent)             # order matters in onSend
        middle.columnconfigure(1, weight=1)
        return left


    def actionButtons(self):                       # must be method for self
        return [('Cancel', self.destroy),          # close view window silently
                ('Parts',  self.onParts),          # multiparts list or the body
                ('Split',  self.onSplit)]

    def makePartButtons(self):
        """
        add up to N buttons that open attachments/parts
        when clicked; alternative to Parts/Split (2.1);
        okay that temp dir is shared by all open messages:
        part file not saved till later selected and opened;
        partname=partname is required in lambda in Py2.4;
        caveat: we could try to skip the main text part;
        """
        def makeButton(parent, text, callback):
            link = Button(parent, text=text, command=callback, relief=SUNKEN)
            if mailconfig.partfg: link.config(fg=mailconfig.partfg)
            if mailconfig.partbg: link.config(bg=mailconfig.partbg) 
            link.pack(side=LEFT, fill=X, expand=YES)

        parts = Frame(self)
        parts.pack(side=TOP, expand=NO, fill=X)
        for (count, partname) in enumerate(self.partsList(self.origMessage)):
            if count == self.maxPartButtons:
                makeButton(parts, '...', self.onSplit)
                break
            openpart = (lambda partname=partname: self.onOnePart(partname))
            makeButton(parts, partname, openpart)

    def onOnePart(self, partname):
        """
        locate selected part for button and save and open
        okay if multiple mails open: resaves each time selected
        we could probably just use webbrowser directly here
        caveat: tempPartDir is relative to cwd - poss anywhere
        caveat: tempPartDir is never cleaned up: might be large,
        could use tempfile module like html main text part code;
        """
        try:
            savedir  = self.tempPartDir
            message  = self.origMessage
            (contype, savepath) = self.saveOnePart(savedir, partname, message)
        except:
            showerror(appname, 'Error while writing part file')
            printStack(sys.exc_info())
        else:
            self.openParts([(contype, os.path.abspath(savepath))])

    def onParts(self):
        """
        show message part/attachments in popup window;
        uses same file naming scheme as save on Split;
        if non-multipart, single part = full body text
        """
        partnames = self.partsList(self.origMessage)
        msg = '\n'.join(['Message parts:\n'] + partnames)
        showinfo(appname, msg)
       
    def onSplit(self):
        """
        popup save dir dialog and save all parts/attachments there;
        if desired, popup html and multimedia parts in webbrowser,
        text in TextEditor, and well-known doc types on windows;
        could show parts in View windows where embedded texteditor
        would provide a save button, but most are not readable text;
        """
        savedir = self.partsDialog.show()          # class attr: at prior dir
        if savedir:                                # tk dir chooser, not file
            try:
                partfiles = self.saveParts(savedir, self.origMessage)
            except:
                showerror(appname, 'Error while writing part files')
                printStack(sys.exc_info())
            else:
                if self.okayToOpenParts: self.openParts(partfiles)

    def askOpen(self, appname, prompt):
        if not self.verifyPartOpens:
            return True
        else:
            return askyesno(appname, prompt)   # popup dialog
        
    def openParts(self, partfiles):
        """
        auto-open well known and safe file types, but
        only if verified by the user in a popup; other
        types must be opened manually from save dir;
        caveat: punts for type application/octet-stream
        even if safe filename extension such as .html;
        caveat: image/audio/video could use playfile.py;
        """
        for (contype, fullfilename) in partfiles:
            maintype  = contype.split('/')[0]                      # left side
            extension = os.path.splitext(fullfilename)[1]          # or [-4:]
            basename  = os.path.basename(fullfilename)             # strip dir
            
            # html and xml text, web pages, some media
            if contype  in ['text/html', 'text/xml']:
                if self.askOpen(appname, 'Open "%s" in browser?' % basename):
                    try:
                        webbrowser.open_new('file://' + fullfilename)
                    except:
                        showerror(appname, 'Browser failed: using editor')
                        textEditor.TextEditorMainPopup(self, fullfilename)

            # text/plain, text/x-python, etc.
            elif maintype == 'text':
                if self.askOpen(appname, 'Open text part "%s"?' % basename):
                    textEditor.TextEditorMainPopup(self, fullfilename)

            # multimedia types: windows opens mediaplayer, imageviewer, etc.
            elif maintype in ['image', 'audio', 'video']:
                if self.askOpen(appname, 'Open media part "%s"?' % basename):
                    try:
                        webbrowser.open_new('file://' + fullfilename)
                    except:
                        showerror(appname, 'Error opening browser')

            # common windows documents: word, adobe, excel, archives, etc.
            elif (sys.platform[:3] == 'win' and
                  maintype == 'application' and
                  extension in ['.doc', '.pdf', '.xls', '.zip','.tar', '.wmv']):
                    if self.askOpen(appname, 'Open part "%s"?' % basename):
                        os.startfile(fullfilename)

            else:  # punt!
                msg = 'Cannot open part: "%s"\nOpen manually in: "%s"'
                msg = msg % (basename, os.path.dirname(fullfilename))
                showinfo(appname, msg)


###############################################################################
# message edit windows - write, reply, forward
###############################################################################


if mailconfig.smtpuser:                              # user set in mailconfig?
    MailSenderClass = mailtools.MailSenderAuth       # login/password required
else:
    MailSenderClass = mailtools.MailSender

    
class WriteWindow(ViewWindow, MailSenderClass):
    """
    customize view display for composing new mail
    inherits sendMessage form mailtools.MailSender
    """
    modelabel = 'Write'

    def __init__(self, headermap, starttext):
        ViewWindow.__init__(self, headermap, starttext)
        MailSenderClass.__init__(self)
        self.attaches   = []                     # each win has own open dialog
        self.openDialog = None                   # dialog remembers last dir

    def actionButtons(self):
        return [('Cancel', self.quit),           # need method to use self
                ('Parts',  self.onParts),        # PopupWindow verifies cancel
                ('Attach', self.onAttach),
                ('Send  ', self.onSend)]

    def onParts(self):
        # caveat: deletes not currently supported
        if not self.attaches:
            showinfo(appname, 'Nothing attached')
        else:
            msg = '\n'.join(['Already attached:\n'] + self.attaches)
            showinfo(appname, msg)
       
    def onAttach(self):
        """
        attach a file to the mail: name added
        here will be added as a part on Send;
        """
        if not self.openDialog:
            self.openDialog = Open(title=appname + ': Select Attachmment File')
        filename = self.openDialog.show()        # remember prior dir
        if filename:
            self.attaches.append(filename)       # to be opened in send method

    def onSend(self):
        """
        threaded: mail edit window send button press
        may overlap with any other thread, disables none but quit
        Exit,Fail run by threadChecker via queue in after callback
        caveat: no progress here, because send mail call is atomic
        assumes multiple recipient addrs are separated with ';'
        
        caveat: should parse To,Cc,Bcc instead of splitting on ';',
        or use a multi-line input widgets instead of simple entry;
        as is, reply logic and gui user must avoid embedded ';'
        characters in addresses - very unlikely but not impossible;
        mailtools module saves sent message text in a local file
        """
        fieldvalues = [entry.get() for entry in self.hdrFields]     
        From, To, Cc, Subj = fieldvalues[:4]
        extraHdrs  = [('Cc', Cc), ('X-Mailer', appname + ' (Python)')]
        extraHdrs += zip(self.userHdrs, fieldvalues[4:]) 
        bodytext = self.editor.getAllText()

        # split multiple recipient lists, fix empty fields
        Tos = To.split(';')                                     # split to list
        Tos = [addr.strip() for addr in Tos]                    # spaces around
        for (ix, (name, value)) in enumerate(extraHdrs):
            if value:                                           # ignored if ''
                if value == '?':                                # ? not replaced
                    extraHdrs[ix] = (name, '')
                elif name.lower() in ['cc', 'bcc']:
                    values = value.split(';')
                    extraHdrs[ix] = (name, [addr.strip() for addr in values])
       
        # withdraw to disallow send during send
        # caveat: withdraw not foolproof- user may deiconify
        self.withdraw()
        self.getPassword()      # if needed; don't run popup in send thread!
        popup = popuputil.BusyBoxNowait(appname, 'Sending message')
        sendingBusy.incr()
        threadtools.startThread(
            action  = self.sendMessage,
            args    = (From, Tos, Subj, extraHdrs, bodytext, self.attaches,
                                                     saveMailSeparator),
            context = (popup,),
            onExit  = self.onSendExit,
            onFail  = self.onSendFail)

    def onSendExit(self, popup):
        # erase wait window, erase view window, decr send count
        # sendMessage call auto saves sent message in local file
        # cant use window.addSavedMails: mail text unavailable
        popup.quit()
        self.destroy()
        sendingBusy.decr()

        # poss \ when opened, / in mailconfig
        sentname = os.path.abspath(mailconfig.sentmailfile)  # also expands '.'
        if sentname in openSaveFiles.keys():                 # sent file open?
            window = openSaveFiles[sentname]                 # update list,raise
            window.loadMailFileThread()

    def onSendFail(self, exc_info, popup):
        # popup error, keep msg window to save or retry, redraw actions frame
        popup.quit()
        self.deiconify()
        self.lift()
        showerror(appname, 'Send failed: \n%s\n%s' % exc_info[:2])
        printStack(exc_info)
        self.smtpPassword = None        # try again
        sendingBusy.decr()

    def askSmtpPassword(self):
        """
        get password if needed from gui here, in main thread
        caveat: may try this again in thread is no input first
        time, so goes into a loop until input is provided; see
        pop paswd input logic for a non-looping alternative
        """
        password = ''
        while not password:
            prompt = ('Password for %s on %s?' %
                     (self.smtpUser, self.smtpServerName))
            password = popuputil.askPasswordWindow(appname, prompt)
        return password


class ReplyWindow(WriteWindow):
    """
    customize write display for replying
    text and headers set up by list window
    """
    modelabel = 'Reply'


class ForwardWindow(WriteWindow):
    """
    customize reply display for forwarding
    text and headers set up by list window
    """
    modelabel = 'Forward'
