import json

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps import TEST_DATA
from t1_contact.views import ContactView
from t5_forms.tests import LoginUnitTest


class ContactFormTest(TestCase):
    """Check for form recieve, when open session with user.
    """
    fixtures = ['initial_data.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.fake_path = reverse('contact')
        self.user = User.objects.create_user(
            username=TEST_DATA['first_name'],
            email=TEST_DATA['email'],
            password=TEST_DATA['password']
        )

    def test_if_form_is_present_on_contact_page(self):
        """Must be changed the template and new form present.
        """
        request = self.factory.get(path=self.fake_path)
        request.user = self.user
        LoginUnitTest._mock_session_to_request(request)
        response = ContactView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context_data['form'])
        ids = [
            'id="contact-first_name"',
            'id="contact-last_name"',
            'id="contact-birth_date"',
            'id="contact-bio"',
            'id="contact-email"',
            'id="contact-jabber"',
            'id="contact-skype"',
            'id="contact-other"'
        ]
        map(
            lambda form_id: self.assertIn(form_id, response.render().content),
            ids
        )
        return response

    def test_check_put_request_and_get_changed_data_on_page(self):
        """Check put request and for chenging data in db(without image).
        """
        from datetime import date
        data = dict(
            first_name="hello",
            last_name="world",
            birth_date=date.today(),
            bio="wefwefwefwefwefwe",
            email="test@test.ad",
            jabber="test@jabber.com",
            skype="fwfwefwefwe"
        )
        request = self.factory.put(
            path=self.fake_path,
            data=dict(**data),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertTrue(request.is_ajax())
        request.user = self.user
        LoginUnitTest._mock_session_to_request(request)
        response = ContactView.as_view()(request)
        content = [el for el in json.loads(response.content).values()]
        self.assertEqual(response.get('content-type'), 'application/json')
        new_res = self.test_if_form_is_present_on_contact_page()
        map(
            lambda el: self.assertIn(el, new_res.render().content),
            content
        )
