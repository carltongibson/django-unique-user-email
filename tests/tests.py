from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase


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
