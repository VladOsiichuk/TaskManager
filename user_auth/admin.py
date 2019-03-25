from django.contrib import admin
from django.conf import settings
from .models import User, CustomGroup

admin.site.register(User)
admin.site.register(CustomGroup)
