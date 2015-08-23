import os
import unittest
import json
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from selenium import webdriver

from .models import Contact
from .views import ContactView

 
TEST_DATA = dict(
    first_name="Bogdan",
    last_name="Kurinnyi",
    birth_date="1994-07-26",
    bio="self.educated man, try to find himself in web development.",
    contacts="063-981-33-35",
    email="dev1dor@ukr.net",
    jabber="dev1dor@jabber.ua",
    skype="DeV1doR",
    other="Some other contacts"
)

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
        self.contact = Contact.objects.get(email=TEST_DATA['email'])
        self.fake_path = reverse('contact', kwargs={'pk': self.contact.id})

    def tearDown(self):
    	self.contact.delete()


class ContactUnitTest(BaseConfigTestCase):

    def setUp(self):
        super(ContactUnitTest, self).setUp()
        self.factory = RequestFactory()

    def test_t1_contact_get_ok_request_and_check_title(self):
        request = self.factory.get(path=self.fake_path)
        view = ContactView.as_view()
        response = view(request, pk=self.contact.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
        	' '.join([TEST_DATA['first_name'], TEST_DATA['last_name']]), 
        	response.content
    	)


class ContactIntegrationTest(BaseConfigTestCase):

    def setUp(self):
        super(ContactIntegrationTest, self).setUp()
        self.driver = webdriver.Firefox()

    def tearDown(self):
    	super(ContactIntegrationTest, self).tearDown()
        self.driver.quit()

    def test_t1_contact_find_data_on_page_and_check_it_with_base(self):
        driver = self.driver
        driver.get(self.fake_path)
        driver.implicitly_wait(10)

        self.assertEqual(
            driver.title,
            ' '.join([TEST_DATA['first_name'], TEST_DATA['last_name']])
        )

        first_name = driver.find_element_by_xpath(XPATHS['first_name'])
        self.assertEqual(first_name, TEST_DATA['first_name'])

        last_name = driver.find_element_by_xpath(XPATHS['last_name'])
        self.assertEqual(last_name, TEST_DATA['last_name'])

        birth_date = driver.find_element_by_xpath(XPATHS['birth_date'])
        self.assertEqual(birth_date, TEST_DATA['birth_date'])

        bio = driver.find_element_by_xpath(XPATHS['bio'])
        self.assertEqual(bio, TEST_DATA['bio'])

        contacts = driver.find_element_by_xpath(XPATHS['contacts'])
        self.assertEqual(contacts, TEST_DATA['contacts'])

        email = driver.find_element_by_xpath(XPATHS['email'])
        self.assertEqual(email, TEST_DATA['email'])

        jabber = driver.find_element_by_xpath(XPATHS['jabber'])
        self.assertEqual(jabber, TEST_DATA['jabber'])

        skype = driver.find_element_by_xpath(XPATHS['skype'])
        self.assertEqual(skype, TEST_DATA['skype'])

        other = driver.find_element_by_xpath(XPATHS['other'])
        self.assertEqual(other, TEST_DATA['other'])
