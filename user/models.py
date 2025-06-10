from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from utils.models import TimestampModel


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("올바른 이메일을 입력하세요.")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_active = False
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)


class User(AbstractBaseUser, PermissionsMixin, TimestampModel):
    objects = UserManager()

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    last_login = models.DateTimeField(null=True, blank=True, auto_now=True)

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
