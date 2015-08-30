from django.core.urlresolvers import reverse

from hello.models import Contact
from hello.ft import BaseConfigTestCase


class ContactIntegrationTest(BaseConfigTestCase):
    """Perform tests to the data which rendered on the page and
    check it with database initial data.
    """

    @classmethod
    def setUpClass(cls):
        cls.fake_path = reverse('contact')
        cls.model = Contact
        super(ContactIntegrationTest, cls).setUpClass()

    def test_contact_find_data_on_page_and_check_it_with_base(self):
        """Tests all data on rendered page and check it with database.
        """
        contact = self.model.objects.last()
        self.driver.get('%s%s' % (self.live_server_url, self.fake_path))
        self.driver.implicitly_wait(10)

        self.assertEqual(
            self.driver.title,
            unicode(
                ' '.join(contact.first_name, contact.last_name)
            )
        )
        xpaths = dict(
            first_name='//span[@id="first_name"]',
            last_name='//span[@id="last_name"]',
            birth_date='//span[@id="birth_date"]',
            bio='//span[@id="bio"]',
            email='//span[@id="email"]',
            jabber='//span[@id="jabber"]',
            skype='//span[@id="skype"]',
            other='//span[@id="other"]'
        )
        first_name = self.driver \
            .find_element_by_xpath(xpaths['first_name']).text
        self.assertEqual(first_name, contact.first_name)

        last_name = self.driver.find_element_by_xpath(xpaths['last_name']).text
        self.assertEqual(last_name, contact.last_name)

        birth_date = self.driver \
            .find_element_by_xpath(xpaths['birth_date']).text
        self.assertEqual(birth_date, contact.birth_date)

        bio = self.driver.find_element_by_xpath(xpaths['bio']).text
        self.assertEqual(bio, contact.bio)

        email = self.driver.find_element_by_xpath(xpaths['email']).text
        self.assertEqual(email, contact.email)

        jabber = self.driver.find_element_by_xpath(xpaths['jabber']).text
        self.assertEqual(jabber, contact.contact.jabber)

        skype = self.driver.find_element_by_xpath(xpaths['skype']).text
        self.assertEqual(skype, contact.skype)

        other = self.driver.find_element_by_xpath(xpaths['other']).text
        self.assertEqual(other, contact.other)
