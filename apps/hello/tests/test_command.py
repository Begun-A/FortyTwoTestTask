import datetime
import subprocess
import os
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


class CommandsTestCase(TestCase):

    @classmethod
    def setUp(cls):
        cls.custom_cmd = 'modelscount'
        cls.bash_file = os.path.join(settings.BASE_DIR, 'count_models.sh')
        cls.file_name = datetime.datetime.now().strftime("%Y-%m-%d") + ".dat"
        cls.file_path = os.path.join(settings.BASE_DIR, cls.file_name)

    def test_modelscount_command(self):
        """Test ./manage.py modelscount command
        and check if it written in dat file.
        """

        subprocess.call(["rm", self.file_path])
        subprocess.call(["sh", self.bash_file])
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
