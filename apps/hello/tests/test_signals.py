from django.test import TestCase
from hello.models import Contact, SignalLog

from apps import TEST_DATA

class SignalUnitTest(TestCase):
    """Signal test on post, put and delete data. (taken Contact form as mockup)
    """
    fixtures = ['initial_data.json']

    def setUp(self):
        self.model = Contact
        self.data = TEST_DATA.copy()
        self.data.pop("password", None)

    def test_check_signal_after_post_complete(self):
        """Create some information and check it in signal log.
        """
        c_m = Contact.objects.create(**self.data)
        sl_m = SignalLog.objects.get(pk=self.data['pk'])
        self.assertEqual(sl_m.action, "POST")
        self.assertEqual(sl_m.model, c_m.__name__)

    def test_check_signal_after_put_complete(self):
        """Alter some information and check it in signal log.
        """
        c_m = Contact.objects.get(pk=self.data['pk'])
        c_m.first_name = "Hello"
        c_m.last_name = "World"
        c_m.save()
        sl_m = SignalLog.objects.get(pk=self.data['pk'])
        self.assertEqual(sl_m.action, "PUT")
        self.assertEqual(sl_m.model, c_m.__name__)

    def test_check_signal_after_delete_complete(self):
        """Delete some information and check it in signal log.
        """
        c_m = Contact.objects.get(pk=self.data['pk'])
        c_m.delete()
        sl_m = SignalLog.objects.get(pk=self.data['pk'])
        self.assertEqual(sl_m.action, "DELETE")
        self.assertEqual(sl_m.model, c_m.__name__)
