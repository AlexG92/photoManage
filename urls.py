from django.conf.urls import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
   # Examples:
   # url(r'^$', '{{ project_name }}.views.home', name='home'),
   # url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),
   # url(r'^$', 'views.index'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^photos/', include('photos.urls')),
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
                            (r'^media/(?P<path>.*)$',
                             'serve', {
                                'document_root': 'media',
                                'show_indexes': True }),)