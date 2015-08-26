from django.core.urlresolvers import reverse

from apps import TEST_DATA, BaseConfigTestCase


XPATHS = dict(
    first_name='//span[@id="first_name"]',
    last_name='//span[@id="last_name"]',
    birth_date='//span[@id="birth_date"]',
    bio='//span[@id="bio"]',
    email='//span[@id="email"]',
    jabber='//span[@id="jabber"]',
    skype='//span[@id="skype"]',
    other='//span[@id="other"]'
)


class ContactIntegrationTest(BaseConfigTestCase):
    """Perform tests to the data which rendered on the page and
    check it with database initial data.
    """

    @classmethod
    def setUpClass(cls):
        cls.fake_path = reverse('contact')
        super(ContactIntegrationTest, cls).setUpClass()

    def test_contact_find_data_on_page_and_check_it_with_base(self):
        """Tests all data on rendered page and check it with database.
        """
        self.driver.get('%s%s' % (self.live_server_url, self.fake_path))
        self.driver.implicitly_wait(10)

        self.assertEqual(
            self.driver.title,
            unicode(
                ' '.join([TEST_DATA['first_name'], TEST_DATA['last_name']])
            )
        )

        first_name = self.driver \
            .find_element_by_xpath(XPATHS['first_name']).text
        self.assertEqual(first_name, TEST_DATA['first_name'])

        last_name = self.driver.find_element_by_xpath(XPATHS['last_name']).text
        self.assertEqual(last_name, TEST_DATA['last_name'])

        birth_date = self.driver \
            .find_element_by_xpath(XPATHS['birth_date']).text
        self.assertEqual(birth_date, TEST_DATA['birth_date'])

        bio = self.driver.find_element_by_xpath(XPATHS['bio']).text
        self.assertEqual(bio, TEST_DATA['bio'])

        email = self.driver.find_element_by_xpath(XPATHS['email']).text
        self.assertEqual(email, TEST_DATA['email'])

        jabber = self.driver.find_element_by_xpath(XPATHS['jabber']).text
        self.assertEqual(jabber, TEST_DATA['jabber'])

        skype = self.driver.find_element_by_xpath(XPATHS['skype']).text
        self.assertEqual(skype, TEST_DATA['skype'])

        other = self.driver.find_element_by_xpath(XPATHS['other']).text
        self.assertEqual(other, TEST_DATA['other'])
