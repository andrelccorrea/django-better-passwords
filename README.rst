Django Better Passwords
==================

This app provides tools to enforce stronger password policies and
expiration.

Features
--------

-  Configurable password expiration;
-  Customizable password validator;
-  Uses Django messages framework to warn the user about the expiration;
-  Prevents user from logging in after expiration and redirects to
   password change page;
-  Compatible with default Django admin and Django CMS (django-cms)
   admin;
-  Can be used to expire only staff passwords, or for all users;
-  Force password update immediately after user creation.

Requirements
------------

Requires Python >= 3.6 and Django >=2. Recommended Python 3.11 or 3.12
and Django 4.2 or 5.0;

Quick start
-----------

1. Install the lib with ``pip install django-better-passwords``.

2. Add ``'django_better_passwords.apps.BetterPasswordsConfig'`` to ``INSTALLED_APPS``.

3. Add ``'better_passwords.middleware.PasswordExpirationMiddleware'`` to
   ``MIDDLEWARE``. It should be listed after authentication, session and
   message middlewares, like this:

   .. code:: python

      MIDDLEWARE = [
         "django.middleware.security.SecurityMiddleware",
         "django.contrib.sessions.middleware.SessionMiddleware",
         "django.middleware.common.CommonMiddleware",
         "django.middleware.csrf.CsrfViewMiddleware",
         "django.contrib.auth.middleware.AuthenticationMiddleware",
         "django.contrib.messages.middleware.MessageMiddleware",
         "better_passwords.middleware.PasswordExpirationMiddleware",
         "django.middleware.clickjacking.XFrameOptionsMiddleware",
      ]

4. Add
   ``'better_passwords.validators.custom_password_validator.CustomPasswordValidator'``
   to ``AUTH_PASSWORD_VALIDATORS``. Comment out or remove
   ``'django.contrib.auth.password_validation.MinimumLengthValidator'``
   to avoid conflicting:

   .. code:: python

      AUTH_PASSWORD_VALIDATORS = [
         ...
         # {
         #     "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
         # },
         {
            "NAME": "better_passwords.validators.custom_password_validator.CustomPasswordValidator",
            "OPTIONS": {
                  "min_length": 8,
                  "max_length": 20,
                  "required_characters": "!#$%^&*()_+{}[]:\"-=,./<>?",
                  "forbidden_characters": "@",
            },
         },
      ]

5. The validator accepts 5 parameters, being:

   1. ``min_length (int)``: the minimum password length;
   2. ``max_length (int)``: the maximum password length;
   3. ``required_characters (str)``: a string containing a list of special characters of which at least ``required_characters_count`` must be present in the password;
   4. ``required_characters_count (int)``: the number of special required characters that must be present in the password;
   5. ``forbidden_characters (str)``: a string containing a list of
      characters none of which can be present in the password;

6. Aditional app settings:

   .. code:: python

      DBP_PASSWORD_EXPIRATION_DAYS = 60
      DBP_PASSWORD_CHANGE_REDIRECT_URL = "password_change"
      DBP_LOGOUT_URL = "logout"

   Attention: If ``DBP_PASSWORD_CHANGE_REDIRECT_URL`` is
   present, when a user tries to log in or navigate to any url, he will
   be redirected to the ``password_change`` page. If it is not present,
   only users who try to access the admin area will be redirected.

Contributing
------------

We use pre-commit paired with black, flake8 and isort to keep things in their rightful place.

After cloning the project:

* Create and activate a venv;
* Install pip-tools;
* Run ``pip-compile requirements.in`` and ``pip-sync requirements.txt`` to install dependencies;
* Run ``pre-commit install -f`` to install pre-commit hook. It will create a **git hook**, that will **run automatically before every commit**;

Acknowledgements
----------------

This app is inspired by
`django-password-policies-iplweb <https://github.com/iplweb/django-password-policies-iplweb>`__
and
`django-password-expire <https://pypi.org/project/django-password-expire/>`__.

Author
~~~~~~

André Corrêa - andre.lccorrea@gmail.com
