from django.conf.urls import *
from accounts.views import *

urlpatterns = patterns('',
    url(r'^login/$',  login_user),
    url(r'^logout/$', logout_user),
    url(r'^register.html', register),
)