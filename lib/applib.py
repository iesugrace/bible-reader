import os, sys
from subprocess import Popen, PIPE

def defaultFormater(data, color=True, n=1):
    """ This formater is for formatting
    the bible verses. 'n' parameter controls
    the number of newline characters to prepend.
    """
    eles = (data['book'], data['chap'], data['verse'], data['content'])
    if color and os.isatty(sys.stdout.fileno()):
        fmt   = '\033[0;32m%s\033[0m'   # book
        fmt  += '\033[1;32m{\033[0m'    # left brace
        fmt  += '\033[1;34m%s\033[0m'   # chapter
        fmt  += ':'                     # colon separator
        fmt  += '\033[1;34m%s\033[0m'   # verse
        fmt  += '\033[1;32m}\033[0m'    # right brace
        fmt  += ' %s'                   # content
        text = fmt % eles
    else:
        text = "%s{%s:%s} %s" % eles
    return  ''.join(['\n'] * n) + text

class Pager:
    """ Read data from the stdin, write it
    to the stdout using the LESS program
    """
    prog = 'less'
    def __init__(self, args=[]):
        self.pager = Popen([self.prog] + args, stdin=PIPE)

    def write(self, *chunks, isBytes=True):
        for data in chunks:
            if not isBytes:
                data = data.encode()
            self.pager.stdin.write(data)

    def go(self):
        self.pager.stdin.close()
        self.pager.wait()

def pageOut(records_data, formater=None, color=True):
    """ Apply color to the text, pipe the
    text to a pager, for a better viewing.
    the 'records_data' is a iterable of dicts.
    """
    if not records_data:
        return

    if not formater:
        formater = defaultFormater

    pager = Pager(['-XRF'])
    itr   = iter(records_data)
    try:
        first = next(itr)
        pager.write(formater(first, color, n=0), isBytes=False)
    except StopIteration:
        return
    for data in itr:
        pager.write(formater(data, color), isBytes=False)
    pager.go()
