from functools import wraps
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.conf import settings
from django.conf.urls import url
from photoManage.urls import urlpatterns
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson


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

def render(template):
    '''Specify a template to render a view to'''

    def wrapper(method):

        @wraps(method)
        def view(request, *args, **kwargs):

            context = method(request, *args, **kwargs)
            if isinstance(context, HttpResponse):
                return context

            return render_to_response(template, context, context_instance=RequestContext(request))

        return view

    return wrapper

def render_to_json(method):
    '''Renders a view to a serialized json object'''

    @wraps(method)
    def view(request, *args, **kwargs):
        request.csrf = csrf(request)
        context = method(request, *args, **kwargs)
        if isinstance(context, HttpResponse):
            return context
        return HttpResponse(simplejson.dumps(context or {}))

    return view


def json_request(method):
    '''Deserializes json request, sets object to request.JSON'''

    @wraps(method)
    def view(request, *args, **kwargs):
        request.JSON = simplejson.loads(request.body or '{}')
        return method(request, *args, **kwargs)
    return view