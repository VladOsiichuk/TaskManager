from django.contrib import admin
from .model import Desk, Task, Column, Comment

admin.site.register(Desk)
admin.site.register(Task)
admin.site.register(Column)
admin.site.register(Comment)
