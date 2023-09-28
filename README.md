Django Controlled Vocabularies
==============================

[![Build Status](https://github.com/unt-libraries/django-controlled-vocabularies/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/unt-libraries/django-controlled-vocabularies/actions)


About
-----

The django-controlled-vocabularies app is used to manage vocabularies used by the UNT Libraries digital infrastructure which
includes: The [UNT Digital Library](http://digital.library.unt.edu), [The Portal to Texas History](http://texashistory.unt.edu), and the [Gateway to Oklahoma History](http://gateway.okhistory.org).


Requirements
------------

* Django 4.2
* Python 3.8 - 3.10


System Requirements
------------

* libxml2
* libxslt


Installation
------------

These instructions are for adding django-controlled-vocabularies as an app to an existing Django project.
If you simply want to test out the app to see how it works, skip to the Developing/Testing section further below.

1.  Download and install from source code.

    Install with SSH:
    ```sh
        $ pip install git+ssh://git@github.com/unt-libraries/django-controlled-vocabularies
    ```

    OR install with HTTPS:
    ```sh
        $ pip install git+https://github.com/unt-libraries/django-controlled-vocabularies
    ```

2.  Add app and sites framework to INSTALLED_APPS.
    ```python
        INSTALLED_APPS = (
            'django.contrib.sites',
            'controlled_vocabularies'
        )
    ```

3.  Set the VOCAB_DOMAIN setting to your own desired location.
    ```python
        VOCAB_DOMAIN = 'http://example.org/vocabs/'
    ```

4.  Set the SITE_ID.
    ```python
        SITE_ID = 1
    ```

5.  Include the URLs.
    ```python
        urlpatterns = [
            path('admin/', admin.site.urls),
            path('vocabularies/', include('controlled_vocabularies.urls'))
        ]
    ```

6.  Migrate the database.

    ```sh
        $ python manage.py migrate
    ```


Developing/Testing
------------------

This will allow you to run the tests, easily make changes to the app, and visually inspect the app locally in your browser.

1.  Clone the repository into a location of your choosing:
    ```sh
        $ git clone git@github.com:unt-libraries/django-controlled-vocabularies.git
    ```

2.  Navigate into the repository:
    ```sh
        $ cd django-controlled-vocabularies
    ```

3.  Prepare and activate a Python virtual environment for the app using virtualenv, pyenv, pipenv, or something similar. Leave it activated for the remaining instructions.

4.  Install all requirements:
    ```sh
        $ pip install -r requirements.txt
    ```

5.  Run the test suite if desired:
    ```sh
        $ pytest
    ```
    Note: You may also use `tox` to run the test suite, but there is only a benefit to this method if you have multiple Python versions available, and it does not require a virtual environment.

6.  Run the migrations (steps 6-10 are for viewing/testing the app locally from your web browser):
    ```sh
        $ python manage.py migrate
    ```

7.  Create a superuser for yourself so you can access the admin portion of the app:
    ```sh
        $ python manage.py createsuperuser
    ```

8.  Run the test server:
    ```sh
        $ python manage.py runserver
    ```

9.  Navigate to localhost:8000/vocabularies/ in your browser and test the app as desired. The admin interface is located at localhost:8000/admin/.

10.  Stop the test server when you're done by pressing `Ctrl+c`


License
-------

See LICENSE.txt


Contributors
------------

* Brandon Fredericks
* [Mark Phillips](https://github.com/vphill)
* [Joey Liechty](https://github.com/yeahdef)
* [Gio Gottardi](https://github.com/somexpert)
* [Madhulika Bayyavarapu](https://github.com/madhulika95b)
* [Gracie Flores-Hays](https://github.com/gracieflores)
