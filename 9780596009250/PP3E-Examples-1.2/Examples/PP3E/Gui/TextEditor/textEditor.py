################################################################################
# PyEdit 2.0: a Python/Tkinter text file editor and component.
#
# Uses the Tk text widget, plus GuiMaker menus and toolbar buttons to 
# implement a full-featured text editor that can be run as a stand-alone 
# program, and attached as a component to other GUIs.  Also used by 
# PyMailGUI and PyView to edit mail text and image file notes, and 
# by PyMailGUI and PyDemos2 in pop-up mode to display source files.
#
# New in 2.0:
# -added simple font components input dialog
# -use Tk 8.4 undo stack api to add undo, redo, modified test
# -now verifies on quit, open, new, run, only if text modified and unsaved
# -searches are case-insensitive now
# -configuration module for initial font/color/size/searchcase
# TBD: could also allow search case choice in GUI, and could use regexps.
# NOTE: a "PP2E" typo in the first printing of the book was fixed here.
################################################################################
     
Version = '2.0'
import sys, os                             # platform, args, run tools
from Tkinter        import *               # base widgets, constants
from tkFileDialog   import Open, SaveAs    # standard dialogs
from tkMessageBox   import showinfo, showerror, askyesno
from tkSimpleDialog import askstring, askinteger
from tkColorChooser import askcolor
from PP3E.Gui.Tools.guimaker import *      # Frame + menu/toolbar builders

try:
    import textConfig                      # startup font and colors
    configs = textConfig.__dict__          # work if not on the path or bad
except:
    configs = {}

helptext = """PyEdit version %s
January, 2006
(1.0: October, 2000)

Programming Python, 3rd Edition
O'Reilly Media, Inc.

A text editor program and embeddable object
component, written in Python/Tkinter.  Use
menu tear-offs and toolbar for quick access
to actions, and Alt-key shortcuts for menus.

New in version %s:
- font pick dialog
- unlimited undo/redo
- quit/open/new/run prompt save only if changed 
- searches are case-insensitive
- startup configuration module textConfig.py
"""

START     = '1.0'                          # index of first char: row=1,col=0
SEL_FIRST = SEL + '.first'                 # map sel tag to index
SEL_LAST  = SEL + '.last'                  # same as 'sel.last'
     
FontScale = 0                              # use bigger font on linux
if sys.platform[:3] != 'win':              # and other non-windows boxes
    FontScale = 3

################################################################################
# Main class: implements editor gui, actions
################################################################################

