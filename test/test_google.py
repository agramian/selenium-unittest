#!/usr/bin/python

from selenium_unittest.selenium_test_base import BaseSeleniumTest
from custom_text_test_runner import case_name
import time

class LoginSuccessTests(BaseSeleniumTest):

    base_test_category='Google'

    def setup_suite(self):
        self.driver.get('http://google.com')

    @case_name('Search Google')
    def test_successful_login(self):
        """Entering a query and hitting the search button should show the results page
        """
        self.driver.find_element_by_xpath("//input[@title='Search']").send_keys('test')
        time.sleep(1)
        self.driver.find_element_by_xpath("//button[@value='Search']").click()
        time.sleep(2)
