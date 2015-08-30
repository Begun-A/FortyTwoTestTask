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

    def test_if_we_can_add_data_to_db(self):
        """Test if we can add data and check in db.
        """
        self.model(**FAKE_DATA).save()
        self.assertEqual(self.model.objects.count(), 2)
        db_data = json.loads(
            serializers.serialize('json', [self.model.objects.last(), ])
        )[0]['fields']
        self.assertDictEqual(db_data, FAKE_DATA)

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
        map(
            lambda el: self.assertIn(el, response_content),
            [el for el in db_data.values()]
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

    def test_admin_actions_of_this_model(self):
        """Delete, add, and update of data from admin.
        """
        pattern = ('hello', 'contact')
        admin_u = "admin@admin.com"
        admin_p = "admin"
        self.client.login(
            username=admin_u,
            password=admin_p
        )
        delete_path = reverse('admin:%s_%s_delete' % pattern, args=(1,))
        self.client.post(
            path=delete_path,
            data={
                u'action': [u'delete_selected'],
                u'_selected_action': [u'1'],
                u'post': [u'yes']
            }
        )
        self.assertEqual(self.model.objects.count(), 0)

        add_path = reverse('admin:%s_%s_add' % pattern)
        self.client.post(
            path=add_path,
            data=FAKE_DATA
        )
        self.assertEqual(self.model.objects.count(), 1)
        db_data = json.loads(
            serializers.serialize('json', [self.model.objects.last(), ])
        )[0]['fields']
        self.assertDictEqual(db_data, FAKE_DATA)

        update_path = reverse('admin:%s_%s_change' % pattern, args=(1,))
        FAKE_DATA["first_name"] = "Human"
        self.client.post(
            path=update_path,
            data=FAKE_DATA
        )
        self.assertEqual(self.model.objects.count(), 1)
        db_data = json.loads(
            serializers.serialize('json', [self.model.objects.last(), ])
        )[0]['fields']
        self.assertDictEqual(db_data, FAKE_DATA)
