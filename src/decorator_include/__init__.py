"""
A replacement for ``django.conf.urls.include`` that takes a decorator,
or an iterable of view decorators as the first argument and applies them, in
reverse order, to all views in the included urlconf.
"""

from __future__ import unicode_literals
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.utils import six

try:
    from importlib import import_module
except ImportError:
    # For python 2.6
    from django.utils.importlib import import_module


class DecoratedPatterns(object):
    """
    A wrapper for an urlconf that applies a decorator to all its views.
    """
    def __init__(self, urlconf_name, decorators):
        self.urlconf_name = urlconf_name
        try:
            iter(decorators)
        except TypeError:
            decorators = [decorators]
        self.decorators = decorators
        if not isinstance(urlconf_name, six.string_types):
            self._urlconf_module = self.urlconf_name
        else:
            self._urlconf_module = None

    def decorate_pattern(self, pattern):
        if isinstance(pattern, RegexURLResolver):
            regex = pattern.regex.pattern
            urlconf_module = pattern.urlconf_name
            default_kwargs = pattern.default_kwargs
            namespace = pattern.namespace
            app_name = pattern.app_name
            urlconf = DecoratedPatterns(urlconf_module, self.decorators)
            decorated = RegexURLResolver(
                regex, urlconf, default_kwargs,
                app_name, namespace
            )
        else:
            callback = pattern.callback
            for decorator in reversed(self.decorators):
                callback = decorator(callback)
            decorated = RegexURLPattern(
                pattern.regex.pattern,
                callback,
                pattern.default_args,
                pattern.name
            )
        return decorated

    def _get_urlpatterns(self):
        try:
            patterns = self.urlconf_module.urlpatterns
        except AttributeError:
            patterns = self.urlconf_module
        return [self.decorate_pattern(pattern) for pattern in patterns]
    urlpatterns = property(_get_urlpatterns)

    def _get_urlconf_module(self):
        if self._urlconf_module is None:
            self._urlconf_module = import_module(self.urlconf_name)
        return self._urlconf_module
    urlconf_module = property(_get_urlconf_module)

    def __getattr__(self, name):
        return getattr(self.urlconf_module, name)


def decorator_include(decorators, arg, namespace=None, app_name=None):
    """
    Works like ``django.conf.urls.include`` but takes a view decorator
    or an iterable of view decorators as the first argument and applies them,
    in reverse order, to all views in the included urlconf.
    """
    if isinstance(arg, tuple):
        if namespace:
            raise ImproperlyConfigured(
                'Cannot override the namespace for a dynamic module that provides a namespace'
            )
        urlconf, app_name, namespace = arg
    else:
        urlconf = arg
    decorated_urlconf = DecoratedPatterns(urlconf, decorators)
    return (decorated_urlconf, app_name, namespace)
