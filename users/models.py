from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    phone = PhoneNumberField(null=False, blank=False, unique=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ('username',)

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.get_full_name()} ({self.phone})'