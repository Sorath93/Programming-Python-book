######################################################################
# PyMailGUI help text string, in this separate module only to avoid
# distracting from executable code.  As coded, we throw up this text
# in a simple scrollable text box; in the future, we might instead 
# use an HTML file opened with a browser (use webbrowser module, or
# run a "netscape help.html" or DOS "start help.html" with os.system);
# that would add an external dependency, unless text on browser fail; 
######################################################################

# used to have to be narrow for Linux info box popups; 
# now uses scrolledtext with buttons instead;

helptext = """PyMailGUI, version 2.1
January, 2006
Programming Python, 3rd Edition
O'Reilly Media, Inc.

PyMailGUI is a multi-window interface for processing email, both on-line and
off-line.  Its main interfaces include one list window for the mail server,
zero or more list windows for mail save files, and multiple view windows for
composing or viewing emails selected in a list window.  On start-up, the main
(server) list window appears first, but no mail server connection is attempted
until a Load or message send request.  All PyMailGUI windows may be resized,
which is especially useful in list windows to see additional columns. 


Major enhancements in this version:

* MIME multi-part mails with attachments may be both viewed and composed.
* Mail transfers are no longer blocking, and may overlap in time.
* Mail may be saved and processed off-line from a local file.
* Message parts may now be opened automatically within the GUI.
* Multiple messages may be selected for processing in list windows.
* Initial downloads fetch mail headers only; full mails are fetched on request.
* View window headers and list window columns are configurable.
* Deletions are performed immediately, not delayed until program exit.
* Most server transfers report their progress in the GUI.
* Long lines are intelligently wrapped in viewed and quoted text.
* Fonts and colors in list and view windows may be configured by the user.
* Authenticating SMTP mail-send servers that require login are supported.
* Sent messages are saved in a local file, which may be opened in the GUI.
* View windows intelligently pick a main text part to be displayed.
* Already-fetched mail headers and full mails are cached for speed.
* Date strings and addresses in composed mails are formatted properly.
* (2.1) View windows now have quick-access buttons for attachments/parts.
* (2.1) Inbox out-of-synch errors detected on deletes, and index and mail loads.
* (2.1) Save-file loads and deletes threaded, to avoid pauses for large files.


Note: To use PyMailGUI to read and write email of your own, you must change
the POP and SMTP server names and login details in the file mailconfig.py,
located in PyMailGUI's source-code directory.  See section 10 for details.

Contents:
1)  LIST WINDOW ACTIONS
2)  VIEW WINDOW ACTIONS
3)  OFFLINE PROCESSING
4)  VIEWING TEXT AND ATTACHMENTS
5)  SENDING TEXT AND ATTACHMENTS
6)  MAIL TRANSFER OVERLAP
7)  MAIL DELETION
8)  INBOX MESSAGE NUMBER SYNCHRONIZATION
9)  LOADING EMAIL
10) THE mailconfig CONFIGURATION MODULE
11) DEPENDENCIES
12) MISCELLANEOUS HINTS




1) LIST WINDOW ACTIONS

Click list window buttons to process email: 

- Load:\t fetch all (or new) mail headers from POP server inbox
- View:\t display selected emails nicely formatted
- Delete:\t delete selected emails from server or save file
- Write:\t compose a new email message, send by SMTP
- Reply:\t compose replies to selected emails, send by SMTP
- Fwd:\t compose forwards of selected emails, send by SMTP
- Save:\t write all selected emails to a chosen save file
- Open:\t load emails from an offline save file into new list window
- Quit:\t exit program (server list), close window (file list) 

Double-click on an email in a list window's listbox to view the mail's raw text,
including any mail headers not shown by the View button.  List windows opened
for mail save files support all of the above except Load.  After the initial
Load, Load only fetches newly-arrived message headers.  To forceably reload all
mails from the server, restart PyMailGUI.  There is reload button, because full
reloads are only required on rare deletion and inbox synchronization errors
(described ahead), and reloads are initiated automatically in these cases.

Click on emails in the main window's listbox to select them.  Click the "All"
checkbox to select all or no emails at once.  More than one email may be
selected at the same time: View, Delete, Reply, Fwd, and Save buttons are
applied to all currently selected emails, in both server and save-file list
windows.  Use Ctrl+click to select multiple mails, Shift+click to select all
from prior selecion, or click+move to drag the selection out.

In 2.1, most of the actions in the server List window automatically run a
quick-check to detect inbox out-of-synch errors with the server.  If a synch
error pop-up appears, a full index reload will be automatically run; there
is no need to stop and restart PyMailGUI (see ahead in this help).



2) VIEW WINDOW ACTIONS

Action buttons in message view windows (View):

- Cancel:\t closes the message view window
- Parts:\t lists all message parts, including attachments
- Split:\t extracts, saves, and possibly opens message parts

Actions in message compose windows (Write, Reply, Fwd):

- Cancel:\t closes the message window, discarding its content
- Parts:\t lists files already attached to mail being edited
- Attach:\t adds a file as an attachment to a mail being edited
- Send:\t sends the message to all its recipients

Parts and Split buttons appear in all View windows; for simple messages, the
sole part is the message body.  Message reply, forward, and delete requests are
made in the list windows, not message view windows.  Deletions do not erase
open view windows.

New in 2.1: View windows also have up to a fixed maximum number of quick
access buttons for attached message parts.  They are alternatives to Split.
After the maximum number, a '...' button is added, which simply runs Split.
The maximum number of part buttons to display per view window can be set in
the mailconfig.py user settings module (described ahead).



3) OFFLINE PROCESSING

To process email offline: Load from the server, Save to a local file, and
later select Open to open a save file's list window in either the server List
window or another save file's List window.  Open cretes a new List window for
the file, or raises its window if the file is already open.

A save file's list window allows all main window actions listed above, except
for Load.  For example, saved messages can be viewed, deleted, replied to, or
forwarded, from the file's list window.  Operations are mapped to the local
mail save file, instead of the server's inbox.   Saved messages may also be
saved: to move mails from one save file to another, Save and then Delete from
the source file's window.

You do not need to connect to a server to process save files off-line: click
the Open button in the main list window.  In a save-file list window, a Quit
erases that window only; a Delete removes the message from the local save file,
not from a server. Save-file list windows are automatically updated when new
mails are saved to the corresponding file anywhere in the GUI.  The sent-mail
file may also be opened and processed as a normal save-mail file, with Open.

Save buttons in list windows save the full message text (including its headers,
and a message separator).  To save just the main text part of a message, either
use the Save button in the TextEditor at the bottom of a view or edit window,
or select the "Split" action button.  To save attachments, see the next section.

New in 2.1: local save-file Open and Delete requests are threaded to avoid
blocking the GUI during loads and deletes of large files.  Because of this, a
loaded file's index may not appear in its List window immediately.  Similarly,
when new mails are saved or messages are sent, there may be a delay before
the corresponding local file's List window is updated, if it is currently open.

As a status indication, the window's title changes to "Loading..." on loads
and "Deleting..." during deletes, and is reset the file's name after the thread
exits (the server window uses pop-ups for status indication, because the delay
is longer, and there is progress to display).  Eventually, either the index will
appear and its window raised, or an error message will pop up.  Save-file loads
and deletes are not allowed to overlap with each other for a given file, but
may overlap with server transfers and operations on other open files.

Note: save-file Save operations are still not threaded, and may pause the GUI
momentarily when saving very many large mails.  This is normaly not noticeable,
because unlike Open and Delete, saves simply append to the save-file, and do
not reload its content.  To avoid pauses completely, though, don't save very
many large mails in a single operation.

Also note: the current implementation loads the entire save-mail file into
memory when opened.  Because of this, save-mail files are limited in size,
depending upon your computer.  To avoid consuming too much memory, you
should try to keep your save files relatively small (at the least, smaller
than your computer's available memory).  As a rule of thumb, organize your
saved mails by categories into many small files, instead of a few large files.



4) VIEWING TEXT AND ATTACHMENTS

PyMailGUI's view windows use a text-oriented display.  When a mail is viewed,
its main text is displayed in the View window.  This text is taken from the
entire body of a simple message, or the first text part of a multi-part MIME
message.  To extract the main message text, PyMailGUI looks for plain text,
then HTML, and then text of any other kind.  If no such text content is found,
nothing is displayed in the view window, but parts may be opened manually with
the "Split" button (and quick-access part buttons in 2.1, described below).

If the body of a simple message is HTML type, or a HTML part is used as the
main message text, a web browser is popped up as an alternative display for
the main message text, if verified by the user (the mailconfig module can be
used to bypass the verification; see ahead).  This is equivalent to opening
the HTML part with the "Split" button, but is initiated automatically for the
main message text's HTML.  If a simple message is something other than text
or HTML, its content must be openened manually with Split.

When viewing mails, messages with multi-part attachments are prefixed with
a "*" in list windows.  "Parts" and "Split" buttons appear in all View windows.
Message parts are defined as follows:

- For simple messages, the message body is considered to be the sole
  part of the message.

- For multi-part messages, the message parts list includes the main
  message text, as well as all attachments.

In both cases, message parts may be saved and opened with the "Split" button.
For simple messages, the message body may be saved with Split, as well as the
Save button in the view window's text editor.  To process multi-part messages:

- Use "Parts" to display the names of all message parts, including any
  attachments, in a popup dialog.

- Use "Split" to view message parts: all mail parts are first saved to a
  selected directory, and any well-known and generally safe part files are
  opened automatically, but only if verified by the user.

- See also the note below about 2.1 quick access buttons, for an alternative
  to the Parts/Split interface on View windows.
  
For "Split", select a local directory to save parts to.  After the save, text
parts open in the TextEditor GUI, HTML and multimedia types open in a web
browser, and common Windows document types (e.g., .doc and .xls files) open via
the Windows registry entry for the filename extension.  For safety, unknown
types and executable program parts are never run automatically; even Python
programs are displayed as source text only (save the code to run manually).

Web browsers on some platforms may open multimedia types (image, audio, video)
in specific content handler programs (e.g., MediaPlayer, image viewers).  No
other types of attachments are ever opened, and attachments are never opened
without user verification (or mailconfig.py authorization in 2.1, described
below).  Browse the parts save directory to open other parts manually.

To avoid scrolling for very long lines (sometimes sent by HTML-based mailers),
the main text part of a message is automatically wrapped for easy viewing.
Long lines are split up at the first delimiter found before a fixed column,
when viewed, replied, or forwarded.  The wrapping column may be configured or
disabled in the mailconfig module (see ahead).  Text lines are never
automatically wrapped when sent; users or recipients should manage line length
in composed mails.

New in 2.1: View windows also have up to a fixed maximum number of quick-access
buttons for attached message parts.  They are alternatives to Split: selecting
an attachment's button automatically extracts, saves, and opens that single
attachment directly, without Split directory and popup dialogs (a temporary
directory is used).  The maximum number of part buttons to display per view
window can be set in the mailconfig.py user settings module (described ahead).
For mails with more than the maximum number of attachments, a '...' button is
added which simply runs Split to save and open any additional attachments.

Also in 2.1, two settings in the mailconfig.py module (see section 10) can be
used to control how PyMailGUI opens parts in the GUI:

- okayToOpenParts: controls whether part opens are allowed at all
- verifyPartOpens: controls whether to ask before each part is opened.

Both are used for View window Split actions and part quick-access buttons.  If
okayToOpenParts is False, quick-access part buttons will not appear in the gui,
and Split saves parts in a directory but does not open them.  verifyPartOpens
is used by both Split and quick-access part buttons: if False, part buttons
open parts immediately, and Split opens all known-type parts automatically
after they are saved (unknown types and executables are never opened).

An additional setting in this module, verifyHTMLTextOpen, controls verification
of opening a web browser on a HTML main text part of a message; if False, the
web browser is opened without prompts.  This is a separate setting from
verifyPartOpens, because this is more automatic than part opens, and some
HTML main text parts may have dubious content (e.g., images, ads).



5) SENDING TEXT AND ATTACHMENTS

When composing new mails, the view window's "Attach" button adds selected files
as attachments, to be sent with the email's main text when the View window's
"Send" is clicked.  Attachment files may be of any type; they are selected in
a pop-up dialog, but are not loaded until Send.  The view window's "Parts"
button displays attachments already added.

The main text of the message (in the view window editor) is sent as a simple
message if there are no attachments, or as the first part of a multi-part MIME
message if there are.  In both cases, the main message text is always sent as
plain text.  HTML files may be attached to the message, but there is no support
for text-or-HTML multi-part alternative format for the main text, nor for
sending the main text as HTML only.  Not all clients can handle HTML, and
PyMailGUI's text-based view windows have no HTML editing tools.

Multi-part nesting is never applied: composed mails are always either a simple
body, or a linear list of parts containing the main message text and attachment
files.

For mail replies and forwards, headers are given intial values, the main
message text (described in the prior section) is wrapped and quoted with '>'
prefixes, and any attachments in the original message are stripped.  Only
new attachments added are sent with the message.

To send to multiple addresses, separate each recipient's address in To and Cc
fields with semicolons.  For instance:
        tim@oreily.com; "Smith, Bob" <bob@bob.com>; john@nasa.gov
Note that because these fields are split on semicolons without full parsing,
a recipient's address should not embed a ';'.  For replies, this is handled
automatically: the To field is prefilled with the original message's From,
using either the original name and address, or just the address if the name
contains a ';' (a rare case).  Cc and Bcc headers fields are ignored if they
contain just the initial "?" when sent.

Successfully sent messages are saved in a local file whose name you list in the
mailconfig.py module.  Sent mails are saved if the variable "sentmailfile" is
set to a valid filename; set to an empty string to disable saves.  This file
may be opened using the Open button of the GUI's list windows, and its content
may be viewed, processed, deleted, saved, and so on within the GUI, just like a
manually saved mail file.  Also like manually saved mail files, the sent-file
list window is automatically updated whenever a new message is sent, if it is
open (there is no need to close and reopen to see new sends).  If this file
grows too large to open, you can delete its content with Delete, after possibly
saving sent mails you wish to keep to another file with Save.

Note that some ISPs may require that you be connected to their systems in order
to use their SMTP servers (sending through your dial-up ISP's server while
connected to a broadband provider may not work--try the SMTP server at your
broadband provider instead), and some SMTP servers may require authentication
(set the "smtpuser" variable in the mailconfig.py module to force authentication
logins on sends).  See also the Python library module smptd for SMTP server
tools; in principle, you could run your own SMTP server locally on 'localhost'.



6) MAIL TRANSFER OVERLAP

PyMailGUI runs mail server transfers (loads, sends, and deletes) in threads, to
avoid blocking the GUI.  Transfers never block the GUI's windows, and windows
do not generally block other windows.  Users can view, create, and process mails
while server transfers are in progress.  The transfers run in the background,
while the GUI remains active.

PyMailGUI also allows mail transfer threads to overlap in time.  In particular,
new emails may be written and sent while a load or send is in progress, and mail
loads may overlap with sends and other mail loads already in progress.  For
example, while waiting for a download of mail headers or a large message, you
can open a new Write window, compose a message, and send it; the send will
overlap with the load currently in progress.  You may also load another mail,
while the load of a large mail is in progress.

While mail transfers are in progress, popup windows display their current
progress as a message counter.  When sending a message, the original edit
View window is popped back up automatically on Send failures, to save or retry.
Because delete operations may change POP message numbers on the server, this
operation disables other deletions and loads while in progress.

Offline mail save-file loads and deletes are also threaded: these threads may
overlap in time with server transfers, and with operations on other open save
files.  Saves are disabled if the source or target file is busy with a load
or save operation.  Quit is never allowed while any thread is busy.



7) MAIL DELETION

Mail is not removed from POP servers on Load requests, but only on explicit
"Delete" button deletion requests, if verified by the user.  Delete requests
are run immediately, upon user verification.

To delete your mail from a server and process off-line: in the server list
window select the All checkbutton, Save to a local file, and then Delete to
delete all mails from the server; use Open to open the save file later to view
and process saved mail.

When deleting from the server window, the mail list (and any already-viewed
message text) is not reloaded from server, if the delete was successful.  If
the delete fails, all email must be reloaded, because some POP message numbers
may have changed; the reload occurs automatically.  Delete in a file list
window deletes from the loal file only.

As of version 2.1, PyMailGUI automatically matches messages selected for
deletion with their headers on the mail server, to ensure that the correct
mail is deleted.  If the mail index is out of synch with the server, mails
that do not match the server are not deleted, since their POP message numbers
are no longer accurate.  In this event, an error is displayed, and a full reload
of the mail index list is automatically performed; you do not need to stop and
restart PyMailGUI to reload the index list.  This can slow deletions (it adds
roughly one second per deleted mail on the test machine used), but prevents
the wrong mail from being deleted.  See the POP message number synchronization
errors description in the next section.



8) INBOX MESSAGE NUMBER SYNCHRONIZATION

PyMailGUI does header matching in order to ensure that deletions only delete
the correct messages, and periodically detect synchronization errors with the
server.  If a synchronization error message appears, the operation is cancelled,
and a full index reload from the server is automatically performed.  You need
not stop and restart PyMailGUI and reload the index, but must reattempt the
operation after the reload.

The POP email protocol assigns emails a relative message number, reflecting
their position in your inbox.  In the server List window, PyMailGUI loads its
mail index list on demand from the server, and assumes it reflects the content
of your inbox from that point on.  A message's position in the index list is
used as its POP relative message number for later loads and deletes.

This normally works well, since newly-arrived emails are added to the end
of the inbox.  However, the message numbers of the index list can become out
of synch with the server in two ways:

A) Because delete operations change POP relative message numbers in the inbox,
deleting messages in another email client (even another PyMailGUI instance)
while the PyMailGUI server list window is open can invalidate PyMailGUI's
message index numbers.  In this case, the index list window may be arbitrarily
out of synch with the inbox on the server.

B) It is also possible that your ISP may automatically delete emails from
your inbox at any time, making PyMailGUI's email list out of synch with message
numbers on the mail server.  For example, some ISPs may automatically move an
email from the inbox to the undeliverable box, in response to a fetch failure.
If this happens, PyMailGUI's message numbers will be off by one, according to
the server's inbox.

To accomodate such cases, PyMailGUI 2.1 always matches messages to be deleted
against the server's inbox, by comparing already-fetched headers text with the
headers text returned for the same message number; the delete only occurs if
the two match.  In addition, PyMailGUI runs a quick check for out-of-synch
errors by comparing headers for just the last message in the index, whenever
the index list is updated, and whenever full messages are fetched.

This header matching adds a slight overhead to deletes, index loads, and mail
fetches, but guarantees that deletes will not remove the wrong message, and 
ensures that the message you receive corresponds to the item selected in the
server index List window.  The synch test overhead is one second or less on
test machines used - it requires 1 POP server connect and an inbox size and
(possibly) header text fetch.

In general, you still shouldn't delete messages in PyMailGUI while running a
different email client, or that client's message numbers may become confused
unless it has simlar synchronization tests.  If you receive a synch error
pop-up on deletes or loads, PyMailGUI automatically begins a full reload of
the mail index list displayed in the server List window.



9) LOADING EMAIL

To save time, Load requests only fetch mail headers, not entire messages.
View operations fetch the entire message, unless it has been previously viewed
(already-loaded messages are cached).  Multiple message downloads may overlap
in time, and may overlap with message editing and sends.

In addition, after the intial load, new Load requests only fetch headers of
newly-arrived messages.  All headers must be refetched after a delete failure,
however, due to possibly changed POP message numbers.

PyMailGUI only is connected to a mail server while a load, send, or delete
operation is in progress.  It does not connect at all unless one of these
operations is attempted, and disconnects as soon as the operation finishes.
You do not need any Internet connectivity to run PyMailGUI unless you attempt
one of these operations.  In addition, you may disconnect from the Internet
when they are not in progress, without having to stop the GUI--the program
will reconnect on the next transfer operation.

Note: if your POP mail server does support the TOP command for fetching mail
headers (most do), see variable "srvrHasTop" in the mailtools.py module to
force full message downloads.

Also note that, although PyMailGUI only fetches message headers initially if
your email server supports TOP, this can still take some time for very large
inboxes; as a rule of thumb, use save-mail files and deletions to keep your
inbox small.



10) THE mailconfig CONFIGURATION MODULE

Change the mailconfig.py module file in PyMailGUI's home directory on your
own machine to reflect your email server names, user name, email address, and
optional mail signature line added to all composed mails.

Most settings in this module are optional, or have reasonable preset defaults.
However, you must minimally set this module's "smtpservername" variable to send
mail, and its "popservername" and "popusername" to load mail from a server.
These are simple Python variables assigned to strings in this file.  See the
module file and its embedded comments for details.

The mailconfig module's "listheaders" attribute can also be set to a tuple of
string header field name, to customize the set of headers displayed in list
windows; mail size is always displayed last.  Similarly mailconfig's
"viewheaders" attribute can extend the set of headers shown in a View window
(though From, To, Cc, and Subject fields are always shown).  List windows
display message headers in fixed-width columns.

Variables in the mailconfig module also can be used to tailor the font used in
list windows ("fontsz"), the column at which viewed and quoted text is
automatically wrapped ("wrapsz"), colors and fonts in various windows, the
local file where sent messages are saved, the opening of mail parts, and more;
see the file's source code for more details.

Note: use caution when changing this file, as PyMailGUI may not run at all if
some of its variables are missing.  You may wish to make a backup copy before
editing it in case you need to restore its defaults.  A future version of this
system may have a configuration dialog which generates this module's code.



11) DEPENDENCIES

This client-side program currently requires Python and Tkinter.  It uses Python
threads, if installed, to avoid blocking the GUI.  Sending and loading email
from a server requires an Internet connection.  Requires Python 2.3 or later,
and uses the Python "email" standard library module to parse and compose mail
text.  Reuses a number of modules located in the PP3E examples tree.



12) MISCELLANEOUS HINTS

- Use ';' between multiple addresses in "To" and "Cc" headers. 
- Passwords are requested if needed, and not stored by PyMailGUI.
- You may list your password in a file named in mailconfig.py.
- Reply and Fwd automatically quote the original mail text.
- Save pops up a dialog for selecting a file to hold saved mails.
- Save always appends to the save file, rather than erasing it.
- Delete does not reload message headers, unless it fails.
- Delete checks your inox to make sure the correct mail is deleted.
- Fetches detect inbox changes and automatically reload index list.
- Open and save dialogs always remember the prior directory.
- To print emails, "Save" to a text file and print with other tools.
- Click this window's Source button to view its source-code files.
- Watch http://www.rmi.net/~lutz for updates and patches
- This is an Open Source system: change its code as you like.
- See the SpamBayes system for a spam filter for incoming email.
"""

if __name__ == '__main__': 
    print helptext                    # to stdout if run alone
    raw_input('Press Enter key')      # pause in DOS console popups
