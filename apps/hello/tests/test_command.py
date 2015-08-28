import datetime
import os
from django.core.management import call_command
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


class CommandsTestCase(TestCase):

    @classmethod
    def setUp(cls):
        cls.custom_cmd = 'modelscount'
        cls.file_name = datetime.datetime.now().strftime("%Y-%m-%d") + ".dat"
        cls.file_path = os.path.join(settings.BASE_DIR, cls.file_name)

    def test_modelscount_command(self):
        """Test ./manage.py modelscount command and get it response.
        """

        args = []
        opts = {}
        call_command(self.custom_cmd, *args, **opts)
        self.assertTrue(self.file_path)
        with open(self.file_path) as f:
            readed = f.read()

        for ct in ContentType.objects.all():
            m = ct.model_class()
            self.assertIn('error', readed)
            self.assertIn(
                "%s.%s" % (m.__module__, m.__name__),
                readed
            )
