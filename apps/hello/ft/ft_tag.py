import time

from .ft import BaseConfigTestCase


class TagTest(BaseConfigTestCase):
    """Perform tests to the render of tag and go on it link.
    """

    @classmethod
    def setUpClass(cls):
        cls.fake_path = '/admin/contact/1/'
        super(TagTest, cls).setUpClass()

    def test_edit_link_url(self):
        """Click on link and go modify.
        """
        self.driver.get('%s%s' % (self.live_server_url, self.fake_path))
        self.driver.implicitly_wait(10)

        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('admin@admin.com')

        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('admin')

        self.driver.find_element_by_xpath('//input[@value="Sign in"]').click()
        time.sleep(3)

        self.driver.find_element_by_xpath(
            '//a[@href="%s"]' % self.fake_path
        ).click()
        time.sleep(2)
        self.assertequal(self.driver.current_url, self.fake_path)
