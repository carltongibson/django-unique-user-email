# django-unique-user-email
Enable login-by-email with the default User model for your Django project by making auth.User.email unique.

## A quick note on why?

Django's _leaky battery_ is its recommendation that you create a custom user model.
Auth is so central and so standard that, into the high-nines (99.99%?), the vast majority of projects should **never** need to customise the central auth model.
This is a battery that Django should very much provide.

There's a complexity tax from exposing the auth model.
There's a performance tax as the auth model becomes a generic dumping ground for User related data that has nothing to do with authentication.
There's a learning tax as users hit the custom user model, and the (frankly, misplaced) warnings about it's importance.

Again, the vast majority of projects should **never** need to customise the central auth model.

> Can I login with my email?

Most projects, all folks wanted was login-by-email.
By making the default `auth.User` model have unique email field, and a few other bits and bobs, this is enabled.

The goal of this package is to give you the tools you need for login-by-email with Django's default `User` model. I believe this should be a option in Django itself, so it's a proof-of-concept for a future discussion there too.

A longer discussion: [Evolving Django’s auth.User](https://buttondown.com/carlton/archive/evolving-djangos-authuser/)

Previously, [a blog post that says a little by way of introduction](https://noumenal.es/posts/django-unique-user-email/928/).

## Overview

* Install from `pip`:

        pip install django-unique-user-email

* Add to `INSTALLED_APPS`


        INSTALLED_APPS = [
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",

            "unique_user_email",
            ...
        ]

* Migrate to add the unique constraint to `User.email`.

* Install auth backend to allow email login

        AUTHENTICATION_BACKENDS = [
            'unique_user_email.backend.EmailBackend',
            'django.contrib.auth.backends.ModelBackend',
        ]

* Use the custom `AuthenticationForm` to login with `username` or `email`.

        # urls.py
        from django.contrib.auth.views import LoginView
        from unique_user_email.forms import AuthenticationForm

        urlpatterns = [
            # Route LoginView before other auth views to match first.
            # https://docs.djangoproject.com/en/dev/topics/auth/default/#module-django.contrib.auth.views
            path(
                "accounts/login/",
                LoginView.as_view(form_class=AuthenticationForm),
                name="login",
            ),
            ...
        ]


Fuller tutorial, **Coming Soon**.


## Testing

* Clone the repo, create a virtual environment, and `pip install -e .` the package.
* You can run with `just test`.

    This wraps the full command:

        django-admin test --settings=tests.settings --pythonpath=.
