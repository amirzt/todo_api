from datetime import datetime, timedelta

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.crypto import get_random_string

from user.manager import CustomUserManager


def get_yesterday():
    return datetime.now() + timedelta(days=-1)


def get_username():
    chars = 'abcdefghijklmnopqrstuvwxyz'
    code = get_random_string(length=6, allowed_chars=chars)
    return code


class CustomUser(AbstractBaseUser, PermissionsMixin):
    device_id = models.CharField(max_length=255, null=True)
    package_name = models.CharField(default='com.example.todo', null=False, max_length=100)
    username = models.CharField(max_length=50, unique=True, default=get_username)

    email = models.CharField(max_length=255, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    is_visible = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    expire_date = models.DateTimeField(default=get_yesterday)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    class Meta:
        unique_together = ('device_id', 'package_name')
