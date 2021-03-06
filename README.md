Django Controlled Vocabularies
==============================

[![Build Status](https://travis-ci.org/unt-libraries/django-controlled-vocabularies.svg?branch=master)](https://travis-ci.org/unt-libraries/django-controlled-vocabularies)


About
-----

The django-controlled-vocabularies app is used to manage vocabularies used by the UNT Libraries digital infrastructure which
includes: The [UNT Digital Library](http://digital.library.unt.edu), [The Portal to Texas History](http://texashistory.unt.edu), and the [Gateway to Oklahoma History](http://gateway.okhistory.org).


Requirements
------------

* Django 2.2
* Python 3.6 - 3.7


System Requirements
------------

* libxml2
* libxslt


Installation
------------

1.  Download and install from source code.
    ```sh
        $ pip install git+git://github.com/unt-libraries/django-controlled-vocabularies.git
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
