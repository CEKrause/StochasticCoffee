# -*- coding: utf-8 -*-
# user models.
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


class User(models.Model):
    
    #PID	First Name	Last Name	email	branch	division	frequency
    id = models.AutoField(primary_key=True)
    first_name  = models.CharField(max_length=200)
    last_name	 = models.CharField(max_length=200)
    email	 = models.CharField(max_length=200,unique=True, null=False)
    branch	 = models.CharField(max_length=200)
    division	 = models.CharField(max_length=200)
    frequency = models.CharField(max_length=200)
    password = models.CharField(max_length=7, default='0', editable=False)

    
    def __str__(self):
        return self.first_name +' '+ self.last_name
    

class Match(models.Model):
    id = models.AutoField(primary_key=True)
    first_user = models.ForeignKey('app.User', on_delete=models.CASCADE,related_name='first_user')
    second_user = models.ForeignKey('app.User', on_delete=models.CASCADE,related_name='second_user')
    date_match = models.DateTimeField(blank=False, null=False)
    
    def __str__(self):
        return self.first_user +' , '+ self.second_user +' : '+ str(date_match)
    