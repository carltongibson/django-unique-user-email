from django.apps import AppConfig


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
        User.Meta.constraints = [
            models.UniqueConstraint(
                name="unique_user_email",
                fields=["email"],
                # deferrable=models.Deferrable.DEFERRED,
            ),
        ]
        User._meta.constraints = User.Meta.constraints
        # ... as long as original_attrs is not updated.
        # User._meta.original_attrs["constraints"] = User.Meta.constraints
