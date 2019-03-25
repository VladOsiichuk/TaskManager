from django.contrib.auth.models import Group
from desk.models import Desk
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin, AbstractUser, UserManager


class UserManager(UserManager):
  pass


class User(AbstractUser):
    objects = UserManager()


class CustomGroup(Group):
    """
    @related_desk: desk to which group is related
    """
    related_desk = models.ForeignKey(Desk, on_delete=models.CASCADE)

