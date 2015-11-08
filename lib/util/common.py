import transaction
from BTrees.OOBTree import OOBTree

def getContainer(root, containerName):
    """
    return a ZODB container, create it if not yet exists
    """
    cont = getattr(root, containerName, None)
    if not cont:
        setattr(root, containerName, OOBTree())
        transaction.commit()
        cont = getattr(root, containerName)
    return cont

