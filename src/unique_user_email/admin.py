from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class UniqueUserEmailAdmin(BaseUserAdmin):
    """The unique user email admin."""

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )


admin.site.unregister(User)
admin.site.register(User, UniqueUserEmailAdmin)
