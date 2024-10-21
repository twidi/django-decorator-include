django-decorator-include
========================

Include Django URL patterns with decorators.

Maintained by Steve Mapes, Stéphane "Twidi" Angel, and Jon Dufresne on
https://github.com/twidi/django-decorator-include
based on the original work from Jeff Kistler on
https://github.com/jeffkistler/django-decorator-include.

.. image:: https://img.shields.io/pypi/v/django-decorator-include.svg
    :target: https://pypi.org/project/django-decorator-include/

.. image:: https://github.com/twidi/django-decorator-include/workflows/build/badge.svg
    :target: https://github.com/twidi/django-decorator-include/actions?query=workflow%3Abuild

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/twidi/django-decorator-include

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/twidi/django-decorator-include

Installation
------------

Assuming you have pip installed, run the following command to install from
PyPI::

    pip install django-decorator-include

Usage
-----

``decorator_include`` is intended for use in URL confs as a replacement for the
``django.conf.urls.include`` function. It works in almost the same way as
``include`` however the first argument should be either a decorator or an
iterable of decorators to apply to all included views (if an iterable, the order of the
decorators is the order in which the functions will be applied on the views).
Here is an example URL conf

.. code-block:: python

    from django.contrib import admin
    from django.core.exceptions import PermissionDenied
    from django.urls import path
    from django.contrib.auth.decorators import login_required, user_passes_test

    from decorator_include import decorator_include

    from mysite.views import index

    def only_user(username):
        def check(user):
            if user.is_authenticated and user.username == username:
                return True
            raise PermissionDenied
        return user_passes_test(check)

    urlpatterns = [
        path('', views.index, name='index'),
        # will redirect to login page if not authenticated
        path('secret/', decorator_include(login_required, 'mysite.secret.urls')),
        # will redirect to login page if not authenticated
        # will return a 403 http error if the user does not have the "god" username
        path('admin/', decorator_include([login_required, only_user('god')], admin.site.urls),
    ]

Supported versions
------------------

=============== ========================
Django versions Python versions
=============== ========================
2.2             3.6, 3.7, 3.8, 3.9
3.0             3.6, 3.7, 3.8, 3.9
3.1             3.6, 3.7, 3.8, 3.9
3.2             3.6, 3.7, 3.8, 3.9, 3.10
4.0             3.8, 3.9, 3.10
4.1             3.8, 3.9, 3.10, 3.11
4.2             3.8, 3.9, 3.10, 3.11, 3.12
5.0             3.10, 3.11, 3.12, 3.13
5.1             3.10, 3.11, 3.12, 3.13, 3.14

=============== ========================

* Python 3.11 only works with Django 4.1.3+

All library versions to use for old Django/Python support
---------------------------------------------------------

=============== =============================== ==================
Django versions Python versions                  Library versions
=============== =============================== ==================
1.4, 1.5        2.6, 2.7                         1.2
1.6             2.6, 2.7, 3.2, 3.3               1.2
1.7             2.7, 3.2, 3.3, 3.4               1.2
1.8             2.7, 3.2, 3.3, 3.4, 3.5          1.3
1.9, 1.10       2.7, 3.4, 3.5                    1.3
1.11            2.7, 3.4, 3.5, 3.6               1.4.x (>=1.4.1,<2)
2.0             3.4, 3.5, 3.6, 3.7               3.0
2.1             3.5, 3.6, 3.7                    3.0
2.2             3.5, 3.6, 3.7, 3.8, 3.9          3.0
3.0             3.6, 3.7, 3.8, 3.9               3.0
3.1             3.6, 3.7, 3.8, 3.9               3.0
3.2             3.6, 3.7, 3.8, 3.9, 3.10         3.0
4.0             3.8, 3.9, 3.10                   3.1
4.1             3.8, 3.9, 3.10                   3.1
4.2             3.10, 3.11, 3.12                 3.1
4.2             3.10, 3.11, 3.12                 3.1
5.0             3.10, 3.11, 3.12, 3.13           3.1
5.1             3.10, 3.11, 3.12, 3.13, 3.14     3.1, 3.2 *
=============== =============================== ==================

* Python 3.14 flagged as supported added in 3.2

Development
-----------

Make sure you are in a virtualenv on a valid python version.

Grab the sources from Github::

    git clone -b develop https://github.com/twidi/django-decorator-include.git


Then go into the newly created ``django-decorator-include`` directory and install
the package in editable mode::

    pip install -e .


To run the tests, this library provides a test project, so you can launch
them this way::

    django-admin test --settings=tests.settings tests

Or simply launch the ``runtests.sh`` script (it will run this exact command)::

    ./runtests.sh

This project uses `pre-commit`_ to automatically run `black`_ , `flake8`_ and `isort`_ on
every commit. If you haven't already, first install pre-commit using the
project's documentation. Then, to enable pre-commit for
django-decorator-include::

    pre-commit install

After that, the next commit will run the tools on changed files. If you want to
run the pre-commit hooks on all files, use::

    pre-commit run --all-files

The above command is also available as a tox environment::

    tox -e lint

Base your work on the ``develop`` branch. Iit should be the default branch on
git assuming you used the ``-b develop`` argument on the ``git clone``
command as shown above.

When creating the pull request, ensure you are using the correct base
(twidi/django-decorator-include on develop).

.. _pre-commit: https://pre-commit.com/
.. _flake8: https://flake8.pycqa.org/
.. _isort: https://pycqa.github.io/isort/
.. _black: https://github.com/psf/black/

