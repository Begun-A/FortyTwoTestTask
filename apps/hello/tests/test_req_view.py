from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from apps import FAKE_PATH_LIST
from hello.models import LogWebRequest
from hello.views import LogRequestView


class LogRequestTest(TestCase):
    """Check status, ajax work.
    """
    fixtures = ['initial_data.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.fake_path = reverse('requests')
        self.requests_html = 'requests.html'

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
