django-decorator-include
========================

Include Django URL patterns with decorators.

Maintened by Twidi, on https://github.com/twidi/django-decorator-include
based on the  original work from Jeff Kistler on https://github.com/jeffkistler/django-decorator-include


Installation
------------

Installation from Source
````````````````````````

Unpack the archive, ``cd`` to the source directory, and run the following
command::

    python setup.py install

Installation with pip
`````````````````````

Assuming you have pip installed, run the following command to install from PyPI::

    pip install django-decorator-include

Installation with pip and git
`````````````````````````````

Assuming you have pip and git installed, run the following command to
install from the GitHub repository::

    pip install git+git://github.com/twidi/django-decorator-include.git#egg=django-decorator-include

Requirements
------------

The only required package is ``future``, used for compatibility with python 2 and python 3

Usage
-----

``decorator_include`` is intended for use in URL confs as a replacement
for the ``django.conf.urls.include`` function. It works in almost
the same way as ``include``, however the first argument should be either a
decorator or an iterable of decorators to apply, in reverse order, to all
included views. Here is an example URL conf::

    from django.conf.urls import url
    from django.contrib.auth.decorators import login_required

    from decorator_include import decorator_include

    urlpatterns = [
        url(r'^$', 'mysite.views.index', name='index'),
        url(r'^secret/', decorator_include(login_required, 'mysite.secret.urls'),
    ]

Running tests
-------------

If `decorator_include` is in the `INSTALLED_APPS` of your project, and it was installed with the test (ie not from PyPI) simply run::

    django-admin test decorator_include

(you may want to use ``django-admin`` or  ``./manage.py`` depending on your installation)

If you are in a fresh virtualenv to work on ``decorator_include``, install the django version you want::

    pip install django

Then make the ``decorator_include`` module available in your python path. For example, with ``virtualenv-wrapper``, considering you are at the root of the ``django-decorator-include`` repository, simply do::

    add2virtualenv src

Or simply::

    pip install -e .

Then to run the tests, this library provides a test project, so you can launch them this way::

    DJANGO_SETTINGS_MODULE=decorator_include.tests.testproject.settings django-admin.py test decorator_include

Or simply launch the ``runtests.sh`` script (it will run this exact command)::

    ./runtests.sh

Supported versions
------------------

============== ===============
Django version Python versions
============== ===============
1.4, 1.5       2.6, 2.7
1.6            2.6, 2.7, 3.2, 3.3
1.7, 1.8       2.7, 3.2, 3.3, 3.4
1.9            2.7, 3.4, 3.5
1.10           2.7, 3.4, 3.5
============== ===============

