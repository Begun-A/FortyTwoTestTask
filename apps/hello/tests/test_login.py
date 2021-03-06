import json

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

from hello.views import LoginView


class LoginUnitTest(TestCase):
    """Check for form recieve, sending data(of exists user and not exits).
    Check form for validation.
    """

    fixtures = ['initial_data.json']
    ADMIN_USERNAME = "admin@admin.com"
    ADMIN_PASSWORD = "admin"

    def setUp(self):
        self.factory = RequestFactory()
        self.fake_path = reverse('login')
        self.user = User.objects.last()

    def tearDown(self):
        self.user.delete()

    @staticmethod
    def _mock_session_to_request(request):
        """Create session for user.
        """
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

    def test_created_user(self):
        """Check if user in database.
        """
        check_user = User.objects.last()
        self.assertEqual(self.user, check_user)

    def test_login_get_OK_and_recieve_form(self):
        """Check if we render page.
        """
        request = self.factory.get(self.fake_path)
        response = LoginView.as_view()(request)
        content = response.render().content
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context_data['form'])
        self.assertIn('group-username', content)
        self.assertIn('group-password', content)

    def test_login_ajax_post_with_valid_user(self):
        """Submit valid data to the LoginView and get json answer with
        redirect link.
        """
        request = self.factory.post(
            path=self.fake_path,
            data=dict(
                username=self.ADMIN_USERNAME,
                password=self.ADMIN_PASSWORD
            ),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertTrue(request.is_ajax())
        LoginUnitTest._mock_session_to_request(request)
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        success_url = json.loads(response.content)['url']
        self.assertEqual(success_url, reverse('contact'))
        self.assertEqual(response.get('content-type'), 'application/json')

    def test_login_ajax_post_with_invalid_user(self):
        """Submit invalid data to the LoginView and get form errors.
        """
        request = self.factory.post(
            path=self.fake_path,
            data=dict(
                username='avaba',
                password='kedabra'
            ),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertTrue(request.is_ajax())
        LoginUnitTest._mock_session_to_request(request)
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(response.get('location'))
        errors = ['__all__', 'username', 'password']
        self.assertIsNotNone(response.content)
        res_cont = json.loads(response.content)
        try:
            for error in errors:
                self.assertIsNotNone(res_cont[error])
        except KeyError:
            pass

    def test_logout_by_client(self):
        """Close current session with user.
        """
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 301)
