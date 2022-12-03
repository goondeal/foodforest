from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone = PhoneNumberField(null=True, blank=True, unique=True)

    username_validator = None
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.get_full_name()} ({self.phone})'