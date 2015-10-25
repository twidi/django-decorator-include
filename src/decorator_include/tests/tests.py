from __future__ import unicode_literals
from django.test import TestCase


class IncludeDecoratedTestCase(TestCase):
    urls = 'decorator_include.tests.urls'

    def get_decorator_include(self):
        from decorator_include import decorator_include
        return decorator_include

    def test_basic(self):
        decorator_include = self.get_decorator_include()

        def test_decorator(func):
            func.tested = True
            return func

        result = decorator_include(
            test_decorator,
            'decorator_include.tests.urls'
        )
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].__class__.__name__, 'DecoratedPatterns')
        self.assertIsNone(result[1])
        self.assertIsNone(result[2])

    def test_basic_namespace(self):
        decorator_include = self.get_decorator_include()

        def test_decorator(func):
            func.tested = True
            return func

        result = decorator_include(
            test_decorator,
            'decorator_include.tests.urls',
            'test'
        )
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].__class__.__name__, 'DecoratedPatterns')
        self.assertIsNone(result[1])
        self.assertEqual(result[2], 'test')

    def test_get_urlpatterns(self):
        decorator_include = self.get_decorator_include()

        def test_decorator(func):
            func.decorator_flag = 'test'
            return func

        result = decorator_include(
            test_decorator,
            'decorator_include.tests.urls'
        )
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].__class__.__name__, 'DecoratedPatterns')
        patterns = result[0].urlpatterns
        self.assertEqual(len(patterns), 2)
        self.assertEqual(patterns[0].callback.decorator_flag, 'test')

    def test_multiple_decorators(self):
        decorator_include = self.get_decorator_include()

        def first_decorator(func):
            func.decorator_flag = 'first'
            return func

        def second_decorator(func):
            func.decorator_flag = 'second'
            func.decorated_by = 'second'
            return func

        result = decorator_include(
            (first_decorator, second_decorator),
            'decorator_include.tests.urls'
        )
        self.assertEqual(result[0].__class__.__name__, 'DecoratedPatterns')
        patterns = result[0].urlpatterns
        pattern = patterns[0]
        self.assertEqual(pattern.callback.decorator_flag, 'first')
        self.assertEqual(pattern.callback.decorated_by, 'second')

    def test_follow_include(self):
        decorator_include = self.get_decorator_include()

        def test_decorator(func):
            func.decorator_flag = 'test'
            return func

        result = decorator_include(
            test_decorator,
            'decorator_include.tests.urls'
        )
        patterns = result[0].urlpatterns
        decorated = patterns[1]
        self.assertEqual(decorated.url_patterns[1].callback.decorator_flag, 'test')
        decorated = patterns[1].url_patterns[0].url_patterns[0]
        self.assertEqual(decorated.callback.decorator_flag, 'test')

    def test_get_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_test(self):
        response = self.client.get('/include/test/')
        self.assertEqual(response.status_code, 302)

    def test_get_deeply_nested(self):
        response = self.client.get('/include/included/deeply_nested/')
        self.assertEqual(response.status_code, 302)
