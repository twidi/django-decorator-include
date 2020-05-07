from django.contrib import admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.urls import path

from decorator_include import decorator_include


def identity(func):
    return func


def only_god(func):
    def check(user):
        if user.is_authenticated and user.username == 'god':
            return True
        raise PermissionDenied
    return user_passes_test(check)(func)


def index(request):
    return HttpResponse('Index!')


app_name = 'app_name_tests'

urlpatterns = [
    path('', index, name='index'),
    path('include/', decorator_include(login_required, 'tests.included')),
    path('admin/', decorator_include(identity, admin.site.urls)),
    path('only-god/', decorator_include([login_required, only_god], 'tests.included')),
]
