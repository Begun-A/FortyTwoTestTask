from django.test import TestCase
from django.core import management
from django.utils.six import StringIO
from django.contrib.contenttypes.models import ContentType


class CommandsTestCase(TestCase):

    @classmethod
    def setUp(cls):
        cls.custom_cmd = 'modelscount'

    def test_modelscount_command(self):
        """Test ./manage.py modelscount command
        and check if it written in dat file.
        """
        c_stdout = StringIO()
        c_stderr = StringIO()
        management.call_command(
            self.custom_cmd,
            stderr=c_stderr,
            stdout=c_stdout
        )
        for ct in ContentType.objects.all():
            m = ct.model_class()
            msg = "Model: %(module)s.%(model)s, count: %(count)s" % dict(
                module=m.__module__,
                model=m.__name__,
                count=m.objects.count()
            )
            err_msg = "error: " + msg
            self.assertIn(msg, c_stdout.getvalue())
            self.assertIn(err_msg, c_stderr.getvalue())
