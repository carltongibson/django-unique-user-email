from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class EmailBackend(BaseBackend):
    """
    Authentication backend to allow login by email.

    - authenticate() uses email and password credentials.
    """

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id, is_active=True)
        except User.DoesNotExist:
            return None
        return user

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user. See ModelBackend.
            User().set_password(password)
        else:
            if user.check_password(password):
                return user
