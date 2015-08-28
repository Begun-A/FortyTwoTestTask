from django.test import TestCase
from django.test.client import RequestFactory

from apps import FAKE_PATH_LIST
from hello.middleware import LogWebReqMiddleware
from hello.models import LogWebRequest
from hello.views import LogRequestView


class LogWebRequestMiddlewareTest(TestCase):
    """Test middleware response, and ability to save responses.
    """

    fixtures = ['initial_data.json']

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
