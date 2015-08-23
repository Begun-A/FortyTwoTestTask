import os
import unittest
import json
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from selenium import webdriver
from .views import ContactView


with open(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'fixtures/initial_data.json'
    )
) as test_data:
    data = json.load(test_data)


TEST_DATA = data[0]['fields']

XPATHS = dict(
    first_name='//div[@id="first_name"]',
    last_name='//div[@id="last_name"]',
    birth_date='//div[@id="birth_date"]',
    bio='//div[@id="bio"]',
    contacts='//div[@id="contacts"]',
    email='//div[@id="email"]',
    jabber='//div[@id="jabber"]',
    skype='//div[@id="skype"]',
    other='//div[@id="other"]'
)


class BaseConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.pk = data[0]['pk']
        self.fake_path = reverse('contact', kwargs={'pk': self.pk})


class ContactUnitTest(BaseConfigTestCase):

    def setUp(self):
        super(ContactUnitTest, self).setUp()
        self.factory = RequestFactory()

    def test_contact_get_ok_request(self):
        request = self.factory.get(path=self.fake_path)
        view = ContactView.as_view()
        response = view(request, pk=self.pk)
        self.assertEqual(response.status_code, 200)


class ContactIntegrationTest(BaseConfigTestCase):

    def setUp(self):
        super(ContactIntegrationTest, self).setUp()
        self.absolute_url = 'http://localhost:8000' + self.fake_path
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def test_contact_find_data_on_page_and_check_it_with_base(self):
        driver = self.driver
        driver.get(self.absolute_url)
        driver.implicitly_wait(10)

        self.assertEqual(
            driver.title,
            unicode(
                ' '.join([TEST_DATA['first_name'], TEST_DATA['last_name']])
            )
        )

        first_name = driver.find_element_by_xpath(XPATHS['first_name']).text
        self.assertEqual(first_name, TEST_DATA['first_name'])

        last_name = driver.find_element_by_xpath(XPATHS['last_name']).text
        self.assertEqual(last_name, TEST_DATA['last_name'])

        from datetime import datetime
        birth_date = driver.find_element_by_xpath(XPATHS['birth_date']).text
        conv_date = datetime.strptime(birth_date, '%B %d, %Y') \
            .strftime('%Y-%m-%d')
        self.assertEqual(conv_date, TEST_DATA['birth_date'])

        bio = driver.find_element_by_xpath(XPATHS['bio']).text
        self.assertEqual(bio, TEST_DATA['bio'])

        contacts = driver.find_element_by_xpath(XPATHS['contacts']).text
        self.assertEqual(contacts, TEST_DATA['contacts'])

        email = driver.find_element_by_xpath(XPATHS['email']).text
        self.assertEqual(email, TEST_DATA['email'])

        jabber = driver.find_element_by_xpath(XPATHS['jabber']).text
        self.assertEqual(jabber, TEST_DATA['jabber'])

        skype = driver.find_element_by_xpath(XPATHS['skype']).text
        self.assertEqual(skype, TEST_DATA['skype'])

        other = driver.find_element_by_xpath(XPATHS['other']).text
        self.assertEqual(other, TEST_DATA['other'])
