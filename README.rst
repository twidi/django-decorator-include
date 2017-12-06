django-decorator-include
========================

Include Django URL patterns with decorators.

Maintained by Twidi, on https://github.com/twidi/django-decorator-include based
on the original work from Jeff Kistler on
https://github.com/jeffkistler/django-decorator-include.


Installation
------------

Installation from Source
````````````````````````

Unpack the archive, ``cd`` to the source directory, and run the following
command::

    python setup.py install

Installation with pip
`````````````````````

Assuming you have pip installed, run the following command to install from
PyPI::

    pip install django-decorator-include

Installation with pip and git
`````````````````````````````

Assuming you have pip and git installed, run the following command to install
from the GitHub repository::

    pip install git+git://github.com/twidi/django-decorator-include.git#egg=django-decorator-include

Usage
-----

``decorator_include`` is intended for use in URL confs as a replacement for the
``django.conf.urls.include`` function. It works in almost the same way as
``include``, however the first argument should be either a decorator or an
iterable of decorators to apply, in reverse order, to all included views. Here
is an example URL conf::

    from django.conf.urls import url
    from django.contrib.auth.decorators import login_required

    from decorator_include import decorator_include

    urlpatterns = [
        url(r'^$', 'mysite.views.index', name='index'),
        url(r'^secret/', decorator_include(login_required, 'mysite.secret.urls')),
    ]

Running tests
-------------

If you are in a fresh virtualenv to work on ``decorator_include``, install the
Django version you want::

    pip install django

Then make the ``decorator_include`` module available in your python path. For
example, with ``pip``, considering you are at the root of the
``django-decorator-include`` repository, simply do::

    pip install -e .

Then to run the tests, this library provides a test project, so you can launch
them this way::

    django-admin test --settings=tests.settings tests

Or simply launch the ``runtests.sh`` script (it will run this exact command)::

    ./runtests.sh

Supported versions
------------------

============== ==================
Django version Python versions
============== ==================
1.11           2.7, 3.4, 3.5, 3.6
2.0            3.4, 3.5, 3.6
============== ==================
