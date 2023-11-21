from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from unique_user_email.forms import (
    UniqueUserEmailChangeForm,
    UniqueUserEmailCreationForm,
)


class UniqueUserEmailAdmin(BaseUserAdmin):
    """The unique user email admin."""

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    form = UniqueUserEmailChangeForm
    add_form = UniqueUserEmailCreationForm
    prepopulated_fields = {"username": ["email"]}


admin.site.unregister(User)
admin.site.register(User, UniqueUserEmailAdmin)
