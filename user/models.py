from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from utils.models import TimestampModel


class User(AbstractBaseUser, PermissionsMixin, TimestampModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    last_login = models.DateTimeField(null=True, blank=True, auto_now=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email