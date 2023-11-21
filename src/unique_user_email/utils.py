from django.db import migrations


class AuthAddConstraint(migrations.AddConstraint):
    """
    Override AddConstraint app_label to target auth.User
    """

    target_app_label = "auth"

    def state_forwards(self, app_label, state):
        state.add_constraint(
            self.target_app_label, self.model_name_lower, self.constraint
        )

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model(self.target_app_label, self.model_name)
        if self.allow_migrate_model(schema_editor.connection.alias, model):
            schema_editor.add_constraint(model, self.constraint)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model(self.target_app_label, self.model_name)
        if self.allow_migrate_model(schema_editor.connection.alias, model):
            schema_editor.remove_constraint(model, self.constraint)
