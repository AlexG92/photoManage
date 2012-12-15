from django.db import models
import datetime
from django.utils import timezone
from django.db.models.fields.files import ImageField
from django.contrib.auth.models import User
from django import forms
import os.path
from photoManage.photos.photofilesystem import upload_photo_file_path

# Create your models here.
class Album(models.Model):
    # ...
    def __unicode__(self):
        return self.title
    def lastImage(self):
        if self.photo_set.all():
            return self.photo_set.order_by('-pub_date')[0]
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=200)

class Photo(models.Model):
# ...
    def __unicode__(self):
        return self.title
    def filename(self):
        return os.path.basename(self.photo.name)
    owner = models.ForeignKey(User)
    album = models.ForeignKey(Album, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to=upload_photo_file_path)
    pub_date = models.DateTimeField('date published')

class UploadFileForm(forms.Form):
    file = forms.ImageField()

class AlbumForm(forms.Form):
    title = forms.CharField(max_length=200)

class ChangeFileName(forms.Form):
    title = models.CharField(max_length=200)