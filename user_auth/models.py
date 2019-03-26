from desk.model import Desk
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    PermissionsMixin, AbstractUser, UserManager, Group


class CustomUserManager(UserManager):
    pass


class User(AbstractUser):
    objects = CustomUserManager()
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']


class CustomGroup(Group):
    """
    @related_desk: desk to which group is related
    """

    related_desk = models.ForeignKey(Desk, on_delete=models.CASCADE, default=None)
