from django import forms
from django.conf import settings
from django.contrib.admin.sites import site as default_site
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, models
from django.test import TestCase
from unique_user_email.admin import UniqueUserEmailAdmin
from unique_user_email.backend import EmailBackend
from unique_user_email.forms import AuthenticationForm


class UniqueEmailTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass",
        )

    def test_model_form_disallows_duplicate_emails(self):
        class UserForm(forms.ModelForm):
            class Meta:
                model = User
                fields = ["username", "email"]

        form = UserForm(
            data={
                "username": "testuser2",
                "email": self.user.email,
            }
        )
        self.assertIs(False, form.is_valid())

    def test_full_clean_disallows_duplicate_emails(self):
        user2 = User(
            username="testuser2",
            email=self.user.email,
            password="testpass2",
        )

        with self.assertRaisesMessage(
            ValidationError,
            "User with this Email address already exists.",
        ):
            user2.full_clean()

    def test_model_save_disallows_duplicate_emails(self):
        user2 = User(
            username="testuser2",
            email=self.user.email,
            password="testpass2",
        )
        with self.assertRaisesMessage(
            IntegrityError,
            "UNIQUE constraint failed: auth_user.email",
        ):
            user2.save()

    def test_user_model_constraints(self):
        unique_user_email_unique_constraint = models.UniqueConstraint(
            fields=["email"],
            name="unique_user_email",
        )
        unique_user_email_check_constraint = models.CheckConstraint(
            check=~models.Q(email__exact=""),
            name="check_required_email",
            violation_error_message="A valid 'Email address' is required.",
        )
        self.assertEqual(User._meta.constraints[0], unique_user_email_unique_constraint)
        self.assertEqual(User._meta.constraints[1], unique_user_email_check_constraint)
        self.assertEqual(
            User._meta.original_attrs.get("constraints")[0],
            unique_user_email_unique_constraint,
        )
        self.assertEqual(
            User._meta.original_attrs.get("constraints")[1],
            unique_user_email_check_constraint,
        )

    def test_user_model_required_fields(self):
        self.assertIn("email", User.REQUIRED_FIELDS)


class EmailBackendTests(TestCase):
    def test_none_for_username_logins(self):
        """
        Authenticate with username and password returns None.
        """
        request = None
        backend = EmailBackend()
        self.assertIsNone(
            backend.authenticate(request, username="testUser", password="testPassword")
        )

    def test_user_can_login_with_email(self):
        """
        Authenticate with email and password returns the user.
        """
        user = User.objects.create_user(
            username="testUser", email="a@b.com", password="testPassword"
        )
        request = None
        backend = EmailBackend()
        authed_user = backend.authenticate(
            request, email="a@b.com", password="testPassword"
        )
        self.assertEqual(user, authed_user)

    def test_email_backend_is_installed(self):
        """
        EmailBackend is listed in settings.AUTHENTICATION_BACKENDS.
        """
        self.assertIn(
            "unique_user_email.backend.EmailBackend",
            settings.AUTHENTICATION_BACKENDS,
        )


class AuthenticationFormTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testUser",
            email="a@b.com",
            password="testPassword",
            is_staff=True,
        )

    def test_get_credentials_with_email(self):
        """
        get_credentials() returns email kwarg.
        """
        form = AuthenticationForm(data={"login": "a@b.com", "password": "testPassword"})
        self.assertIs(True, form.is_valid(), form.errors)
        self.assertEqual(
            {"email": "a@b.com", "password": "testPassword"}, form.get_credentials()
        )

    def test_login_view(self):
        tests = ["testUser", "a@b.com"]
        for test in tests:
            with self.subTest(login=test):
                data = {"login": test, "password": "testPassword"}
                url = "/accounts/login/"
                response = self.client.post(url, data=data)
                self.assertRedirects(
                    response,
                    settings.LOGIN_REDIRECT_URL,
                )


class UniqueUserEmailAdminTest(TestCase):
    """Unique user email admin tests."""

    admin = UniqueUserEmailAdmin(User, default_site)

    def test_add_fieldsets(self):
        """Test add fieldsets."""
        self.assertIn("email", self.admin.add_fieldsets[0][1]["fields"])
