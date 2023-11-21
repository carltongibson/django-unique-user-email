from django.db import migrations, models

from unique_user_email.utils import AuthAddConstraint


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        AuthAddConstraint(
            model_name="user",
            constraint=models.UniqueConstraint(
                fields=("email",), name="unique_user_email"
            ),
        ),
    ]
