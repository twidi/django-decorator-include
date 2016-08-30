from __future__ import unicode_literals
from django.conf.urls import include, url
from django.http import HttpResponse


def testify(request):
    return HttpResponse('testify!')

urlpatterns = [
    url(r'^included/', include('decorator_include.tests.included2')),
    url(r'^test/$', testify, name='testify'),
]
