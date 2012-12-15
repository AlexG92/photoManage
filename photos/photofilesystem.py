import os
from django.contrib import messages

def upload_photo_file_path(instance, filename):
    if instance.album is None:
        return os.path.join('photographs/', '%s' % instance.owner, filename)
    else:
        return os.path.join('photographs/', '%s' % instance.owner, '%s' % instance.album, filename)

#### IS THERE A BETTER WAY TO DO THIS? ####
def get_directory(owner, filename=None, album=None):
    absolutePath = os.path.realpath('')
    if filename is None:
        filename = ''
    if album is None:
        album = ''
    directory = os.path.join('%s' % absolutePath, 'media\photographs\\', '%s' % owner, '%s' % album)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join('%s' % directory, '%s' % filename)

def delete_directory(request, album):
    absolutePath = os.path.realpath('')
    directory = os.path.join('%s' % absolutePath, 'media\photographs\\', '%s' % owner, '%s' % album)
    try:
        os.remove(directory)
    except Exception as e:
        messages.error(request, '%s (%s)' % (e.message, type(e)))

def change_directory():
    source = get_directory('alex4', None, 'Taest')
    destination = get_directory('alex4', None, 'Test12')
    print source
    print destination
    os.renames(source, destination)


#from photos.photofilesystem import *
#get_directory('alex','great photo', 'alaska')