#!/usr/bin/env python

import os

from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fp:
        return fp.read()


setup(
    name='django-decorator-include',
    version='1.3',
    license='BSD',
    description='Include Django URL patterns with decorators.',
    long_description=read('README.rst'),
    author='Jeff Kistler',
    author_email='jeff@jeffkistler.com',
    url='https://github.com/twidi/django-decorator-include/',
    py_modules=['decorator_include'],
    install_requires=['Django>=1.11'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
