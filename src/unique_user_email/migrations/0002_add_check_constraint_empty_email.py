from django.db import migrations, models

from unique_user_email.utils import AuthAddConstraint


class Migration(migrations.Migration):
    dependencies = [
        ("unique_user_email", "0001_initial"),
    ]

    operations = [
        AuthAddConstraint(
            model_name="user",
            constraint=models.CheckConstraint(
                check=models.Q(("email__exact", ""), _negated=True),
                name="check_required_email",
                violation_error_message="A valid 'Email address' is required.",
            ),
        ),
    ]
