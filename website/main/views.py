# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import TemplateView
from forms import NameForm

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

# Add this view
class LoginPageView(TemplateView):
    template_name = "login.html"

# Add this view
class SignupPageView(TemplateView):
    template_name = "signup.html"

class ProfilePageView(TemplateView):
    template_name = "profile.html"

from django.http import HttpResponse

def search_form(request):
    return render(request, 'search_form.html')

def search(request):
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)