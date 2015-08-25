import json

from django.test import TestCase
from django.test.client import RequestFactory
from django.core import serializers
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

from apps import FAKE_PATH_LIST, TEST_DATA
from .middleware import LogWebReqMiddleware
from .models import Contact, LogWebRequest
from .views import (
    ContactView,
    LogRequestView,
    LoginView
)


class ContactUnitTest(TestCase):
    """Simple test for status code. Testing '/contact/1/'
    """

    def setUp(self):
        self.fake_path = reverse('contact')
        self.factory = RequestFactory()
        self.contact = Contact.objects.get(email=TEST_DATA['email'])
        self.template = 'hello/contact.html'

    def test_contact_model(self):
        """Test if we recieve data to Contact table.
        """
        self.assertEqual(self.contact.email, TEST_DATA['email'])

    def test_if_data_on_page(self):
        """Check if data renders on page.
        """
        request = self.factory.get(path=self.fake_path)
        response = ContactView.as_view()(request)
        self.assertEqual(response.context_data['contact'], self.contact)

        response_content = response.render().content

        db_data = json.loads(
            serializers.serialize('json', [self.contact, ])
        )[0]['fields']
        map(
            lambda contact: self.assertIn(contact, response_content),
            [contact for contact in db_data.values()]
        )

    def test_contact_get_ok_request(self):
        """Check if page get status OK and response template.
        """
        request = self.factory.get(path=self.fake_path)
        response = ContactView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name[0],
            self.template
        )


class LogRequestTest(TestCase):
    """Check status, ajax work.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.fake_path = reverse('requests')
        self.requests_html = 'hello/requests.html'

    def test_requests_get_ok_request_and_check_template(self):
        """Test rendering of page and view template.
        """
        request = self.factory.get(path=self.fake_path)
        view = LogRequestView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertHTMLEqual(response.template_name[0], self.requests_html)

    def test_by_client_get_10_records_from_db(self):
        """See results of 10 requests in the page.
        """
        (lambda: [self.client.get(path) for path in FAKE_PATH_LIST])()
        response = self.client.get(
            self.fake_path,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        queryset = LogWebRequest.objects.order_by('-id')[:10]
        self.assertEqual(response.status_code, 200)
        map(lambda db: self.assertIn(str(db.path), response.content), queryset)


class LogWebRequestMiddlewareTest(TestCase):
    """Test middleware response, and ability to save responses.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.lwrm = LogWebReqMiddleware()

    def get_req_and_res(self):
        fake_actions = []
        for fake_path in FAKE_PATH_LIST:
            request = self.factory.get(path=fake_path)
            fake_actions.append(
                dict(
                    request=request,
                    response=LogRequestView.as_view()(request)
                )
            )
        return fake_actions

    def test_response_in_lwrm_process_response(self):
        """Test middleware on response answering.
        """
        fake_actions = self.get_req_and_res()
        map(
            lambda income: self.assertEqual(
                self.lwrm.process_response(
                    income['request'], income['response']
                ), income['response']
            ), fake_actions
        )

    def test_save_of_10_lwm_requests_in_db(self):
        """Check some values of 10 income requests which must
        coincide with db stored request data.
        """
        # need for store data
        self.test_response_in_lwrm_process_response()
        # save income req and res
        fake_actions = self.get_req_and_res()[::-1]
        # get saved income req and res
        lwr_queryset = LogWebRequest.objects.order_by('-id')[:10]

        map(
            lambda income, db: self.assertEqual(
                income['response'].status_code, db.status_code
            ),
            fake_actions,
            lwr_queryset
        )
        map(
            lambda income, db: self.assertEqual(
                income['request'].method, db.method
            ),
            fake_actions,
            lwr_queryset
        )
        map(
            lambda income, db: self.assertEqual(
                income['request'].path, db.path
            ),
            fake_actions,
            lwr_queryset
        )
        map(
            lambda income, db: self.assertEqual(
                income['request'].META['REMOTE_ADDR'], db.remote_addr
            ),
            fake_actions,
            lwr_queryset
        )


class LoginUnitTest(TestCase):
    """Check for form recieve, sending data(of exists user and not exits).
    Check form for validation.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.fake_path = reverse('login')
        self.user = User.objects.create_user(
            username=TEST_DATA['first_name'],
            email=TEST_DATA['email'],
            password=TEST_DATA['password']
        )

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
        check_user = User.objects.get(email=TEST_DATA['email'])
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
                username=TEST_DATA['first_name'],
                password=TEST_DATA['password']
            ),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertTrue(request.is_ajax())
        LoginUnitTest._mock_session_to_request(request)
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)['url'], reverse('contact')
        )
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
            map(lambda error: self.assertIsNotNone(res_cont[error]), errors)
        except KeyError:
            pass
