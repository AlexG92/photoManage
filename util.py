from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.conf import settings
from django.conf.urls import url
from urls import *

def uri(pattern, method='GET', enabled=True, cache={}):

    # Normalize pattern
    pattern = pattern.lstrip('^').lstrip('/').rstrip('$').rstrip('/')
    if pattern:
        pattern = '%s/' % pattern
    pattern = '^%s$' % pattern


    def resolver(request, *args, **kwargs):

        view = cache[pattern].get(request.method)
        if view:
            return view(request, *args, **kwargs)
        else:
            return HttpResponseNotFound()

    def wrapper(view):

        if enabled:
            if pattern in cache:
                cache[pattern][method] = view
            else:
                cache[pattern] = {method: view}
                urlpatterns.append(url(pattern, resolver))

        return view

    return wrapper