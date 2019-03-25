from django.contrib import admin
from .models import Desk, Task, Column
from django.conf import settings

admin.site.register(Desk)
admin.site.register(Task)
admin.site.register(Column)
#admin.site.register(settings.AUTH_USER_MODEL)