from django.db import models
from django.contrib.auth.models import User, Group
from desk.models import Desk
from django.db import models


class CustomUser(User):
    pass


class CustomGroup(Group):
    """
    @related_desk: desk to which group is related
    """
    related_desk = models.ForeignKey(Desk, on_delete=models.CASCADE)

