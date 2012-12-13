__author__ = 'Alex'

from django import forms
from accounts.models import UserCreateForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect


#TODO Response Redirect instead of render_to_response

def register(request):
    if request.method == 'POST':
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
                return render_to_response("accounts/register.html", {
                    'form': form,
                    'register': True,
                    }, context_instance=RequestContext(request))
    else:
        form = UserCreateForm()
    return render_to_response("accounts/register.html", {
        'form': form,
        'register': True,
    }, context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    return redirect('accounts/login.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/photos/')
            else:
                error_message = "Sorry, your account is not active"
                return render_to_response("accounts/login.html",{
                    'error_message': error_message,
                    'login':True,
                    }, context_instance=RequestContext(request))
        else:
            error_message = "Invalid Login"
            return render_to_response("accounts/login.html", {
                'error_message': error_message,
                'login':True,
            }, context_instance=RequestContext(request))
    else:
        return render_to_response("accounts/login.html", {
          'login':True,
        }, context_instance=RequestContext(request))
