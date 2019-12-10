Change Log
==========


x.x.x
-----

* Upgraded Python compatibility to Python 3.6 - 3.7.
* Removed support for Python 2.
* Removed VOCABULARIES_URL from test settings and README, as that is a defunct setting.


2.1.0
-----

* Added the /all.[json|py] and /all-verbose.[json/py] URL patterns. Existing /all and /all-verbose patterns will be deprecated.


2.0.0
-----

* Upgraded Django compatibility to include 1.10 and 1.11.
* Removed Django 1.7 - 1.9 compatibility.
* Made code compliant with PEP-8 style rules.


1.0.1
-----

* Added CHANGELOG.md to keep track of changes.
* Updated app to work with django 1.6 - 1.8
* Fixed [issue #2](https://github.com/unt-libraries/django-controlled-vocabularies/issues/2) where leading and
trailing whitespace was saved if entered for the name and/or label fields on the models.
* Fixed [issue #10](https://github.com/unt-libraries/django-controlled-vocabularies/issues/10) by correcting some
of the model helper strings.
* Corrected typos in the about page.
* Fixed [issue #11](https://github.com/unt-libraries/django-controlled-vocabularies/issues/11) by removing static
highlighting of `Home` navbar tab.
* Fixed [issue #7](https://github.com/unt-libraries/django-controlled-vocabularies/issues/7) by adding initial
migration.
* Fixed a test which was inconsistently passing.


1.0.0
-----

Initial release.
