django-decorator-include
========================

Include Django URL patterns with decorators.

Maintained by Stéphane "Twidi" Angel, and Jon Dufresne on
https://github.com/twidi/django-decorator-include
based on the original work from Jeff Kistler on
https://github.com/jeffkistler/django-decorator-include.

.. image:: https://badge.fury.io/py/django-decorator-include.svg
    :target: https://badge.fury.io/py/django-decorator-include

.. image:: https://travis-ci.org/twidi/django-decorator-include.svg?branch=develop
    :target: https://travis-ci.org/twidi/django-decorator-include

Installation
------------

Assuming you have pip installed, run the following command to install from
PyPI::

    pip install django-decorator-include


Usage
-----

``decorator_include`` is intended for use in URL confs as a replacement for the
``django.conf.urls.include`` function. It works in almost the same way as
``include``, however the first argument should be either a decorator or an
iterable of decorators to apply, in reverse order, to all included views. Here
is an example URL conf::

    from django.urls import path
    from django.contrib.auth.decorators import login_required

    from decorator_include import decorator_include

    from mysite.views import index

    urlpatterns = [
        path('', views.index, name='index'),
        path('secret/', decorator_include(login_required, 'mysite.secret.urls')),
    ]


Supported versions
------------------

=============== ==================
Django versions Python versions
=============== ==================
2.0             3.4, 3.5, 3.6
=============== ==================

All library versions to use for old Django/Python support
---------------------------------------------------------

=============== ======================= ==================
Django versions Python versions         Library versions
=============== ======================= ==================
1.4, 1.5        2.6, 2.7                1.2
1.6             2.6, 2.7, 3.2, 3.3      1.2
1.7             2.7, 3.2, 3.3, 3.4      1.2
1.8             2.7, 3.2, 3.3, 3.4, 3.5 1.3
1.9, 1.10       2.7, 3.4, 3.5           1.3
1.11            2.7, 3.4, 3.5, 3.6      1.4.x (>=1.4.1,<2)
2.0             3.4, 3.5, 3.6           2.0
=============== ======================= ==================


Development
-----------

Make sure you are in a virtualenv on a valid python version.

Grab the sources from Github::

    git clone -b develop https://github.com/twidi/django-decorator-include.git


Then go into the newly created ``django-decorator-include`` directory and install
the few needed libraries::

    pip install -r requirements.txt


To run the tests, this library provides a test project, so you can launch
them this way::

    django-admin test --settings=tests.settings tests

Or simply launch the ``runtests.sh`` script (it will run this exact command)::

    ./runtests.sh

Base your work on the ``develop`` branch. Iit should be the default branch on
git assuming you used the ``-b develop`` argument on the ``git clone``
command as shown above.

When creating the pull request, ensure you are using the correct base
(twidi/django-decorator-include on develop).
