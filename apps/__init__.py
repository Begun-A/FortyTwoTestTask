import os
import json

from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import LiveServerTestCase

with open(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        't1_contact/fixtures/initial_data.json'
    )
) as test_data:
    initial_data = json.load(test_data)


TEST_DATA = initial_data[1]['fields']
TEST_DATA['password'] = 'qwerty'
IMG_PATH = '~/Pictures/test.jpg'
FAKE_PATH_LIST = [
    '/fefw',
    '/12747630-426-13!@$*&_*&%!_)&@*$&__!#  *$!@$*_!%)(&#*$&&$)!(#$)(',
    '/',
    '/el/',
    '/www',
    '/1242',
    '/?d=3',
    '/?_=23423523',
    '/avaba-kedabra/',
    '/****/'
]


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
