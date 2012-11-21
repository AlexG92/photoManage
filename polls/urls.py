from django.conf.urls import *

urlpatterns = patterns('polls.views',
   # Examples:
   # url(r'^$', '{{ project_name }}.views.home', name='home'),
   # url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),
    url(r'^$', 'index'),
    url(r'^(?P<poll_id>\d+)/$', 'detail'),
    url(r'^(?P<poll_id>\d+)/results/$', 'results'),
    url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),

)