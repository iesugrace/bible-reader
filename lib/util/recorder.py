from util.common import getContainer
from interact import interact
import ZODB, transaction
from BTrees.OOBTree import OOBTree


"""Keep all opened database connections, to prevent
reopen the same database within the same process.
"""
_connections = {}
def _db_is_opened(conn):
    try:
        root = conn.root
    except ZODB.POSException.ConnectionStateError:
        return False
    else:
        return True


def _open_db(path, **db_args):
    conn = _connections.get(path)
    if not (conn and _db_is_opened(conn)):
        conn = ZODB.connection(path, **db_args)
        _connections[path] = conn
    return conn


def _close_db(path):
    conn = _connections.get(path)
    if conn and _db_is_opened(conn):
        conn.close()
        del _connections[path]


class Recorder:
    '''
    A class for managing simple records.
    The records stored in a flat fashion, that is, one key, one value
    '''
    def __init__(self, db_path, **db_args):
        self.db_path = db_path
        self.db_args = db_args

    def opendb(self):
        if 'db' not in self.__dict__ or not self.db:
            connection = _open_db(self.db_path, **self.db_args)
            self.db    = getContainer(connection.root, 'main')

    def closedb(self):
        _close_db(self.db_path)
        del self.db

    def commit(self):
        transaction.commit()

    def save(self, key, ent):
        self.opendb()
        self.db[key] = ent
        self.commit()

    def dbinstance(self):
        '''
        open the database and return the container
        '''
        self.opendb()
        return self.db

    def add(self, key, ent):
        self.save(key, ent)

    def delete(self, key):
        self.opendb()
        del self.db[key]
        self.commit()

    def search(self, filter):
        # filter is a function takes two arguments, and returns Boolean
        # subclass must overload the __str__ method
        self.opendb()
        entries = ((k, v) for k,v in self.db.items() if filter(k, v))
        return entries

    def list(self):
        return Recorder.search(self, filter=(lambda k,v: True))

    def menu(self):
        choices = [
            ['add', self.add],
            ['list', self.list],
            ['search', self.search],
            ['edit', self.edit],
            ['delete', self.delete]
        ]
        i, junk = interact.printAndPick([x for x, y in choices], prompt='choice: ', lineMode=True)
        action = choices[i][-1]
        action()


class Logger(Recorder):
    def dellast(self):
        self.opendb()
        keys = [k for k in self.db]
        if not keys: return

        key = sorted(keys)[-1]
        log = self.db[key]
        i = interact.readstr('%s\nconfirm? [n] ' % log, default='n')
        if i not in ('y', 'Y'):
            return
        self.delete(key)


if __name__ == '__main__':
    logger = Logger('/tmp/testlog')
    #logger.add('sex', 'Male')
    #logger.add('age', 34)
    logger.list()
    logger.dellast()
