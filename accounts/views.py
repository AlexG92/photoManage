from django import forms
from accounts.models import UserCreateForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from photoManage.util import uri

@uri('accounts/register/', method='GET')
def register(request):
    form = UserCreateForm()
    return render_to_response("accounts/register.html", {
        'form': form,
        'register': True,
    }, context_instance=RequestContext(request))

@uri('accounts/register/', method='POST')
def register(request):
    form = UserCreateForm(request.POST)
    if form.is_valid():
        username = form.clean_username()
        password = form.clean_password2()
        form.save()
        user = authenticate(username=username, password=password)
        if user.is_authenticated():
            login(request, user)
            return HttpResponseRedirect("/photos/")
        else:
            return render_to_response("/accounts/register.html",
                {
                    'form': form,
                    'register': True,
                }, context_instance=RequestContext(request))
    else:
        return render_to_response("accounts/register.html",
            {
                'form': form,
                'register': True,
            }, context_instance=RequestContext(request))


@uri('accounts/login')
def login_user(request):
    return render_to_response("accounts/login.html",
        {
            'login':True,
        }, context_instance=RequestContext(request))

@uri('accounts/login', method='POST')
def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/photos/')
        else:
            messages.error(request, 'Sorry, your account is not active')
            return render_to_response("accounts/login.html",
                {
                    'login':True,
                }, context_instance=RequestContext(request))
    else:
        messages.error(request, 'Invalid Login')
        return render_to_response("accounts/login.html",
            {
                'login':True,
            }, context_instance=RequestContext(request))


@uri('accounts/logout/')
def logout_user(request):
    logout(request)
    return redirect('/accounts/login/')