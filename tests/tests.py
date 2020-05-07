from django.contrib import admin
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.test import TestCase
from django.urls import path


def test_decorator(func):
    func.tested = True
    return func


class IncludeDecoratedTestCase(TestCase):
    def get_decorator_include(self):
        from decorator_include import decorator_include
        return decorator_include

    def test_basic(self):
        decorator_include = self.get_decorator_include()

        urlconf, app_name, namespace = decorator_include(test_decorator, 'tests.urls')
        self.assertEqual(urlconf.__class__.__name__, 'DecoratedPatterns')
        # use app_name defined in tests.urls
        self.assertEqual(app_name, 'app_name_tests')
        # if not defined, the namespace is the app_name
        self.assertEqual(namespace, 'app_name_tests')

    def test_basic_namespace(self):
        decorator_include = self.get_decorator_include()

        urlconf, app_name, namespace = decorator_include(test_decorator, 'tests.urls', 'test')
        self.assertEqual(urlconf.__class__.__name__, 'DecoratedPatterns')
        # use app_name defined in tests.urls
        self.assertEqual(app_name, 'app_name_tests')
        # use passed namespace
        self.assertEqual(namespace, 'test')

    def test_basic_2_tuple(self):
        decorator_include = self.get_decorator_include()

        urlconf, app_name, namespace = decorator_include(test_decorator, ('tests.urls', 'testapp'))
        self.assertEqual(urlconf.__class__.__name__, 'DecoratedPatterns')
        # use app_name defined in tests.urls even if passed in the tuple
        self.assertEqual(app_name, 'app_name_tests')
        # if not defined, the namespace is the app_name
        self.assertEqual(namespace, 'app_name_tests')

        # temporarily remove app_name from `tests.urls` to ensure it will use the provided one
        from tests import urls
        old_app_name = urls.app_name
        try:
            del urls.app_name
            urlconf, app_name, namespace = decorator_include(test_decorator, ('tests.urls', 'testapp'))
            self.assertEqual(urlconf.__class__.__name__, 'DecoratedPatterns')
            # no app_name in tests.urls, we use the one passed in the tuple
            self.assertEqual(app_name, 'testapp')
            # if not defined, the namespace is the app_name
            self.assertEqual(namespace, 'testapp')
        finally:
            urls.app_name = old_app_name

    def test_basic_2_tuple_namespace(self):
        decorator_include = self.get_decorator_include()

        urlconf, app_name, namespace = decorator_include(test_decorator, ('tests.urls', 'testapp'), 'testns')
        self.assertEqual(urlconf.__class__.__name__, 'DecoratedPatterns')
        # use app_name defined in tests.urls even if passed in the tuple
        self.assertEqual(app_name, 'app_name_tests')
        # use passed namespace
        self.assertEqual(namespace, 'testns')

        # temporarily remove app_name from `tests.urls` to ensure it will use the provided one
        from tests import urls
        old_app_name = urls.app_name
        try:
            del urls.app_name
            urlconf, app_name, namespace = decorator_include(test_decorator, ('tests.urls', 'testapp'), 'testns')
            self.assertEqual(urlconf.__class__.__name__, 'DecoratedPatterns')
            # no app_name in tests.urls, we use the one passed in the tuple
            self.assertEqual(app_name, 'testapp')
            # use passed namespace
            self.assertEqual(namespace, 'testns')
        finally:
            urls.app_name = old_app_name

    def test_basic_3_tuple(self):
        decorator_include = self.get_decorator_include()

        # passing a 3 tuple with a python path for the urls module is not allowed
        with self.assertRaises(ImproperlyConfigured):
            decorator_include(test_decorator, ('tests.urls', 'testapp', 'testns'))

        # but it is allowed when the first item can return directly urls, like the admin urls
        urlconf, app_name, namespace = decorator_include(test_decorator, admin.site.urls)
        self.assertEqual(urlconf.__class__.__name__, 'DecoratedPatterns')
        self.assertEqual(app_name, 'admin')
        self.assertEqual(namespace, 'admin')

        # or directly a list
        urlpatterns = [
            path('myview/', lambda request: HttpResponse('view'), name='myview'),
        ]
        urlconf, app_name, namespace = decorator_include(test_decorator, (urlpatterns, 'myviewsapp', 'myviewsns'))
        self.assertEqual(urlconf.__class__.__name__, 'DecoratedPatterns')
        self.assertEqual(app_name, 'myviewsapp')
        self.assertEqual(namespace, 'myviewsns')

    def test_get_urlpatterns(self):
        decorator_include = self.get_decorator_include()

        def test_decorator(func):
            func.decorator_flag = 'test'
            return func

        urlconf, app_name, namespace = decorator_include(test_decorator, 'tests.urls')
        self.assertEqual(urlconf.__class__.__name__, 'DecoratedPatterns')
        patterns = urlconf.urlpatterns
        # 3 URL patterns
        #   /
        #   /include/
        #   /admin/
        #   /only-god/
        #   /with-perm/
        self.assertEqual(len(patterns), 5)
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

        urlconf, app_name, namespace = decorator_include((first_decorator, second_decorator), 'tests.urls')
        self.assertEqual(urlconf.__class__.__name__, 'DecoratedPatterns')
        patterns = urlconf.urlpatterns
        pattern = patterns[0]
        self.assertEqual(pattern.callback.decorator_flag, 'first')
        self.assertEqual(pattern.callback.decorated_by, 'second')

    def test_follow_include(self):
        decorator_include = self.get_decorator_include()

        def test_decorator(func):
            func.decorator_flag = 'test'
            return func

        urlconf, app_name, namespace = decorator_include(test_decorator, 'tests.urls')
        patterns = urlconf.urlpatterns
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

    def test_multiple_decorators_real_case(self):
        # the `/only-god/` path is decorated with two decorators:
        # - `login_required` that will redirect to login page if not authenticated
        # - `only_god` that will raise a 403 if it's not the "god" user

        # not authenticated will redirect to login page
        response = self.client.get('/only-god/test/')
        self.assertEqual(response.status_code, 302)

        # authenticated as god is ok
        god = User(username='god')
        god.set_password('foo')
        god.save()
        self.client.login(username='god', password='foo')
        response = self.client.get('/only-god/test/')
        self.assertEqual(response.status_code, 200)

        # authenticated as another user will raise
        notgod = User(username='notgod')
        notgod.set_password('foo')
        notgod.save()
        self.client.login(username='notgod', password='foo')
        response = self.client.get('/only-god/test/')
        self.assertEqual(response.status_code, 403)

    def test_django_permission_required(self):
        permission = Permission.objects.create(
            codename='is_god',
            name='Can do god things',
            content_type=ContentType.objects.get_for_model(User),
        )

        # not authenticated will redirect to login page
        response = self.client.get('/with-perm/test/')
        self.assertEqual(response.status_code, 302)

        # authenticated with permission
        allowed_user = User(username='allowed')
        allowed_user.set_password('foo')
        allowed_user.save()
        allowed_user.user_permissions.add(permission)
        self.client.login(username='allowed', password='foo')
        response = self.client.get('/with-perm/test/')
        self.assertEqual(response.status_code, 200)

        # authenticated without permission will raise
        not_allowed = User(username='not_allowed')
        not_allowed.set_password('foo')
        not_allowed.save()
        self.client.login(username='not_allowed', password='foo')
        response = self.client.get('/with-perm/test/')
        self.assertEqual(response.status_code, 403)
