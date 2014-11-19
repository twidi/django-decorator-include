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
`````````````````````````````

Assuming you have pip installed, run the following command to install from pypi::

    pip install django-decorator-include

Installation with pip and git
`````````````````````````````

Assuming you have pip and git installed, run the following command to
install from the GitHub repository::

    pip install git+git://github.com/twidi/django-decorator-include.git#egg=django-decorator-include

Usage
-----

``decorator_include`` is intended for use in URL confs as a replacement
for the ``django.conf.urls.defaults.include`` function. It works in almost
the same way as ``include``, however the first argument should be either a
decorator or an iterable of decorators to apply, in reverse order, to all
included views. Here is an example URL conf::

    from django.conf.urls.defaults import *
    from django.contrib.auth.decorators import login_required

    from decorator_include import decorator_include

    urlpatterns = patterns('',
        url(r'^$', 'mysite.views.index', name='index'),
        url(r'^secret/', decorator_include(login_required, 'mysite.secret.urls'),
    )
