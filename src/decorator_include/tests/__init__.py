from __future__ import unicode_literals
from django.test import TestCase


class IncludeDecoratedTests(TestCase):
    urls = 'decorator_include.tests.urls'

    def getDecoratorInclude(self):
        from decorator_include import decorator_include
        return decorator_include

    def testBasic(self):
        decorator_include = self.getDecoratorInclude()

        def test_decorator(func):
            func.tested = True
            return func

        result = decorator_include(
            test_decorator,
            'decorator_include.tests.urls'
        )
        self.assertEquals(3, len(result))
        self.assertTrue('DecoratedPatterns', result[0].__class__.__name__)
        self.assertTrue(result[1] is None)
        self.assertTrue(result[2] is None)

    def testBasicNamespace(self):
        decorator_include = self.getDecoratorInclude()

        def test_decorator(func):
            func.tested = True
            return func

        result = decorator_include(
            test_decorator,
            'decorator_include.tests.urls',
            'test'
        )
        self.assertEquals(3, len(result))
        self.assertTrue('DecoratedPatterns', result[0].__class__.__name__)
        self.assertTrue(result[1] is None)
        self.assertEquals('test', result[2])

    def testGetURLPatterns(self):
        decorator_include = self.getDecoratorInclude()

        def test_decorator(func):
            func.decorator_flag = 'test'
            return func

        result = decorator_include(
            test_decorator,
            'decorator_include.tests.urls'
        )
        self.assertEquals(3, len(result))
        self.assertTrue('DecoratedPatterns', result[0].__class__.__name__)
        patterns = result[0].urlpatterns
        self.assertEquals(2, len(patterns))
        self.assertEquals('test', patterns[0].callback.decorator_flag)

    def testMultipleDecorators(self):
        decorator_include = self.getDecoratorInclude()

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
        self.assertTrue('DecoratedPatterns', result[0].__class__.__name__)
        patterns = result[0].urlpatterns
        pattern = patterns[0]
        self.assertEquals('first', pattern.callback.decorator_flag)
        self.assertEquals('second', pattern.callback.decorated_by)

    def testFollowInclude(self):
        decorator_include = self.getDecoratorInclude()

        def test_decorator(func):
            func.decorator_flag = 'test'
            return func

        result = decorator_include(
            test_decorator,
            'decorator_include.tests.urls'
        )
        patterns = result[0].urlpatterns
        decorated = patterns[1]
        self.assertEquals('test', decorated.url_patterns[1].callback.decorator_flag)
        decorated = patterns[1].url_patterns[0].url_patterns[0]
        self.assertEquals('test', decorated.callback.decorator_flag)

    def testGetIndex(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)

    def testGetTest(self):
        response = self.client.get('/include/test/')
        self.assertEquals(302, response.status_code)

    def testGetDeeplyNested(self):
        response = self.client.get('/include/included/deeply_nested/')
        self.assertEquals(302, response.status_code)
