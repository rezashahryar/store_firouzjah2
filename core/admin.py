from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(models.OtpRequest)


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    model = models.User
    ordering = ('username',)
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_superuser')
    list_display = ['username', 'email', 'is_superuser', 'is_staff', 'is_active']

    fieldsets = (
        ('Authentication', {
            "fields": (
                'username', 'email', 'password', 'first_name', 'last_name', 'mobile'
            ),
        }),
        ('group permissions', {
            'fields': (
                'user_permissions', 'groups',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_staff', 'is_active', 'is_superuser'
            ),
        }),
        ('last login', {
            'fields': (
                'last_login',
                'date_joined',
            ),
        }),
    )

    add_fieldsets = (
        ('Create User', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')
        }),
    )
