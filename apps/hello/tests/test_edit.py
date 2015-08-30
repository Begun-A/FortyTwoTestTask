import json

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class EditFormTest(TestCase):
    """Check for form recieve, when open session with user.
    """
    fixtures = ['initial_data.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.fake_path = reverse('edit')
        self.user = User.objects.last()
        self.client.login(
            username="admin@admin.com",
            password="admin"
        )

    def test_if_form_is_present_on_contact_page(self):
        """Must be changed the template and new form present.
        """
        response = self.client.get(path=self.fake_path)
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

    def test_check_valid_post_request_and_get_changed_data_on_page(self):
        """Check post request and for change the data in db(without image).
        """
        data = dict(
            first_name="hello",
            last_name="world",
            birth_date='1348-03-23',
            email="test@test.ad",
            jabber="test@jabber.com",
            skype="fwfwefwefwe",
        )
        response = self.client.post(
            path=self.fake_path,
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        content = [el for el in json.loads(response.content).values()]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('content-type'), 'application/json')
        new_res = self.test_if_form_is_present_on_contact_page()
        map(
            lambda el: self.assertIn(el, new_res.content),
            content
        )

    def test_check_invalid_post_request_and_get_form_errors(self):
        """Check post request with invalid data and get errors from form.
        """
        data = dict(
            first_name="",
            last_name="",
            birth_date="",
            email="",
            jabber="",
            skype=""
        )
        response = self.client.post(
            path=self.fake_path,
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        errors = [
            'First name is required.',
            'Surname is required.',
            'Skype is required.',
            'Birthday date is required.',
            'Jabber is required.',
            'Email is required.'
        ]
        content = [el for el in json.loads(response.content).values()]
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get('content-type'), 'application/json')
        map(
            lambda el: self.assertIn(el[0], errors),
            content
        )
