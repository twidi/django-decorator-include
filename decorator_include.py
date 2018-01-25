"""
A replacement for ``django.conf.urls.include`` that takes a decorator,
or an iterable of view decorators as the first argument and applies them, in
reverse order, to all views in the included urlconf.
"""

from importlib import import_module
from os import path

import pkg_resources
from setuptools.config import read_configuration

from django.core.exceptions import ImproperlyConfigured
from django.urls import URLPattern, URLResolver
from django.utils.functional import cached_property


def _extract_version(package_name):
    try:
        # if package is installed
        version = pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        # if not installed, so we must be in source, with ``setup.cfg`` available
        _conf = read_configuration(path.join(
            path.dirname(__file__), 'setup.cfg')
        )
        version = _conf['metadata']['version']

    return tuple(int(part) for part in version.split('.') if part.isnumeric())


VERSION = _extract_version('django_decorator_include')


class DecoratedPatterns(object):
    """
    A wrapper for an urlconf that applies a decorator to all its views.
    """
    def __init__(self, urlconf_module, decorators):
        # ``urlconf_module`` may be:
        #   - an object with an ``urlpatterns`` attribute
        #   - an ``urlpatterns`` itself
        #   - the dotted Python path to a module with an ``urlpatters`` attribute
        self.urlconf = urlconf_module
        try:
            iter(decorators)
        except TypeError:
            decorators = [decorators]
        self.decorators = decorators

    def decorate_pattern(self, pattern):
        if isinstance(pattern, URLResolver):
            decorated = URLResolver(
                pattern.pattern,
                DecoratedPatterns(pattern.urlconf_module, self.decorators),
                pattern.default_kwargs,
                pattern.app_name,
                pattern.namespace,
            )
        else:
            callback = pattern.callback
            for decorator in reversed(self.decorators):
                callback = decorator(callback)
            decorated = URLPattern(
                pattern.pattern,
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
        if isinstance(self.urlconf, str):
            return import_module(self.urlconf)
        else:
            return self.urlconf


def decorator_include(decorators, arg, namespace=None):
    """
    Works like ``django.conf.urls.include`` but takes a view decorator
    or an iterable of view decorators as the first argument and applies them,
    in reverse order, to all views in the included urlconf.
    """
    app_name = None
    if isinstance(arg, tuple):
        # callable returning a namespace hint
        try:
            urlconf, app_name = arg
        except ValueError:
            if namespace:
                raise ImproperlyConfigured(
                    'Cannot override the namespace for a dynamic module that provides a namespace'
                )
            # can happen for example when using decorator_include with ``admin.site.urls``
            urlconf, app_name, namespace = arg
    else:
        # No namespace hint - use manually provided namespace
        urlconf = arg

    decorated_urlconf = DecoratedPatterns(urlconf, decorators)
    namespace = namespace or app_name
    return (decorated_urlconf, app_name, namespace)
