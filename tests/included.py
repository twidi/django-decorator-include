from django.http import HttpResponse
from django.urls import include, path


def testify(request):
    return HttpResponse('testify!')


urlpatterns = [
    path('included/', include('tests.included2')),
    path('test/', testify, name='testify'),
]
