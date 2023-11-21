from django.apps import AppConfig
from django.db.models import Q


class UniqueUserEmailConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "unique_user_email"

    def ready(self):
        from django.contrib.auth.models import User
        from django.db import models

        # Updating the field itself triggers the auto-detector
        # field = User._meta.get_field("email")
        # field._unique = True
        #
        # But setting a constraint does not...
        unique_user_email_constraints = User.Meta.constraints = [
            models.UniqueConstraint(
                fields=["email"],
                name="unique_user_email",
                # deferrable=models.Deferrable.DEFERRED,
            ),
            models.CheckConstraint(
                check=~Q(email__exact=""),
                name="check_required_email",
                violation_error_message="A valid 'Email address' is required.",
            ),
        ]
        User._meta.constraints = unique_user_email_constraints
        # ... as long as original_attrs is not updated.
        User._meta.original_attrs["constraints"] = unique_user_email_constraints
        User.REQUIRED_FIELDS = ("email",)
