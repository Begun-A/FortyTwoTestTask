from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from apps import initial_data
from .middleware import LogWebReqMiddleware
from .models import LogWebRequest
from .views import (
    ContactView,
    LogRequestView,
)


class ContactUnitTest(TestCase):
    """Simple test for status code. Testing '/contact/1/'
    """

    def setUp(self):
        self.pk = initial_data[0]['pk']
        self.fake_path = reverse('contact', kwargs={'pk': self.pk})
        self.factory = RequestFactory()

    def test_contact_get_ok_request(self):
        """Check if page get status OK.
        """
        request = self.factory.get(path=self.fake_path)
        view = ContactView.as_view()
        response = view(request, pk=self.pk)
        self.assertEqual(response.status_code, 200)


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


class LogWebRequestMiddlewareTest(TestCase):
    """Test middleware response, and ability to save responses.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.pk = initial_data[0]['pk']
        self.lwrm = LogWebReqMiddleware()
        self.lwr_queryset = LogWebRequest.objects.order_by('-id')[:10]

    def get_req_and_res(self):
        fake_path_list = [
            reverse('requests'),
            reverse('contact', kwargs={'pk': self.pk}),
            '/',
            '/el/',
            '/www',
            '1242',
            '/?d=3',
            '/?_=23423523',
            '/avaba-kedabra/',
            '/****/'
        ]
        fake_actions = []
        for fake_path in fake_path_list:
            request = self.factory.get(path=fake_path)
            fake_actions.append(
                dict(
                    request=request,
                    response=LogRequestView.as_view()(request)
                )
            )
        return fake_actions

    def test_response_in_lwm_process_response(self):
        """Test middleware on response answering.
        """
        fake_actions = self.get_req_and_res()
        map(
            lambda income: self.assertEqual(
                self.lwm.process_response(
                    income['request'], income['response']
                ), income['response']
            ), fake_actions
        )

    def test_save_of_10_lwm_requests_in_db(self):
        """Check some values of 10 income requests which must
        coincide with db stored request data.
        """
        fake_actions = self.get_req_and_res()[::-1]
        map(
            lambda income, db: self.assertEqual(
                income['response'].status_code, db.status_code
            ),
            fake_actions,
            self.lwr_queryset
        )
        map(
            lambda income, db: self.assertEqual(
                income['request'].method, db.method
            ),
            fake_actions,
            self.lwr_queryset
        )
        map(
            lambda income, db: self.assertEqual(
                income['request'].path, db.path
            ),
            fake_actions,
            self.lwr_queryset
        )
        map(
            lambda income, db: self.assertEqual(
                income['request'].META['REMOTE_ADDR'], db.remote_addr
            ),
            fake_actions,
            self.lwr_queryset
        )
