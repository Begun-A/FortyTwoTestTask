import unittest
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from apps import initial_data
from .views import ContactView


class ContactUnitTest(unittest.TestCase):
    """Simple test for status code.
    """

    def setUp(self):
        self.pk = initial_data[0]['pk']
        self.fake_path = reverse('contact', kwargs={'pk': self.pk})
        self.factory = RequestFactory()

    def test_contact_get_ok_request(self):
        request = self.factory.get(path=self.fake_path)
        view = ContactView.as_view()
        response = view(request, pk=self.pk)
        self.assertEqual(response.status_code, 200)
