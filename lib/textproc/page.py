def more(data, number=0):
    from system.term import getch, Term
    from textproc.wrap import Wrap

    if not number:
        number = Term().lines() - 1
    size = number
    w = Wrap()
    limit = Term().cols()
    leftdata = None
    while True:
        while size:
            if leftdata:
                line, leftdata = leftdata, None
            line = data.readline()
            if not line: return
            while line:
                wrapped, line = w.wrap(line, limit).read()
                print(wrapped, end='')
                size -= 1
                if not size:
                    leftdata = line
                    break
        inp = getch()
        if inp == ' ':
            size = number
        elif inp == '\r':
            size = 1
        else:
            break
