import time
from django.core.urlresolvers import reverse

from .ft import BaseConfigTestCase


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
