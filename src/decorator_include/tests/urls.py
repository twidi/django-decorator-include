from __future__ import unicode_literals
from django.conf.urls import patterns, url
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from decorator_include import decorator_include


def index(request):
    return HttpResponse('Index!')

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^include/', decorator_include(login_required, 'decorator_include.tests.included')),
)
