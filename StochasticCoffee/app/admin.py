# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, Match

# Registering models.

admin.site.register(User)
admin.site.register(Match)
