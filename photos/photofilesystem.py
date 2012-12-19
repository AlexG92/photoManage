import os

### get_directory is possibly creating a new path, should I be doing this in another function?

def upload_photo_file_path(instance, filename):
    if instance.album is None:
        return os.path.join('photographs/', '%s' % instance.owner, filename)
    else:
        return os.path.join('photographs/', '%s' % instance.owner, '%s' % instance.album, filename)

def get_directory(owner, filename=None, album=None, createDir=True):
    absolutePath = os.path.realpath('')
    if filename is None:
        filename = ''
    if album is None:
        album = ''
    directory = os.path.join('%s' % absolutePath, 'media\photographs\\', '%s' % owner, '%s' % album)
    if not os.path.exists(directory) and createDir == True:
        os.makedirs(directory)
    return os.path.join('%s' % directory, '%s' % filename)

def change_directory(source, destination):
    if os.path.exists(destination):
        raise Exception('Album with that name exists, please pick a unique album name')
    else:
        os.rename(source, destination)


#from photos.photofilesystem import *
#get_directory('alex','great photo', 'alaska')