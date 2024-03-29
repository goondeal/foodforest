from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = CustomUser

    list_display = ('email', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('phone', 'email', 'password')}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        (_("Important dates"), {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('phone',)
    ordering = ('-date_joined',)


admin.site.register(CustomUser, CustomUserAdmin)
