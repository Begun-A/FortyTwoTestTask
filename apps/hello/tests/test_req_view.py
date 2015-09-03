import json
import random
from django.core import serializers
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from hello.models import LogWebRequest
from hello.views import LogRequestView
from hello.factories import (
    FAKE_ADDRS,
    FAKE_METHODS,
    FAKE_STATUSES,
    FAKE_PATH_LIST
)


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

    def check_ajax_responses_on_request_page(
        self, m_count, prio=None, req_count=10
    ):
        for x in xrange(m_count):
            LogWebRequest(
                method=random.choice(FAKE_METHODS),
                status_code=random.choice(FAKE_STATUSES),
                remote_addr=random.choice(FAKE_ADDRS),
                path=random.choice(FAKE_PATH_LIST),
                priority=random.randrange(0, 100) if not prio else prio
            ).save()

        if prio:
            data = dict(priority=prio, count=req_count)
        else:
            data = dict(count=req_count)
        # get json info about it
        response = self.client.get(
            path=self.fake_path,
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.get('content-type'), 'application/json')
        response_f_cont = LogRequestTest._serialize_queryset(response.content)
        self.assertLessEqual(len(response_f_cont), req_count)

        # check it with db
        queryset = self.model.objects.order_by('-id')
        if prio:
            queryset = queryset.filter(priority=prio)

        query_json = serializers.serialize('json', queryset)
        db_content = LogRequestTest._serialize_queryset(query_json)
        for x in xrange(m_count):
            if x < req_count:
                self.assertIn(db_content[x], response_f_cont)
            else:
                self.assertNotIn(db_content[x], response_f_cont)

    def test_answer_of_10_req_on_page(self):
        """Check json if it ansvered.
        1) Test with default count, all priority;
        2) Test with random count, random priority;
        """
        # take models count for generation = 147
        m_count = 147
        # 1
        self.check_ajax_responses_on_request_page(m_count=m_count)
        # 2
        self.check_ajax_responses_on_request_page(
            m_count=m_count,
            prio=random.randrange(0, 100),
            req_count=random.randrange(0, m_count)
        )
