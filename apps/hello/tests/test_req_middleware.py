from django.test import TestCase
from django.test.client import RequestFactory

from hello.factories import FAKE_PATH_LIST
from hello.middleware import LogWebReqMiddleware
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
