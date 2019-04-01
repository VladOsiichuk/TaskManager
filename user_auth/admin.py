from django.contrib import admin
from django.conf import settings
from .models import User, CustomGroup, UsersDesks

admin.site.register(User)
admin.site.register(CustomGroup)
admin.site.register(UsersDesks)
