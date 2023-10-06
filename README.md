# django-unique-user-email
Enable login-by-email with the default User model for your Django project by making auth.User.email unique. 


**Coming Soon**

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

The goal of this package is to give you the tools you need for login-by-email with Django's default `User` model. I believe this should be a option in Django itself, so it's a proof-of-concept for a futyre discussion there too. 

**Coming Soon**
