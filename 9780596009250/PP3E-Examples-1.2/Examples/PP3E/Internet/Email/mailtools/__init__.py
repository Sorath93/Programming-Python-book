################################################################################
# interface to mail server transfers, used by pymail, PyMailGUI and PMailCGI;
# does loads, sends, parsing, composing, and deleting, with attachment parts,
# encoding, etc.;  the parser, fetcher, and sender classes here are designed
# to be mixed-in to subclasses which use their methods, or used as embedded or
# standalone objects;  also has convenience subclasses for silent mode, etc.;
# loads all if pop server doesn't do top;  doesn't handle threads or UI here,
# and allows askPassword to differ per subclass;  progress callback funcs get
# status;  all calls raise exceptions on error--client must handle in GUI/other;
# this changed from file to package: nested modules imported here for bw compat;
# TBD: in saveparts, should file be opened in text mode for text/ contypes?
# TBD: in walkNamedParts, should we skip oddballs like message/delivery-status?
################################################################################

# collect modules here, when package dir imported directly
from mailFetcher import *
from mailSender  import *
from mailParser  import *

# export nested modules here, when from mailtools import *
__all__ = 'mailFetcher', 'mailSender', 'mailParser'

# test case moved to selftest.py to allow mailconfig's
# path to be set before importing nested modules above
