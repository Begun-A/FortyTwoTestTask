import time
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase

from apps import TEST_DATA, FAKE_PATH_LIST
from apps.hello.models import LogWebRequest


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


class BaseConfigTestCase(LiveServerTestCase):
    """Config for initialization LiveServer.
    """
    fixtures = ['initial_data.json']

    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver()
        super(BaseConfigTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(BaseConfigTestCase, cls).tearDownClass()


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


class LogWebRequestIntegrationTest(BaseConfigTestCase):
    """Perform tests to the data which rendered on the page,
    step on different pages via one uri.
    """

    @classmethod
    def setUpClass(cls):
        cls.fake_path = reverse('requests')
        super(LogWebRequestIntegrationTest, cls).setUpClass()

    def test_10_fake_requests(self):
        """Test 10 different requests and check them on requests page.
        """
        self.driver.get('%s%s' % (self.live_server_url, self.fake_path))
        self.driver.implicitly_wait(10)

        for fake_path in FAKE_PATH_LIST:
            # step on another tab in browser
            body = self.driver.find_element_by_tag_name('body')
            body.send_keys(Keys.CONTROL + 't')
            self.driver.implicitly_wait(10)
            # go to this link
            self.driver.get('%s%s' % (self.live_server_url, fake_path))
            self.driver.implicitly_wait(10)
            # return back, see if we get new result
            body = self.driver.find_element_by_tag_name('body')
            body.send_keys(Keys.CONTROL + Keys.F4)

            queryset = LogWebRequest.objects.order_by('-id')[0]
            last_rec = [
                each.value_from_object(queryset)
                for each in queryset._meta.fields
            ]
            self.driver.refresh()
            first_row = self.driver.find_elements_by_tag_name('tr')[1].text
            map(
                lambda row: self.assertIn(
                    unicode(row), first_row
                ), last_rec[:3]
            )

    def test_title_of_3_req(self):
        """Test 3 requests and check title if it changed.
        """

        self.driver.get('%s%s' % (self.live_server_url, self.fake_path))
        self.driver.implicitly_wait(10)

        import time
        time.sleep(2)
        init_title = self.driver.title
        depth = 0
        for fake_path in FAKE_PATH_LIST[:3]:
            # step on another tab in browser
            body = self.driver.find_element_by_tag_name('body')
            body.send_keys(Keys.CONTROL + 't')
            self.driver.implicitly_wait(10)
            # go to this link
            self.driver.get('%s%s' % (self.live_server_url, fake_path))
            self.driver.implicitly_wait(10)
            depth = depth + 1
        # return back, see if we get new result
        for d in xrange(depth):
            body = self.driver.find_element_by_tag_name('body')
            body.send_keys(Keys.CONTROL + Keys.F4)
            self.driver.implicitly_wait(10)
        # ipdb.set_trace()
        new_title = self.driver.title
        self.assertNotEqual(init_title, new_title)
        self.assertEqual(new_title, "3 new requests")


class LoginFormIntegrationTest(BaseConfigTestCase):
    """Perform tests to the data which rendered on the page,
    step on different pages via one uri.
    """

    @classmethod
    def setUpClass(cls):
        cls.fake_path = reverse('login')
        super(LoginFormIntegrationTest, cls).setUpClass()

    def test_sent_with_valid_data(self):
        """Check if submit is ok and get redirect to contact page.
        """

        self.driver.get('%s%s' % (self.live_server_url, self.fake_path))
        self.driver.implicitly_wait(10)

        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('admin@admin.com')

        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('admin')

        self.driver.find_element_by_xpath('//input[@value="Sign in"]').click()
        time.sleep(3)
        self.assertEqual(
            '%s%s' % (self.live_server_url, reverse('contact')),
            self.driver.current_url
        )

    def test_sent_with_invalid_data(self):
        """Check if form show errors.
        """

        self.driver.get('%s%s' % (self.live_server_url, self.fake_path))
        self.driver.implicitly_wait(10)

        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('hello')

        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('I try to hack')

        sign_in = self.driver.find_element_by_xpath(
            '//input[@value="Sign in"]'
        )
        sign_in.click()
        # check for disabled button
        self.assertTrue(sign_in.is_enabled())
        # we dont want to go with bad data
        self.assertNotEqual(
            '%s%s' % (self.live_server_url, reverse('contact')),
            self.driver.current_url
        )
        # we stay on this page
        self.assertEqual(
            '%s%s' % (self.live_server_url, self.fake_path),
            self.driver.current_url
        )
        sub_b_xpath = '//div[@class="help-block"]'
        page_error = self.driver.find_element_by_xpath(sub_b_xpath).text
        check_errors = [
            'Username is required.',
            'Password is required.',
            'Please enter a correct username and password. '
            'Note that both fields may be case-sensitive.'
        ]

        self.assertEqual(page_error, check_errors[2])

        # clear username input, check it error
        username_input.clear()
        sign_in.click()
        page_error = self.driver.find_element_by_xpath(sub_b_xpath).text
        self.assertEqual(page_error, check_errors[0])

        # clear password input, check it error
        password_input.clear()
        username_input.send_keys('hello')
        sign_in.click()
        page_error = self.driver.find_element_by_xpath(sub_b_xpath).text
        self.assertEqual(page_error, check_errors[1])

        # clear both input, check 2 errors
        username_input.clear()
        sign_in.click()
        page_errors = [
            error.text for error in
            self.driver.find_elements_by_xpath(sub_b_xpath)
        ]
        map(lambda error: self.assertIn(error, check_errors[:2]), page_errors)
