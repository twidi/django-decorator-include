"""
A replacement for ``django.conf.urls.include`` that takes a decorator,
or an iterable of view decorators as the first argument and applies them, in
reverse order, to all views in the included urlconf.
"""

from __future__ import unicode_literals

from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.utils.functional import cached_property

try:
    from django.urls import URLPattern, URLResolver
    django_2_0_patterns = True
except ImportError:
    # Django < 2.0
    from django.core.urlresolvers import RegexURLPattern as URLPattern, RegexURLResolver as URLResolver
    django_2_0_patterns = False

VERSION = (1, 4)


class DecoratedPatterns(object):
    """
    A wrapper for an urlconf that applies a decorator to all its views.
    """
    def __init__(self, urlconf_name, decorators):
        # urlconf_name is the dotted Python path to the module defining
        # urlpatterns. It may also be an object with an urlpatterns attribute
        # or urlpatterns itself.
        self.urlconf_name = urlconf_name
        try:
            iter(decorators)
        except TypeError:
            decorators = [decorators]
        self.decorators = decorators

    def decorate_pattern(self, pattern):
        if isinstance(pattern, URLResolver):
            decorated = URLResolver(
                pattern.pattern if django_2_0_patterns else pattern.regex.pattern,
                DecoratedPatterns(pattern.urlconf_name, self.decorators),
                pattern.default_kwargs,
                pattern.app_name,
                pattern.namespace,
            )
        else:
            callback = pattern.callback
            for decorator in reversed(self.decorators):
                callback = decorator(callback)
            decorated = URLPattern(
                pattern.pattern if django_2_0_patterns else pattern.regex.pattern,
                callback,
                pattern.default_args,
                pattern.name,
            )
        return decorated

    @cached_property
    def urlpatterns(self):
        # urlconf_module might be a valid set of patterns, so we default to it.
        patterns = getattr(self.urlconf_module, 'urlpatterns', self.urlconf_module)
        return [self.decorate_pattern(pattern) for pattern in patterns]

    @cached_property
    def urlconf_module(self):
        if isinstance(self.urlconf_name, six.text_type):
            return import_module(self.urlconf_name)
        else:
            return self.urlconf_name


def decorator_include(decorators, arg, namespace=None, app_name=None):
    """
    Works like ``django.conf.urls.include`` but takes a view decorator
    or an iterable of view decorators as the first argument and applies them,
    in reverse order, to all views in the included urlconf.
    """
    if app_name and not namespace:
        raise ValueError('Must specify a namespace if specifying app_name.')

    if isinstance(arg, tuple):
        # callable returning a namespace hint
        try:
            urlconf, app_name = arg
        except ValueError:
            # Passing a 3-tuple to include() is deprecated and will be removed
            # in Django 2.0.
            if namespace:
                raise ImproperlyConfigured(
                    'Cannot override the namespace for a dynamic module that provides a namespace'
                )
            urlconf, app_name, namespace = arg
    else:
        # No namespace hint - use manually provided namespace
        urlconf = arg

    decorated_urlconf = DecoratedPatterns(urlconf, decorators)
    namespace = namespace or app_name
    return (decorated_urlconf, app_name, namespace)
