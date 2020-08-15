###############################################################################
# parsing and attachment extract, analyse, save (see __init__ for docs, test)
###############################################################################

import os, mimetypes                               # mime: type to name
import email.Parser
from email.Message import Message
from mailTool import MailTool

class MailParser(MailTool):
    """
    methods for parsing message text, attachments

    subtle thing: Message object payloads are either a simple
    string for non-multipart messages, or a list of Message
    objects if multipart (possiby nested); we don't need to
    distinguish between the two cases here, because the Message
    walk generator always returns self first, and so works fine
    on non-multipart messages too (a single object is walked);

    for simple messages, the message body is always considered
    here to be the sole part of the mail;  for miltipart messages,
    the parts list includes the main message text, as well as all
    attachments;  this allows simple messages not of type text to
    be handled like attachments in a UI (e.g., saved, opened);
    Message payload may also be None for some oddball part types;
    """

    def walkNamedParts(self, message):
        """
        generator to avoid repeating part naming logic
        skips multipart headers, makes part filenames
        message is already-parsed email.Message object
        doesn't skip oddball types: payload may be None
        """
        for (ix, part) in enumerate(message.walk()):    # walk includes message
            maintype = part.get_content_maintype()      # ix includes multiparts 
            if maintype == 'multipart':
                continue                                # multipart/*: container
            else:
                filename, contype = self.partName(part, ix)
                yield (filename, contype, part)

    def partName(self, part, ix):
        """
        extract filename and content type from message part;
        filename: tries Content-Disposition, then Content-Type
        name param, or generates one based on mimetype guess;
        """
        filename = part.get_filename()                # filename in msg hdrs?
        contype  = part.get_content_type()            # lower maintype/subtype
        if not filename:
            filename = part.get_param('name')         # try content-type name
        if not filename:
            if contype == 'text/plain':               # hardcode plain text ext
                ext = '.txt'                          # else guesses .ksh!
            else:
                ext = mimetypes.guess_extension(contype)
                if not ext: ext = '.bin'              # use a generic default
            filename = 'part-%03d%s' % (ix, ext)
        return (filename, contype)

    def saveParts(self, savedir, message):
        """
        store all parts of a message as files in a local directory;
        returns [('maintype/subtype', 'filename')] list for use by
        callers, but does not open any parts or attachments here;
        get_payload decodes base64, quoted-printable, uuencoded data;
        mail parser may give us a None payload for oddball types we
        probably should skip over: convert to str here to be safe;
        """
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        partfiles = []
        for (filename, contype, part) in self.walkNamedParts(message):
            fullname = os.path.join(savedir, filename)
            fileobj  = open(fullname, 'wb')             # use binary mode
            content  = part.get_payload(decode=1)       # decode base64,qp,uu
            fileobj.write(str(content))                 # make sure is a str
            fileobj.close()
            partfiles.append((contype, fullname))       # for caller to open
        return partfiles

    def saveOnePart(self, savedir, partname, message):
        """
        ditto, but find and save just one part by name
        """
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        fullname = os.path.join(savedir, partname)
        (contype, content) = self.findOnePart(partname, message)
        open(fullname, 'wb').write(str(content))
        return (contype, fullname)
    
    def partsList(self, message):
        """"
        return a list of filenames for all parts of an
        already-parsed message, using same file name logic
        as saveParts, but do not store the part files here
        """
        validParts = self.walkNamedParts(message)
        return [filename for (filename, contype, part) in validParts]

    def findOnePart(self, partname, message):
        """
        find and return part's content, given its name
        intended to be used in conjunction with partsList
        we could also mimetypes.guess_type(partname) here
        we could also avoid this search by saving in dict
        """
        for (filename, contype, part) in self.walkNamedParts(message):
            if filename == partname:
                content = part.get_payload(decode=1)          # base64,qp,uu
                return (contype, content)
        
    def findMainText(self, message):
        """
        for text-oriented clients, return the first text part;
        for the payload of a simple message, or all parts of
        a multipart message, looks for text/plain, then text/html,
        then text/*, before deducing that there is no text to
        display;  this is a heuristic, but covers most simple,
        multipart/alternative, and multipart/mixed messages;
        content-type defaults to text/plain if not in simple msg;        

        handles message nesting at top level by walking instead
        of list scans;  if non-multipart but type is text/html,
        returns the htlm as the text with an html type: caller
        may open in webbrowser;  if non-multipart and not text,
        no text to display: save/open in UI;  caveat: does not
        try to concatenate multiple inline text/plain parts
        """
        # try to find a plain text
        for part in message.walk():                        # walk visits messge
            type = part.get_content_type()                 # if non-multipart
            if type == 'text/plain':
                return type, part.get_payload(decode=1)    # may be base64,qp,uu

        # try to find a html part
        for part in message.walk():
            type = part.get_content_type()
            if type == 'text/html':
                return type, part.get_payload(decode=1)    # caller renders

        # try any other text type, including xml
        for part in message.walk():
            if part.get_content_maintype() == 'text':
                return part.get_content_type(), part.get_payload(decode=1)

        # punt: could use first part, but it's not marked as text 
        return 'text/plain', '[No text to display]'

    # returned when parses fail
    errorMessage = Message()
    errorMessage.set_payload('[Unable to parse message - format error]')
    
    def parseHeaders(self, mailtext):
        """
        parse headers only, return root email.Message object
        stops after headers parsed, even if nothing else follows (top)
        email.Message object is a mapping for mail header fields
        payload of message object is None, not raw body text
        """
        try:
            return email.Parser.Parser().parsestr(mailtext, headersonly=True)
        except:
            return self.errorMessage

    def parseMessage(self, fulltext):
        """
        parse entire message, return root email.Message object
        payload of message object is a string if not is_multipart()
        payload of message object is more Messages if multiple parts
        the call here same as calling email.message_from_string()
        """
        try:
            return email.Parser.Parser().parsestr(fulltext)       # may fail!
        except:
            return self.errorMessage     # or let call handle? can check return

    def parseMessageRaw(self, fulltext):
        """
        parse headers only, return root email.Message object
        stops after headers parsed, for efficiency (not yet used here)
        payload of message object is raw text of mail after headers
        """
        try:
            return email.Parser.HeaderParser().parsestr(fulltext)
        except:
            return self.errorMessage