class TextEditor:                          # mix with menu/toolbar Frame class
    startfiledir = '.'
    ftypes = [('All files',     '*'),                 # for file open dialog
              ('Text files',   '.txt'),               # customize in subclass
              ('Python files', '.py')]                # or set in each instance
     
    colors = [{'fg':'black',      'bg':'white'},      # color pick list
              {'fg':'yellow',     'bg':'black'},      # first item is default
              {'fg':'white',      'bg':'blue'},       # tailor me as desired
              {'fg':'black',      'bg':'beige'},      # or do PickBg/Fg chooser
              {'fg':'yellow',     'bg':'purple'},
              {'fg':'black',      'bg':'brown'},
              {'fg':'lightgreen', 'bg':'darkgreen'},
              {'fg':'darkblue',   'bg':'orange'},
              {'fg':'orange',     'bg':'darkblue'}]
     
    fonts  = [('courier',    9+FontScale, 'normal'),  # platform-neutral fonts
              ('courier',   12+FontScale, 'normal'),  # (family, size, style)
              ('courier',   10+FontScale, 'bold'),    # or popup a listbox
              ('courier',   10+FontScale, 'italic'),  # make bigger on linux
              ('times',     10+FontScale, 'normal'),  # use 'bold italic' for 2
              ('helvetica', 10+FontScale, 'normal'),  # also 'underline', etc.
              ('ariel',     10+FontScale, 'normal'),
              ('system',    10+FontScale, 'normal'),
              ('courier',   20+FontScale, 'normal')]
     
    def __init__(self, loadFirst=''):
        if not isinstance(self, GuiMaker):
            raise TypeError, 'TextEditor needs a GuiMaker mixin'
        self.setFileName(None)
        self.lastfind   = None
        self.openDialog = None
        self.saveDialog = None
        self.text.focus()                           # else must click in text
        if loadFirst: 
            self.onOpen(loadFirst)
 
    def start(self):                                # run by GuiMaker.__init__
        self.menuBar = [                            # configure menu/toolbar
            ('File', 0,                             # a GuiMaker menu def tree
                 [('Open...',    0, self.onOpen),   # build in method for self
                  ('Save',       0, self.onSave),   # label, shortcut, callback
                  ('Save As...', 5, self.onSaveAs),
                  ('New',        0, self.onNew),
                  'separator',
                  ('Quit...',    0, self.onQuit)]
            ),
            ('Edit', 0,
                 [('Undo',       0, self.onUndo),
                  ('Redo',       0, self.onRedo),
                  'separator',
                  ('Cut',        0, self.onCut),
                  ('Copy',       1, self.onCopy),
                  ('Paste',      0, self.onPaste),
                  'separator',
                  ('Delete',     0, self.onDelete),
                  ('Select All', 0, self.onSelectAll)]
            ),
            ('Search', 0,
                 [('Goto...',    0, self.onGoto),
                  ('Find...',    0, self.onFind),
                  ('Refind',     0, self.onRefind),
                  ('Change...',  0, self.onChange)]
            ),
            ('Tools', 0,
                 [('Pick Font...', 6, self.onPickFont),
                  ('Font List',    0, self.onFontList),
                 'separator',
                  ('Pick Bg...',   3, self.onPickBg),
                  ('Pick Fg...',   0, self.onPickFg),
                  ('Color List',   0, self.onColorList),
                 'separator',
                  ('Info...',      0, self.onInfo),
                  ('Clone',        1, self.onClone),
                  ('Run Code',     0, self.onRunCode)]
            )]
        self.toolBar = [
            ('Save',  self.onSave,   {'side': LEFT}),
            ('Cut',   self.onCut,    {'side': LEFT}),
            ('Copy',  self.onCopy,   {'side': LEFT}),
            ('Paste', self.onPaste,  {'side': LEFT}),
            ('Find',  self.onRefind, {'side': LEFT}),
            ('Help',  self.help,     {'side': RIGHT}),
            ('Quit',  self.onQuit,   {'side': RIGHT})]
     
    def makeWidgets(self):                          # run by GuiMaker.__init__
        name = Label(self, bg='black', fg='white')  # add below menu, above tool
        name.pack(side=TOP, fill=X)                 # menu/toolbars are packed
     
        vbar  = Scrollbar(self)  
        hbar  = Scrollbar(self, orient='horizontal')
        text  = Text(self, padx=5, wrap='none')
        text.config(undo=1, autoseparators=1)          # 2.0, default is 0, 1
     
        vbar.pack(side=RIGHT,  fill=Y)
        hbar.pack(side=BOTTOM, fill=X)                 # pack text last
        text.pack(side=TOP,    fill=BOTH, expand=YES)  # else sbars clipped
     
        text.config(yscrollcommand=vbar.set)    # call vbar.set on text move
        text.config(xscrollcommand=hbar.set)
        vbar.config(command=text.yview)         # call text.yview on scroll move
        hbar.config(command=text.xview)         # or hbar['command']=text.xview

        # 2.0: apply user configs or defaults
        startfont = configs.get('font', self.fonts[0])
        startbg   = configs.get('bg',   self.colors[0]['bg'])
        startfg   = configs.get('fg',   self.colors[0]['fg'])
        text.config(font=startfont, bg=startbg, fg=startfg)
        if 'height' in configs: text.config(height=configs['height'])
        if 'width'  in configs: text.config(width =configs['width'])
        self.text = text
        self.filelabel = name
     
    ############################################################################
    # File menu commands
    ############################################################################
     
    def my_askopenfilename(self):      # objects remember last result dir/file
        if not self.openDialog:
           self.openDialog = Open(initialdir=self.startfiledir, 
                                  filetypes=self.ftypes)
        return self.openDialog.show()
     
    def my_asksaveasfilename(self):    # objects remember last result dir/file
        if not self.saveDialog:
           self.saveDialog = SaveAs(initialdir=self.startfiledir, 
                                    filetypes=self.ftypes)
        return self.saveDialog.show()
        
    def onOpen(self, loadFirst=''):
        doit = (not self.text_edit_modified() or      # 2.0
                askyesno('PyEdit', 'Text has changed: discard changes?'))
        if doit:
            file = loadFirst or self.my_askopenfilename()
            if file:
                try:
                    text = open(file, 'r').read()
                except:
                    showerror('PyEdit', 'Could not open file ' + file)
                else:
                    self.setAllText(text)
                    self.setFileName(file)
                    self.text.edit_reset()        # 2.0: clear undo/redo stks
                    self.text.edit_modified(0)    # 2.0: clear modified flag

    def onSave(self):
        self.onSaveAs(self.currfile)  # may be None
     
    def onSaveAs(self, forcefile=None):
        file = forcefile or self.my_asksaveasfilename()
        if file:
            text = self.getAllText()
            try:
                open(file, 'w').write(text)
            except:
                showerror('PyEdit', 'Could not write file ' + file)
            else:
                self.setFileName(file)             # may be newly created
                self.text.edit_modified(0)         # 2.0: clear modified flag
                                                   # don't clear undo/redo stks     
    def onNew(self):
        doit = (not self.text_edit_modified() or   # 2.0
                askyesno('PyEdit', 'Text has changed: discard changes?'))
        if doit:
            self.setFileName(None)
            self.clearAllText()
            self.text.edit_reset()                 # 2.0: clear undo/redo stks
            self.text.edit_modified(0)             # 2.0: clear modified flag
        
    def onQuit(self): 
        doit = (not self.text_edit_modified()      # 2.0
                or askyesno('PyEdit',
                            'Text has changed: quit and discard changes?'))
        if doit:
            self.quit()                            # Frame.quit via GuiMaker

    def text_edit_modified(self):
        """
        2.0: self.text.edit_modified() broken in Python 2.4:
        do manually for now (seems to be bool result type bug)
        """
        return self.tk.call((self.text._w, 'edit') + ('modified', None))
     
    ############################################################################
    # Edit menu commands
    ############################################################################

    def onUndo(self):                           # 2.0
        try:                                    # tk8.4 keeps undo/redo stacks
            self.text.edit_undo()               # exception if stacks empty
        except TclError:                        # menu tear-offs for quick undo
            showinfo('PyEdit', 'Nothing to undo')
            
    def onRedo(self):                           # 2.0: redo an undone
        try:
            self.text.edit_redo()
        except TclError:
            showinfo('PyEdit', 'Nothing to redo')
        
    def onCopy(self):                           # get text selected by mouse,etc
        if not self.text.tag_ranges(SEL):       # save in cross-app clipboard
            showerror('PyEdit', 'No text selected')
        else:
            text = self.text.get(SEL_FIRST, SEL_LAST)  
            self.clipboard_clear()              
            self.clipboard_append(text)
     
    def onDelete(self):                         # delete selected text, no save
        if not self.text.tag_ranges(SEL):
            showerror('PyEdit', 'No text selected')
        else:
            self.text.delete(SEL_FIRST, SEL_LAST)
     
    def onCut(self):
        if not self.text.tag_ranges(SEL):
            showerror('PyEdit', 'No text selected')
        else: 
            self.onCopy()                       # save and delete selected text
            self.onDelete()
     
    def onPaste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')
        except TclError:
            showerror('PyEdit', 'Nothing to paste')
            return
        self.text.insert(INSERT, text)          # add at current insert cursor
        self.text.tag_remove(SEL, '1.0', END) 
        self.text.tag_add(SEL, INSERT+'-%dc' % len(text), INSERT)
        self.text.see(INSERT)                   # select it, so it can be cut
     
    def onSelectAll(self):
        self.text.tag_add(SEL, '1.0', END+'-1c')   # select entire text 
        self.text.mark_set(INSERT, '1.0')          # move insert point to top
        self.text.see(INSERT)                      # scroll to top

    ############################################################################
    # Search menu commands
    ############################################################################
 
    def onGoto(self, forceline=None):
        line = forceline or askinteger('PyEdit', 'Enter line number')
        self.text.update() 
        self.text.focus()
        if line is not None:
            maxindex = self.text.index(END+'-1c')
            maxline  = int(maxindex.split('.')[0])
            if line > 0 and line <= maxline:
                self.text.mark_set(INSERT, '%d.0' % line)      # goto line
                self.text.tag_remove(SEL, '1.0', END)          # delete selects
                self.text.tag_add(SEL, INSERT, 'insert + 1l')  # select line
                self.text.see(INSERT)                          # scroll to line
            else:
                showerror('PyEdit', 'Bad line number')
     
    def onFind(self, lastkey=None):
        key = lastkey or askstring('PyEdit', 'Enter search string')
        self.text.update()
        self.text.focus()
        self.lastfind = key
        if key:                                                    # 2.0: nocase
            nocase = configs.get('caseinsens', 1)                  # 2.0: config
            where = self.text.search(key, INSERT, END, nocase=nocase)
            if not where:                                          # don't wrap
                showerror('PyEdit', 'String not found')
            else:
                pastkey = where + '+%dc' % len(key)           # index past key
                self.text.tag_remove(SEL, '1.0', END)         # remove any sel
                self.text.tag_add(SEL, where, pastkey)        # select key 
                self.text.mark_set(INSERT, pastkey)           # for next find
                self.text.see(where)                          # scroll display
     
    def onRefind(self):
        self.onFind(self.lastfind)
     
    def onChange(self):
        new = Toplevel(self)
        Label(new, text='Find text:').grid(row=0, column=0)
        Label(new, text='Change to:').grid(row=1, column=0)
        self.change1 = Entry(new)
        self.change2 = Entry(new)
        self.change1.grid(row=0, column=1, sticky=EW)
        self.change2.grid(row=1, column=1, sticky=EW)
        Button(new, text='Find',  
               command=self.onDoFind).grid(row=0, column=2, sticky=EW)
        Button(new, text='Apply', 
               command=self.onDoChange).grid(row=1, column=2, sticky=EW)
        new.columnconfigure(1, weight=1)    # expandable entrys
     
    def onDoFind(self):
        self.onFind(self.change1.get())                    # Find in change box
     
    def onDoChange(self):
        if self.text.tag_ranges(SEL):                      # must find first
            self.text.delete(SEL_FIRST, SEL_LAST)          # Apply in change
            self.text.insert(INSERT, self.change2.get())   # deletes if empty
            self.text.see(INSERT)
            self.onFind(self.change1.get())                # goto next appear
            self.text.update()                             # force refresh
     
    ############################################################################
    # Tools menu commands 
    ############################################################################
     
    def onFontList(self):
        self.fonts.append(self.fonts[0])           # pick next font in list
        del self.fonts[0]                          # resizes the text area
        self.text.config(font=self.fonts[0]) 
     
    def onColorList(self):
        self.colors.append(self.colors[0])         # pick next color in list
        del self.colors[0]                         # move current to end
        self.text.config(fg=self.colors[0]['fg'], bg=self.colors[0]['bg']) 
     
    def onPickFg(self): 
        self.pickColor('fg')                       # added on 10/02/00
    def onPickBg(self):                            # select arbitrary color
        self.pickColor('bg')                       # in standard color dialog

    def pickColor(self, part):                     # this is too easy
        (triple, hexstr) = askcolor()
        if hexstr:
            self.text.config(**{part: hexstr})
     
    def onInfo(self):
        text  = self.getAllText()                  # added on 5/3/00 in 15 mins
        bytes = len(text)                          # words uses a simple guess: 
        lines = len(text.split('\n'))              # any separated by whitespace
        words = len(text.split()) 
        index = self.text.index(INSERT)
        where = tuple(index.split('.'))
        showinfo('PyEdit Information',
                 'Current location:\n\n' +
                 'line:\t%s\ncolumn:\t%s\n\n' % where +
                 'File text statistics:\n\n' +
                 'bytes:\t%d\nlines:\t%d\nwords:\t%d\n' % (bytes, lines, words))
     
    def onClone(self):
        new = Toplevel()                # a new edit window in same process
        myclass = self.__class__        # instance's (lowest) class object
        myclass(new)                    # attach/run instance of my class
     
    def onRunCode(self, parallelmode=True):
        """
        run Python code being edited--not an ide, but handy;
        tries to run in file's dir, not cwd (may be PP3E root);
        inputs and adds command-line arguments for script files;
        code's stdin/out/err = editor's start window, if any:
        run with a console window to see code's print outputs;
        but parallelmode uses start to open a dos box for i/o;
        module search path will include '.' dir where started;
        in non-file mode, code's Tk root window is PyEdit win;
        """
        def askcmdargs():
            return askstring('PyEdit', 'Commandline arguments?') or ''
        
        from PP3E.launchmodes import System, Start, Fork
        filemode = False
        thefile  = str(self.getFileName())
        if os.path.exists(thefile):
            filemode = askyesno('PyEdit', 'Run from file?')
        if not filemode:                                    # run text string
            cmdargs   = askcmdargs()
            namespace = {'__name__': '__main__'}            # run as top-level
            sys.argv  = [thefile] + cmdargs.split()         # could use threads
            exec self.getAllText() + '\n' in namespace      # exceptions ignored
        elif self.text_edit_modified():                     # 2.0: changed test
            showerror('PyEdit', 'Text changed: save before run')
        else:
            cmdargs  = askcmdargs()
            mycwd    = os.getcwd()                          # cwd may be root
            os.chdir(os.path.dirname(thefile) or mycwd)     # cd for filenames
            thecmd   = thefile + ' ' + cmdargs
            if not parallelmode:                            # run as file
                System(thecmd, thecmd)()                    # block editor
            else:
                if sys.platform[:3] == 'win':               # spawn in parallel
                    Start(thecmd, thecmd)()                 # or use os.spawnv
                else:
                    Fork(thecmd, thecmd)()                  # spawn in parallel
            os.chdir(mycwd)

    def onPickFont(self):
        # 2.0 font spec dialog
        new = Toplevel(self)
        Label(new, text='Family:').grid(row=0, column=0)      # nonmodal dialog
        Label(new, text='Size:  ').grid(row=1, column=0)      # see pick list 
        Label(new, text='Style: ').grid(row=2, column=0)      # for valid inputs
        self.font1 = Entry(new)
        self.font2 = Entry(new)
        self.font3 = Entry(new)
        self.font1.insert(0, 'courier')                       # suggested vals
        self.font2.insert(0, '12')
        self.font3.insert(0, 'bold italic')
        self.font1.grid(row=0, column=1, sticky=EW)
        self.font2.grid(row=1, column=1, sticky=EW)
        self.font3.grid(row=2, column=1, sticky=EW)
        Button(new, text='Apply', 
               command=self.onDoFont).grid(row=3, columnspan=2)
        new.columnconfigure(1, weight=1)    # expandable entrys

    def onDoFont(self):
        try:
            font = (self.font1.get(), int(self.font2.get()), self.font3.get())
            self.text.config(font=font) 
        except:
            showerror('PyEdit', 'Bad font specification')
     
    ############################################################################
    # Utilities, useful outside this class
    ############################################################################
     
    def isEmpty(self):
        return not self.getAllText() 
     
    def getAllText(self):
        return self.text.get('1.0', END+'-1c')  # extract text as a string     
    def setAllText(self, text):
        self.text.delete('1.0', END)            # store text string in widget
        self.text.insert(END, text)             # or '1.0'
        self.text.mark_set(INSERT, '1.0')       # move insert point to top 
        self.text.see(INSERT)                   # scroll to top, insert set
    def clearAllText(self):
        self.text.delete('1.0', END)            # clear text in widget 
     
    def getFileName(self):
        return self.currfile
    def setFileName(self, name):                # also: onGoto(linenum)
        self.currfile = name  # for save
        self.filelabel.config(text=str(name))

    def setBg(self, color):
        self.text.config(bg=color)              # to set manually from code
    def setFg(self, color):
        self.text.config(fg=color)              # 'black', hexstring
    def setFont(self, font):
        self.text.config(font=font)             # ('family', size, 'style')
        
    def setHeight(self, lines):                 # default = 24h x 80w
        self.text.config(height=lines)          # may also be from textCongif.py
    def setWidth(self, chars):
        self.text.config(width=chars)

    def clearModified(self):
        self.text.edit_modified(0)              # clear modified flag
    def isModified(self):
        return self.text_edit_modified()        # changed since last reset?
 
    def help(self):
        showinfo('About PyEdit', helptext % ((Version,)*2))
     
