"""
This module works as follows:

>>> spams(3)
'spamspamspam'
>>> shrubbery()
'spamspamspamspam!!!'
"""

def spams(N):
    return 'spam' * N

def shrubbery():
    return spams(4) + '!!!'

if __name__ == '__main__':
    import doctest
    doctest.testmod()
