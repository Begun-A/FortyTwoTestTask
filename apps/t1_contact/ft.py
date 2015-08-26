from django.core.urlresolvers import reverse

from apps import TEST_DATA, BaseConfigTestCase


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
        self.assertEqual(first_name, TEST_DATA['first_name'])

        last_name = self.driver.find_element_by_xpath(xpaths['last_name']).text
        self.assertEqual(last_name, TEST_DATA['last_name'])

        birth_date = self.driver \
            .find_element_by_xpath(xpaths['birth_date']).text
        self.assertEqual(birth_date, TEST_DATA['birth_date'])

        bio = self.driver.find_element_by_xpath(xpaths['bio']).text
        self.assertEqual(bio, TEST_DATA['bio'])

        email = self.driver.find_element_by_xpath(xpaths['email']).text
        self.assertEqual(email, TEST_DATA['email'])

        jabber = self.driver.find_element_by_xpath(xpaths['jabber']).text
        self.assertEqual(jabber, TEST_DATA['jabber'])

        skype = self.driver.find_element_by_xpath(xpaths['skype']).text
        self.assertEqual(skype, TEST_DATA['skype'])

        other = self.driver.find_element_by_xpath(xpaths['other']).text
        self.assertEqual(other, TEST_DATA['other'])

    def test_contact_change_on_main_page(self):
        """Tests send data to server and get new updated data on page.
        """
        # first of all I need to login
        import time
        import datetime
        self.driver.get('%s%s' % (self.live_server_url, reverse('login')))
        self.driver.implicitly_wait(10)

        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('admin@admin.com')

        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('admin')

        self.driver.find_element_by_xpath('//input[@value="Sign in"]').click()
        time.sleep(3)
        # next I input fake data in inputs of xpaths
        xpaths = dict(
            first_name='//input[@id="id_first_name"]',
            last_name='//input[@id="id_last_name"]',
            birth_date='//input[@id="id_birth_date"]',
            bio='//input[@id="id_bio"]',
            email='//input[@id="id_email"]',
            jabber='//input[@id="id_jabber"]',
            skype='//input[@id="id_skype"]',
            other='//input[@id="id_other"]'
        )
        test_contact = dict(
            first_name='Miki',
            last_name='Rurk',
            birth_date=datetime.datetime.now(),
            bio='some infa',
            email='admin@admin.com',
            jabber='admin@jabber.com',
            skype='adminka',
            other='some goes'
        )
        first_name = self.driver \
            .find_element_by_xpath(xpaths['first_name'])
        first_name.send_keys(test_contact['first_name'])

        last_name = self.driver.find_element_by_xpath(xpaths['last_name'])
        last_name.send_keys(test_contact['last_name'])

        birth_date = self.driver \
            .find_element_by_xpath(xpaths['birth_date'])
        birth_date.send_keys(datetime.datetime.now())

        bio = self.driver.find_element_by_xpath(xpaths['bio'])
        bio.send_keys(test_contact['bio'])

        email = self.driver.find_element_by_xpath(xpaths['email'])
        email.send_keys(test_contact['email'])

        jabber = self.driver.find_element_by_xpath(xpaths['jabber'])
        jabber.send_keys(test_contact['jabber'])

        skype = self.driver.find_element_by_xpath(xpaths['skype'])
        skype.send_keys(test_contact['skype'])

        other = self.driver.find_element_by_xpath(xpaths['other'])
        other.send_keys(test_contact['other'])

        submit = self.driver.find_element_by_id('update_contact')
        submit.click()

        time.wait(10)
        # wait for processing and go to check data

        first_name = self.driver \
            .find_element_by_xpath(xpaths['first_name'])
        self.assertEqual(
            first_name.get_attribute("value"),
            test_contact['first_name']
        )

        last_name = self.driver.find_element_by_xpath(xpaths['last_name'])
        self.assertEqual(
            last_name.get_attribute("value"),
            test_contact['last_name']
        )

        birth_date = self.driver \
            .find_element_by_xpath(xpaths['birth_date'])
        self.assertEqual(
            birth_date.get_attribute("value"),
            test_contact['birth_date']
        )

        bio = self.driver.find_element_by_xpath(xpaths['bio'])
        self.assertEqual(bio.get_attribute("value"), test_contact['bio'])

        email = self.driver.find_element_by_xpath(xpaths['email'])
        self.assertEqual(email.get_attribute("value"), test_contact['email'])

        jabber = self.driver.find_element_by_xpath(xpaths['jabber'])
        self.assertEqual(jabber.get_attribute("value"), test_contact['jabber'])

        skype = self.driver.find_element_by_xpath(xpaths['skype'])
        self.assertEqual(skype.get_attribute("value"), test_contact['skype'])

        other = self.driver.find_element_by_xpath(xpaths['other'])
        self.assertEqual(other.get_attribute("value"), test_contact['other'])