################################################################################
# ready-to-use editor classes 
# mix in a Frame subclass that builds menu/toolbars
################################################################################

#    
# when editor owns the window 
#
class TextEditorMain(TextEditor, GuiMakerWindowMenu):  # add menu/toolbar maker 
    def __init__(self, parent=None, loadFirst=''):     # when fills whole window
        GuiMaker.__init__(self, parent)                # use main window menus
        TextEditor.__init__(self, loadFirst)           # self has GuiMaker frame
        self.master.title('PyEdit ' + Version)         # title if stand-alone
        self.master.iconname('PyEdit')                 # catch wm delete button
        self.master.protocol('WM_DELETE_WINDOW', self.onQuit)
     
class TextEditorMainPopup(TextEditor, GuiMakerWindowMenu):
    def __init__(self, parent=None, loadFirst='', winTitle=''):     
        self.popup = Toplevel(parent)                  # create own window
        GuiMaker.__init__(self, self.popup)            # use main window menus
        TextEditor.__init__(self, loadFirst) 
        assert self.master == self.popup
        self.popup.title('PyEdit ' + Version + winTitle) 
        self.popup.iconname('PyEdit')               
    def quit(self):
        self.popup.destroy()                           # kill this window only

#         
# when embedded in another window
#
class TextEditorComponent(TextEditor, GuiMakerFrameMenu):     
    def __init__(self, parent=None, loadFirst=''):     # use Frame-based menus
        GuiMaker.__init__(self, parent)                # all menus, buttons on
        TextEditor.__init__(self, loadFirst)           # GuiMaker must init 1st
     
