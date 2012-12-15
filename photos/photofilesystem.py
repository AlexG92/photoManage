import os

def uploadimagepath(instance, filename):
    if instance.album is None:
        return os.path.join('photographs/', '%s' % instance.owner, filename)
    else:
        return os.path.join('photographs/', '%s' % instance.owner, '%s' % instance.album, filename)

def moveimage(owner, filename, album=None):
    return os.path.join('photographs/', '%s' % instance.owner, '%s' % instance.album, filename)