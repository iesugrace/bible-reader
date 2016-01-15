import transaction
from BTrees.OOBTree import OOBTree

def getContainer(root, contName):
    """ return a ZODB container, create it if not yet exists
    """
    cont = getattr(root, contName, None)
    if cont is None:
        cont = OOBTree()
        setattr(root, contName, cont)
        transaction.commit()
    return cont
