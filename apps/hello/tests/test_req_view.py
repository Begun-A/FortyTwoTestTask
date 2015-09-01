import json
from django.core import serializers
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

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
        self.model = LogWebRequest

    def test_requests_get_ok_request_and_check_template(self):
        """Test rendering of page and view template.
        """
        request = self.factory.get(path=self.fake_path)
        view = LogRequestView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertHTMLEqual(response.template_name[0], self.requests_html)

    @staticmethod
    def _serialize_queryset(query_json):
        query_dict = json.loads(query_json)
        fields_json = []
        for q in query_dict:
            import dateutil.parser
            datestring = q['fields']['time']
            formatted_date = dateutil.parser.parse(datestring)
            fields = q.pop("fields")
            fields['pk'] = q['pk']
            fields['time'] = formatted_date.strftime('%Y-%m-%dT%H:%M:%S')
            fields_json.append(fields)
        return fields_json

    def test_ajax_10_response_on_request_page(self):
        """Check if json is ansvered.
        """
        for x in xrange(10):
            LogWebRequest(
                method='GET',
                status_code=200,
                remote_addr='127.0.0.1'
            ).save()

        self.assertEqual(self.model.objects.count(), 10)
        # get json info about it
        response = self.client.get(
            path=self.fake_path,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.get('content-type'), 'application/json')
        response_f_cont = LogRequestTest._serialize_queryset(response.content)

        # check it with db
        queryset = self.model.objects.order_by('-id')[:10]
        self.assertEqual(self.model.objects.count(), 10)
        query_json = serializers.serialize('json', queryset)
        db_content = LogRequestTest._serialize_queryset(query_json)
        for x in xrange(10):
            self.assertDictEqual(db_content[x], response_f_cont[x])

    def test_10_queries_with_filter(self):
        """Send fake filter key and get it content on the page.
        """
        for x in xrange(10):
            LogWebRequest(
                method='GET',
                status_code=200,
                remote_addr='127.0.0.1',
                priority=1
            ).save()

        self.assertEqual(self.model.objects.count(), 10)
        response = self.client.get(
            path=self.fake_path,
            data=dict(priority=1),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.get('content-type'), 'application/json')
        response_f_cont = LogRequestTest._serialize_queryset(response.content)

        # check it with db
        queryset = self.model.objects.order_by('-id')[:10]
        self.assertEqual(self.model.objects.count(), 10)
        query_json = serializers.serialize('json', queryset)
        db_content = LogRequestTest._serialize_queryset(query_json)
        for x in xrange(10):
            self.assertDictEqual(db_content[x], response_f_cont[x])
