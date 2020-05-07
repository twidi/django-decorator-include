Changelog
=========

UNRELEASED *v3.0*
-----------------
* Handle namespace/app_name the same way as Django `include` function
* Added support for Django 2.2 and 3.0
* Added support for Python 3.8

Release *v2.1* - ``2018-11-23``
-------------------------------
* Added support for Django 2.1 and Python 3.7.
* Fixed ImportError when installed on environments with an old version of
  setuptools.

Release *v2.0* - ``2018-01-26``
-------------------------------
* Removed support for Python 2
* Removed support for Django < 2

Release *v1.4* - ``2018-01-25``
-------------------------------
* Removed support for Python 3.2 and 3.3.
* Removed support for Django < 1.11.
* Added support for Django 2.0.
* Added ``tox`` for tests matrix
* Configured setup using ``setup.cfg``

Release *v1.3* - ``2017-05-16``
-----------------------------
* Removed support for Django < 1.8 and Python 2.6.
* Added support for Django 1.11 and Python 3.6.
* Added support for passing a 2-tuple to ``decorator_include()`` as allowed by
  Django's ``include()``.

Release *v1.2* - ``2016-12-28``
---------------------------------
* Official support for Django 1.10.

Release *v1.1* - ``2016-12-15``
-------------------------------
* Stop importing module in ``__init__``.

Release *v1.0* - ``2016-03-13``
---------------------------------
* First official release, adding support for Django 1.9.

Release *v0.2* - ``2014-11-09``
---------------------------------
* Support for Python 3 and Django 1.6+.

Release *v0.1* - ``2014-03-18``
---------------------------------
* Initial version by Jeff Kistler (date: 2011-06-07).
