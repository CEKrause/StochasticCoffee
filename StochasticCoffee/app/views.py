# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.utils.dateformat import format
from django.views import View
from django.views.generic.edit import FormView

from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, RegistrationForm
from .models import User

# defination of views

def home(request):
    return render(request, 'home.html', {})

def signup(request):
    return render(request, 'signup.html', {})



def profile(request, user):
    return render(request, 'profile.html', {'user': user})
    
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.get(email=email)

        
        return profile(request, user)
#        return render(request, 'profile.html', {'user': user})
    
    
    
    return render(request, 'login.html', {})





"""
    subject = form.cleaned_data['subject']
    message = form.cleaned_data['message']
    sender = form.cleaned_data['sender']
    cc_myself = form.cleaned_data['cc_myself']

    recipients = ['info@example.com']
    if cc_myself:
        recipients.append(sender)

    send_mail(subject, message, sender, recipients)
"""