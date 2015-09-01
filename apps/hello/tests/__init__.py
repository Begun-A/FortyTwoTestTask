from .test_login import LoginUnitTest # flake8: noqa
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import LiveServerTestCase


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
