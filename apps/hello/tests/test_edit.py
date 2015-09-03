from __future__ import division

import os
import json
import random
import string

from PIL import Image
from StringIO import StringIO

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, AnonymousUser

from hello.views import EditView
from hello.models import Contact


class EditFormTest(TestCase):
    """Check for form recieve, when open session with user.
    """
    fixtures = ['initial_data.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.fake_path = reverse('edit', kwargs={"pk": 1})
        self.user = User.objects.last()
        self.client.login(
            username="admin@admin.com",
            password="admin"
        )

    def test_if_form_is_present_on_page(self):
        """Must be rendered the form.
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
        for form_id in ids:
            self.assertIn(form_id, response.render().content)
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
        content = json.loads(response.content).values()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('content-type'), 'application/json')
        new_res = self.test_if_form_is_present_on_page()
        for el in content:
            self.assertIn(str(el), new_res.content)

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
        content = json.loads(response.content).values()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get('content-type'), 'application/json')
        for el in content:
            self.assertIn(el[0], errors)

    def test_anonim_cant_edit_page(self):
        """Check if anonim can't edit page while not authenticated.
        It must go to /login/.
        """
        request = self.factory.post(
            path=self.fake_path,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data={}
        )
        request.user = AnonymousUser()
        response = EditView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = "%s?next=%s" % (reverse('login'), self.fake_path)
        self.assertEqual(redirect_url, response.url)

    @staticmethod
    def generate_new_filename(ext):
        """Generate new file name with ascii + digits and
        add it to the file extension.
        """
        name = ''.join(
            random.choice(string.ascii_lowercase + string.digits)
            for x in xrange(16)
        )
        return '.'.join([name, ext])

    @staticmethod
    def create_test_image(name, color, size, ext):
        # solid red
        file = StringIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file, ext)
        file.name = name
        file.seek(0)
        return file

    def make_resize_of_photo(self, photo_size):
        ext = 'png'
        photo_color = (255, 0, 0)
        init_ratio = photo_size[0] / float(photo_size[1])

        photo_name = self.generate_new_filename(ext)
        photo = EditFormTest.create_test_image(
            name=photo_name,
            color=photo_color,
            size=photo_size,
            ext='png'
        )
        response = self.client.get(path=self.fake_path)
        data = response.context_data['form'].initial
        data['photo'] = photo
        photo_upload = self.client.post(
            path=self.fake_path,
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(photo_upload.status_code, 200)

        # now check photo in db
        contact = Contact.objects.last()
        self.assertIsNotNone(contact.photo)
        self.assertEqual(
            os.path.basename(contact.photo.name),
            photo_name
        )
        # have error deviation in save model method (~0.01) so need to perform
        # round of each.
        img_ratio = contact.photo.width / float(contact.photo.height)
        img_size = (contact.photo.width, contact.photo.height)
        self.assertTrue(0.99 < init_ratio / float(img_ratio) < 1.01)
        self.assertEqual(min(img_size[0], img_size[1]), 200)

    def test_resize_photo_with_ascpect_ration_less_1(self):
        """Check if aspect reatio < 1 and photo will be resized.
        """
        size = (123, 5823)
        self.make_resize_of_photo(size)

    def test_resize_photo_with_ascpect_ration_greater_1(self):
        """Check if aspect reatio > 1 and photo will be resized.
        """
        size = (1237, 784)
        self.make_resize_of_photo(size)

    def test_resize_photo_with_ascpect_ration_equal_1(self):
        """Check if aspect reatio == 1 and photo will be resized.
        """
        size = (761, 761)
        self.make_resize_of_photo(size)
