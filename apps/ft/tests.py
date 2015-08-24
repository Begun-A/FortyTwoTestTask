import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.core.urlresolvers import reverse

from apps import TEST_DATA, FAKE_PATH_LIST
from apps import initial_data

from apps.hello.models import LogWebRequest


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


class ContactIntegrationTest(unittest.TestCase):
    """Perform tests to the data which rendered on the page and
    check it with database initial data.
    """

    def setUp(self):
        self.pk = initial_data[0]['pk']
        self.fake_path = reverse('contact', kwargs={'pk': self.pk})
        self.absolute_url = 'http://127.0.0.1:8000' + self.fake_path
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def test_contact_find_data_on_page_and_check_it_with_base(self):
        """Tests all data on rendered page and check it with database.
        """
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


class LogWebRequestIntegrationTest(unittest.TestCase):
    """Perform tests to the data which rendered on the page,
    step on different pages via one uri.
    """

    def setUp(self):
        self.fake_path = reverse('requests')
        self.uri = 'http://127.0.0.1:8000'
        self.absolute_url = self.uri + self.fake_path
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def test_10_fake_requests(self):
        """Test 10 different requests and check them on requests page.
        """
        driver = self.driver
        driver.get(self.absolute_url)
        driver.implicitly_wait(10)

        for fake_path in FAKE_PATH_LIST:
            # step on another tab in browser
            body = driver.find_element_by_tag_name('body')
            body.send_keys(Keys.CONTROL + 't')
            # go to this link
            url = self.uri + fake_path
            driver.get(url)
            driver.implicitly_wait(10)
            # return back, see if we get new result
            body = driver.find_element_by_tag_name('body')
            body.send_keys(Keys.CONTROL + Keys.F4)

            queryset = LogWebRequest.objects.order_by('-id')[0]
            last_rec = [
                each.value_from_object(queryset)
                for each in queryset._meta.fields
            ]
            driver.refresh()
            first_row = self.driver.find_elements_by_tag_name('tr')[1].text
            map(
                lambda row: self.assertIn(
                    unicode(row), first_row
                ), last_rec[:3]
            )

    def test_title_of_3_req(self):
        """Test 3 requests and check title if it changed.
        """
        driver = self.driver
        driver.get(self.absolute_url)
        driver.implicitly_wait(10)

        init_title = driver.title
        depth = 0
        for fake_path in FAKE_PATH_LIST[:3]:
            # step on another tab in browser
            body = driver.find_element_by_tag_name('body')
            body.send_keys(Keys.CONTROL + 't')
            # go to this link
            url = self.uri + fake_path
            # ipdb.set_trace()
            driver.get(url)
            driver.implicitly_wait(10)
            depth = depth + 1
        # return back, see if we get new result
        time.sleep(1)
        for d in xrange(depth):
            body = driver.find_element_by_tag_name('body')
            body.send_keys(Keys.CONTROL + Keys.F4)
        # ipdb.set_trace()
        new_title = driver.title
        self.assertNotEqual(init_title, new_title)
        self.assertEqual(new_title, "3 new requests")
