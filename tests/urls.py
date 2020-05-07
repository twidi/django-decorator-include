from django.contrib import admin
from django.contrib.auth.decorators import (
    login_required, permission_required, user_passes_test
)
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.urls import path

from decorator_include import decorator_include


def identity(func):
    return func


def only_user(username):
    def check(user):
        if user.is_authenticated and user.username == username:
            return True
        raise PermissionDenied
    return user_passes_test(check)


def index(request):
    return HttpResponse('Index!')


app_name = 'app_name_tests'

urlpatterns = [
    path('', index, name='index'),
    path('include/', decorator_include(login_required, 'tests.included')),
    path('admin/', decorator_include(identity, admin.site.urls)),
    path('only-god/', decorator_include([login_required, only_user('god')], 'tests.included')),
    path('with-perm/', decorator_include(
        [login_required, permission_required('auth.is_god', raise_exception=True)],
        'tests.included'
    ))
]