class TextEditorComponentMinimal(TextEditor, GuiMakerFrameMenu): 
    def __init__(self, parent=None, loadFirst='', deleteFile=1):   
        self.deleteFile = deleteFile
        GuiMaker.__init__(self, parent)             
        TextEditor.__init__(self, loadFirst) 
    def start(self):
        TextEditor.start(self)                         # GuiMaker start call
        for i in range(len(self.toolBar)):             # delete quit in toolbar
            if self.toolBar[i][0] == 'Quit':           # delete file menu items
                del self.toolBar[i]; break             # or just disable file
        if self.deleteFile:
            for i in range(len(self.menuBar)):
                if self.menuBar[i][0] == 'File':
                    del self.menuBar[i]; break
        else:
            for (name, key, items) in self.menuBar:
                if name == 'File':
                    items.append([1,2,3,4,6]) 

################################################################################
# stand-alone program run
################################################################################
                                                     
def testPopup():     
    # see PyView and PyMail for component tests
    root = Tk()
    TextEditorMainPopup(root)
    TextEditorMainPopup(root)
    Button(root, text='More', command=TextEditorMainPopup).pack(fill=X)
    Button(root, text='Quit', command=root.quit).pack(fill=X)
    root.mainloop()
     
def main():                                           # may be typed or clicked
    try:                                              # or associated on Windows
        fname = sys.argv[1]                           # arg = optional filename
    except IndexError:
        fname = None
    TextEditorMain(loadFirst=fname).pack(expand=YES, fill=BOTH)
    mainloop()
     
if __name__ == '__main__':                            # when run as a script
    #testPopup()
    main()                                            # run .pyw for no dos box    
