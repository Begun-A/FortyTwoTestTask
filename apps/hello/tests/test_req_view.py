import json
from django.core import serializers
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from hello.models import LogWebRequest
from hello.views import LogRequestView
from hello.factories import FAKE_PATH_LIST, LogWebRequestFactory


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

    def test_by_client_get_10_records_from_db(self):
        """See results of 10 requests in the page.
        """
        for path in FAKE_PATH_LIST:
            self.client.get(path=path)

        # check if it 10 in db
        self.assertEqual(self.model.objects.count(), 10)
        queryset = self.model.objects.order_by('-id')[:10]

        # serializedata from db
        query_json = serializers.serialize('json', queryset)
        db_fields = LogRequestTest._serialize_queryset(query_json)

        # we make request on /requests/ page so one request added
        response = self.client.get(path=self.fake_path)
        # 11 dont be rendered because the page will be refreshed only when ajax
        self.assertEqual(self.model.objects.count(), 11)

        self.assertNotIn(str(11), response.content)
        for db_field in db_fields:
            for val in db_field.values():
                self.assertIn(str(val), response.content)

    def test_ajax_10_response_on_request_page(self):
        """Check if json is ansvered.
        """
        for x in xrange(10):
            LogWebRequestFactory()

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
            LogWebRequestFactory(priority=1)

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
