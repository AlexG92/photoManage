import os
import Image
from photofilesystem import get_directory
from PIL import Image, ImageChops, ImageOps

def create_thumb(owner, filename, album=None):
    photoLocation = get_directory(owner, filename, album)
    saveLocation = os.path.join(get_directory(owner), 'thumbnails\\')
    if not os.path.exists(saveLocation):
        os.makedirs(saveLocation)
    photo = Image.open(photoLocation)
    photo.thumbnail((260,260), Image.ANTIALIAS)
    thumb = ImageOps.fit(photo, (260,260), Image.ANTIALIAS, (0.5, 0.5))
    thumb.save(saveLocation + filename)
    return os.path.join('photographs\\', '%s' % owner, 'thumbnails\\', '%s' % filename)

#from photos.thumbnail import *
#create_thumb('alex4', 'disk_green_3.png')