import json

from django.test import TestCase
from django.test.client import RequestFactory
from django.core import serializers
from django.core.urlresolvers import reverse

from hello.models import Contact
from hello.views import ContactView

from hello.factories import FAKE_DATA


class ContactUnitTest(TestCase):

    fixtures = ['initial_data.json']

    def setUp(self):
        self.fake_path = reverse('contact')
        self.factory = RequestFactory()
        self.template = 'contact.html'
        self.model = Contact
        self.pattern = ('hello', 'contact')
        self.client.login(
            username="admin@admin.com",
            password="admin"
        )

    def test_fixture_load_data(self):
        """Test, if fixture load data.
        """
        self.assertEqual(self.model.objects.count(), 1)

    def test_contact_model(self):
        """Test if we recieve data to Contact table.
        """
        email = 'dev1dor@ukr.net'
        contact = self.model.objects.last()
        self.assertEqual(contact.email, email)

    def test_data_deletion_in_db(self):
        """Test if data deleted in db.
        """
        self.model.objects.last().delete()
        self.assertEqual(self.model.objects.count(), 0)

    def test_if_data_on_page(self):
        """Check if data renders on page.
        """
        contact = self.model.objects.last()

        request = self.factory.get(path=self.fake_path)
        response = ContactView.as_view()(request)

        response_content = response.render().content

        db_data = json.loads(
            serializers.serialize('json', [contact, ])
        )[0]['fields']

        self.assertEqual(response.context_data['contact'], contact)
        for value in [el for el in db_data.values()]:
            self.assertIn(value, response_content)

    def test_contact_page_when_2_records_in_db(self):
        """Check if page don't render second record on page.
        """
        model = self.model(**FAKE_DATA)
        model.save()
        self.assertEqual(self.model.objects.count(), 2)
        request = self.factory.get(path=self.fake_path)
        response = ContactView.as_view()(request)
        response_content = response.render().content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name[0],
            self.template
        )
        db_data = Contact.objects.all().values()[1]
        for el in db_data.values()[:-1]:
            if el:
                self.assertNotIn(str(el), response_content)

    def admin_response_delete(self):
        delete_path = reverse('admin:%s_%s_delete' % self.pattern, args=(1,))
        response = self.client.post(
            path=delete_path,
            data={
                u'action': [u'delete_selected'],
                u'_selected_action': [u'1'],
                u'post': [u'yes']
            }
        )
        self.assertEqual(response.status_code, 302)

    def admin_response_add(self):
        add_path = reverse('admin:%s_%s_add' % self.pattern)
        response = self.client.post(path=add_path, data=FAKE_DATA)
        self.assertEqual(response.status_code, 302)

    def admin_response_update(self):
        update_path = reverse('admin:%s_%s_change' % self.pattern, args=(1,))
        data = FAKE_DATA.copy()
        data["first_name"] = "Human"
        response = self.client.post(
            path=update_path,
            data=data
        )
        self.assertEqual(response.status_code, 302)

    def test_admin_delete_of_model_create_new_and_ckeck_it(self):
        """Delete, add and update data from admin,
        add new and check it on the page.
        """
        # delete and check page not found
        self.admin_response_delete()
        self.assertEqual(self.model.objects.count(), 0)
        contact_res = self.client.get(path=self.fake_path)
        self.assertEqual(contact_res.status_code, 404)
        self.assertIn('<h1>Page Not Found</h1>', contact_res.content)

        # add and check it on main page
        self.admin_response_add()
        self.assertEqual(self.model.objects.count(), 1)
        contact_res = self.client.get(path=self.fake_path)
        response_content = contact_res.render().content
        self.assertEqual(contact_res.status_code, 200)
        db_data = Contact.objects.all().values()[0]
        # need to skip id from query so take list to the last element
        for el in db_data.values()[:-1]:
            if el:
                self.assertIn(str(el), response_content)

        # update it and check it on main page
        self.admin_response_update()
        self.assertEqual(self.model.objects.count(), 1)
        contact_res = self.client.get(path=self.fake_path)
        response_content = contact_res.render().content
        self.assertEqual(contact_res.status_code, 200)
        db_updated = Contact.objects.all().values()[0]
        self.assertNotEqual(db_updated, db_data)
        for el in db_data.values()[:-1]:
            if el:
                self.assertIn(str(el), response_content)
