from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UsernameField
from django.core import exceptions, validators
from django.utils.translation import gettext_lazy as _


class EmailRequiredMixin(object):
    """A mixin to handle a email field as required on user forms."""

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True


class UniqueUserEmailCreationForm(EmailRequiredMixin, BaseUserCreationForm):
    """Override default Django UserCreationForm with required email."""


class UniqueUserEmailChangeForm(EmailRequiredMixin, BaseUserChangeForm):
    """Override default Django UserChangeForm with required email."""


class AuthenticationForm(forms.Form):
    """
    Form allowing login by username or email.

    - Takes login and password.
    - Maps to credentials for authentication, using email if login is an email
      address.
    - Exposes the user for use in the view.
    """

    login = UsernameField(max_length=150, label=_("Username or Email"))
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def get_credentials(self):
        """
        Maps the login to credentials for authentication.

        If the login is an email address, use the email kwarg, otherwise use
        the username kwarg.
        """
        credentials = {}
        login = self.cleaned_data.get("login")
        if self.is_email(login):
            credentials["email"] = login
        else:
            credentials["username"] = login
        credentials["password"] = self.cleaned_data.get("password")
        return credentials

    def is_email(self, login):
        try:
            validators.validate_email(login)
            is_email = True
        except exceptions.ValidationError:
            is_email = False
        return is_email

    def clean(self):
        super().clean()
        if self._errors:
            return

        credentials = self.get_credentials()
        self.user_cache = authenticate(self.request, **credentials)
        if self.user_cache is None:
            raise forms.ValidationError(
                "Please enter a correct username/email and password. Note that both "
                "fields are case-sensitive."
            )
        return self.cleaned_data

    def get_user(self):
        return self.user_cache
