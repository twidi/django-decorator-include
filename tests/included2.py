from django.http import HttpResponse
from django.urls import path


def deeply_nested(request):
    return HttpResponse("deeply nested!")


urlpatterns = [
    path("deeply_nested/", deeply_nested, name="deeply_nested"),
]
