from StringIO import StringIO
from django.test import TestCase
from django.core import management


class CommandsTestCase(TestCase):

    @classmethod
    def setUp(cls):
        cls.custom_cmd = 'modelscount'

    def test_modelscount_command(self):
        """Test ./manage.py modelscount command
        and check if it written in dat file.
        """
        out = StringIO()
        management.call_command(self.custom_cmd, stdout=out)
        outputs = [
            'Model: hello.models.Contact, count: 1',
            'Model: django.contrib.auth.models.User, count: 1'
        ]
        self.assertIsNotNone(out.getvalue())
        for output in outputs:
            self.assertIn(output, out.getvalue())
