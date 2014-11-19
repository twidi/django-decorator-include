#!/usr/bin/env python

import os
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'django-decorator-include',
    version = '0.1',
    license = 'BSD',
    description = 'Include Django URL patterns with decorators.',
    long_description = read('README.rst'),
    author = 'Jeff Kistler',
    author_email = 'jeff@jeffkistler.com',
    url = 'https://github.com/twidi/django-decorator-include/',
    packages = ['decorator_include', 'decorator_include.tests'],
    package_dir = {'': 'src'},
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
