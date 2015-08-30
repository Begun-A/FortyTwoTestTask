from django.test import TestCase

from hello.models import Contact, SignalLog
from hello.factories import FAKE_DATA


class SignalUnitTest(TestCase):
    """Signal test on post, put and delete data. (taken Contact form as mockup)
    """
    fixtures = ['initial_data.json']

    def setUp(self):
        self.model = Contact
        self.model_name = self.model.__name__
        self.model(**FAKE_DATA).save()

    def test_check_signal_after_post_complete(self):
        """Create some information and check it in signal log.
        """
        sl_m = SignalLog.objects.last()
        self.assertEqual(sl_m.action, "POST")
        self.assertEqual(sl_m.model, self.model_name)

    def test_check_signal_after_put_complete(self):
        """Alter some information and check it in signal log.
        """
        c_m = self.model.objects.last()
        c_m.first_name = "Hello"
        c_m.last_name = "World"
        c_m.save()
        sl_m = SignalLog.objects.last()
        self.assertEqual(sl_m.action, "PUT")
        self.assertEqual(sl_m.model, self.model_name)

    def test_check_signal_after_delete_complete(self):
        """Delete some information and check it in signal log.
        """
        c_m = self.model.objects.last()
        c_m.delete()
        sl_m = SignalLog.objects.last()
        self.assertEqual(sl_m.action, "DELETE")
        self.assertEqual(sl_m.model, self.model_name)
