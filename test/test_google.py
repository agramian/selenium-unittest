#!/usr/bin/python

from selenium_unittest.selenium_test_base import BaseSeleniumTest
from custom_text_test_runner import case_name
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class GoogleTests(BaseSeleniumTest):
    """Sample tests using Google
    """

    base_test_category='Google' # for suite identification in results file and print out

    def setup_suite(self):
        self.driver.get('http://google.com')

    def teardown_suite(self):
        # pause before closing so user can see page
        time.sleep(2)

    def setup_case(self):
        self.take_screenshot()

    def teardown_case(self):
        self.take_screenshot('teardown')

    @case_name('Search Google')
    def test_google_search(self):
        """Entering a query and hitting the search button should show the results page
        """
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@title='Search']"))
        )
        self.driver.find_element_by_xpath("//input[@title='Search']").send_keys('test')
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@value='Search']"))
        )
        self.driver.find_element_by_xpath("//button[@value='Search']").click()
