  
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from . import models

# Register your models here.


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'full_name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Information'), {'fields': ('full_name', 'phone_number')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (
            _('Website Roles'),
            {'fields': ('is_kalafex_admin', 'is_artist', 'is_customer')}
        ),
        (
            _('Registration details'),
            {'fields': ('is_first_login',)}
        ),
        (_('Important Dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'full_name', 'is_kalafex_admin',
                       'is_artist', 'is_customer', 'is_first_login')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.KalafexAdmin)
admin.site.register(models.Artist)
admin.site.register(models.Customer)
admin.site.register(models.Address)