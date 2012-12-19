import os
import Image
from photofilesystem import get_directory

def create_thumb(owner, filename, album=None):
    photoLocation = get_directory(owner, filename, album)
    saveLocation = os.path.join(get_directory(owner), 'thumbnails\\')
    if not os.path.exists(saveLocation):
        os.makedirs(saveLocation)
    photo = Image.open(photoLocation)
    photo.thumbnail((189,189), Image.ANTIALIAS)
    photo.save(saveLocation + filename)

#from photos.thumbnail import *
#create_thumb('alex4', 'disk_green_3.png')