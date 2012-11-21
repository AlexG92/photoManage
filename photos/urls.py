__author__ = 'Alex'

from django.conf.urls import *
from photos.views import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^album/(?P<album_id>\d+)$', album),

)