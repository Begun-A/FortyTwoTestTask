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
        size = (int(round(size[0])), int(round(size[1])))
        image = Image.new("RGBA", size=size, color=color)
        image.save(file, ext)
        file.name = name
        file.seek(0)
        return file

    def test_of_resize_photo(self):
        """Check if th given photo will be resized to 200x200.
        """
        ext = 'png'
        photo_color = (255, 0, 0)
        photo_size = (114.5, 644.3)

        photo_name = EditFormTest.generate_new_filename(ext)
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
        self.assertEqual(
            (contact.photo.width, contact.photo.height),
            (200, 200)
        )
        croped_size = EditFormTest.check_correct_resize_image(
            path=contact.photo.path,
            size=photo_size
        )
        c_width = croped_size[2] - croped_size[0]
        c_height = croped_size[3] - croped_size[1]
        self.assertEqual((c_width, c_height), photo_size)

    @staticmethod
    def check_correct_resize_image(path, size):
        filename = str(path)
        image = Image.open(filename)

        current_w = image.width
        current_h = image.height
        needed_w = size[0]
        needed_h = size[1]

        current_r = float(current_w) / float(current_h)
        needed_r = float(needed_w) / float(needed_h)
        if current_r > needed_r:
            # photo aspect is wider than destination ratio
            tw = int(round(needed_h * current_r))
            l = int(round((tw - needed_w) / 2.0))
            size = (l, 0, l + needed_w, needed_h)

        elif current_r < needed_r:
            # photo aspect is taller than destination ratio
            th = int(round(needed_w / current_r))
            t = int(round((th - needed_h) / 2.0))
            size = (0, t, needed_w, t + needed_h)

        return size
