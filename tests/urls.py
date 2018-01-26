from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import path

from decorator_include import decorator_include


def identity(func):
    return func


def index(request):
    return HttpResponse('Index!')


urlpatterns = [
    path('', index, name='index'),
    path('include/', decorator_include(login_required, 'tests.included')),
    path('admin/', decorator_include(identity, admin.site.urls)),
]
