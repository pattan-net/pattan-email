============
pattan-email
============

pattan-email is a Django app to handel sending emails via
SendGrid

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "pattan-email" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "pattan_email",
    ]

2. Include the polls URLconf in your project urls.py like this::

    path("communications/", include("pattan_email.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Define the following in your settings file
        SENDGRID_API_KEY= 

5. Start the development server and visit the admin to create an email.

6. Visit the ``/communications/`` URL to send an email.
