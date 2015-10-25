from __future__ import unicode_literals
import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = '8qw5o&7!g&4kg#+4jr6y%qoj6(1s1ufjqo1#x)fqaca&)$2)ba'

BASE_DIR = os.path.dirname(__file__)

def absolute_path(path):
    return os.path.normpath(os.path.join(BASE_DIR, path))

SITE_ID = 1
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': absolute_path('database.sqlite3'),
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'decorator_include',
]

ROOT_URLCONF = 'decorator_include.tests.urls'

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
