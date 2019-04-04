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


class UsersDesks(models.Model):
    """
    This one is created to get all desks in which user is participant
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desks = models.ForeignKey(Desk, on_delete=models.CASCADE)
