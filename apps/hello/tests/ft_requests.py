from selenium.webdriver.common.keys import Keys
from django.core.urlresolvers import reverse

from hello.factories import FAKE_PATH_LIST
from hello.models import LogWebRequest
from hello.tests import BaseConfigTestCase


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
            # go to this link
            self.driver.get('%s%s' % (self.live_server_url, fake_path))
            # return back, see if we get new result
            body = self.driver.find_element_by_tag_name('body')
            body.send_keys(Keys.CONTROL + Keys.F4)

            queryset = LogWebRequest.objects.order_by('-id')[0]
            last_rec = [
                each.value_from_object(queryset)
                for each in queryset._meta.fields
            ]
            self.driver.refresh()
            first_row = self.driver.find_elements_by_tag_name('tr')[2].text
            for row in last_rec[:3]:
                self.assertIn(unicode(row), first_row)

    def test_title_of_10_req(self):
        """Test 10 requests and check title if it changed.
        """

        self.driver.get('%s%s' % (self.live_server_url, self.fake_path))
        self.driver.implicitly_wait(10)

        import time
        time.sleep(2)

        init_title = self.driver.title
        for fake_path in FAKE_PATH_LIST:
            # step on another tab in browser
            body = self.driver.find_element_by_tag_name('body')
            body.send_keys(Keys.CONTROL + 't')
            # go to this link
            self.driver.get('%s%s' % (self.live_server_url, fake_path))
            time.sleep(1)

        # return back, see if we get new result
        body = self.driver.find_element_by_tag_name('body')
        body.send_keys(Keys.CONTROL + Keys.TAB)

        new_title = self.driver.title
        self.assertNotEqual(init_title, new_title)
        self.assertEqual(new_title, "(10) New requests")
