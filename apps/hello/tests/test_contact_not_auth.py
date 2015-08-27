import json

from django.test import TestCase
from django.test.client import RequestFactory
from django.core import serializers
from django.core.urlresolvers import reverse

from apps import TEST_DATA
from hello.models import Contact
from hello.views import ContactView


class ContactUnitTest(TestCase):
    """Simple test for status code. Testing '/contact/1/'
    """
    fixtures = ['initial_data.json']

    def setUp(self):
        self.fake_path = reverse('contact')
        self.factory = RequestFactory()
        self.contact = Contact.objects.get(email=TEST_DATA['email'])
        self.template = 'contact.html'

    def test_contact_model(self):
        """Test if we recieve data to Contact table.
        """
        self.assertEqual(self.contact.email, TEST_DATA['email'])

    def test_if_data_on_page(self):
        """Check if data renders on page.
        """
        request = self.factory.get(path=self.fake_path)
        response = ContactView.as_view()(request)
        self.assertEqual(response.context_data['contact'], self.contact)

        response_content = response.render().content

        db_data = json.loads(
            serializers.serialize('json', [self.contact, ])
        )[0]['fields']
        map(
            lambda contact: self.assertIn(contact, response_content),
            [contact for contact in db_data.values()]
        )

    def test_contact_get_ok_request(self):
        """Check if page get status OK and response template.
        """
        request = self.factory.get(path=self.fake_path)
        response = ContactView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name[0],
            self.template
        )
