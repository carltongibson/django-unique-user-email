from django.db import migrations, models

target_app_label = "auth"


class CustomAddConstraint(migrations.AddConstraint):
    """
    Override AddConstraint app_label to target auth.User
    """

    def state_forwards(self, app_label, state):
        state.add_constraint(target_app_label, self.model_name_lower, self.constraint)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model(target_app_label, self.model_name)
        if self.allow_migrate_model(schema_editor.connection.alias, model):
            schema_editor.add_constraint(model, self.constraint)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model(target_app_label, self.model_name)
        if self.allow_migrate_model(schema_editor.connection.alias, model):
            schema_editor.remove_constraint(model, self.constraint)


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        CustomAddConstraint(
            model_name="user",
            constraint=models.UniqueConstraint(
                fields=("email",), name="unique_user_email"
            ),
        ),
        CustomAddConstraint(
            model_name="user",
            constraint=models.CheckConstraint(
                check=models.Q(("email__exact", ""), _negated=True),
                name="check_required_email",
                violation_error_message="A valid 'Email address' is required.",
            ),
        ),
    ]
