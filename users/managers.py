from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _
from phonenumber_field.phonenumber import PhoneNumber

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where phone is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError(_('Users must have a phone number'))
        
        phoneNumber = PhoneNumber.from_string(phone)
        if phoneNumber.is_valid():
            user = self.model(phone=phone, **extra_fields)
            user.set_password(password)
            user.save()
            return user
        else:
            raise ValueError(_('Please enter a valid phone number'))


    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(phone, password, **extra_fields)
        