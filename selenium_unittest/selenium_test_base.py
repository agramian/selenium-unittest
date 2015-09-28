#!/usr/bin/python

import os
import unittest
from time import sleep
import json
import re
from selenium_test_manager import SeleniumTestManager
from selenium.webdriver.support.ui import WebDriverWait

class BaseSeleniumTest(unittest.TestCase):
    suite_is_setup = False
    suite_is_teared_down = False
    default_implicit_wait_time = 2
    default_explicit_wait_time = 10
    default_window_size = {'width': 1280, 'height': 720}
    default_window_position = {'x': 0, 'y': 0}

    @classmethod
    def setUpClass(cls):
        selenium_config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "selenium.cfg")
        selenium_cfg = json.load(open(selenium_config_file_path))
        BaseSeleniumTest.browser_name = selenium_cfg['browser_name']
        cls.selenium_test_manager = SeleniumTestManager(**{k:v for (k,v) in selenium_cfg.iteritems() if v})
        cls.selenium_test_manager.setup()
        cls.selenium_server_is_setup = True
        cls.selenium_screenshot_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../results/screenshots", cls.__name__))

    @classmethod
    def tearDownClass(cls):
        BaseSeleniumTest.suite_is_setup = False
        BaseSeleniumTest.suite_is_teared_down = False
        cls.selenium_test_manager.teardown()

    def setUp(self):
        self.stream = self.__dict__['_resultForDoCleanups'].__dict__['stream']
        self.driver = self.get_driver()
        self.driver.set_window_size(BaseSeleniumTest.default_window_size['width'], BaseSeleniumTest.default_window_size['height'])
        self.driver.set_window_position(BaseSeleniumTest.default_window_position['x'], BaseSeleniumTest.default_window_position['y'])
        self.reset_command_wait_time()
        self.screenshot_dir = os.path.join(self.get_screenshot_dir(), self._testMethodName)
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
        if not BaseSeleniumTest.suite_is_setup and hasattr(self, 'setup_suite'):
            self.setup_suite()
            BaseSeleniumTest.suite_is_setup = True
        if hasattr(self, 'setup_case'):
            self.setup_case()

    def tearDown(self):
        """
        # TODO need logic to detect that it's the last test case of the suite
        if not BaseAppiumTest.suite_is_teared_down and hasattr(self, 'teardown_suite'):
            self.teardown_suite()
            BaseAppiumTest.suite_is_teared_down = True
        """
        if hasattr(self, 'teardown_case'):
            try:
                self.teardown_case()
            except:
                test_dict = self._resultForDoCleanups
                test_case_dict = test_dict.results['suites'][test_dict.suite_map[test_dict.suite]]['cases'][test_dict.current_case_number]
                if not test_case_dict['errors'] and not test_case_dict['failures']:
                    raise

    @classmethod
    def get_driver(cls):
        return cls.selenium_test_manager.driver

    def reset_command_wait_time(self):
        self.driver.implicitly_wait(BaseSeleniumTest.default_implicit_wait_time)
        self.wait = WebDriverWait(self.driver, BaseSeleniumTest.default_explicit_wait_time)

    @classmethod
    def get_screenshot_dir(cls):
        return cls.selenium_screenshot_dir

    def take_screenshot(self, name=None):
        if not name: name = self._testMethodName
        # make screenshot and save it to the local filesystem
        name_format = re.compile("([^\.]*)\.?(\d{0,3})")
        while os.path.isfile(os.path.join(self.screenshot_dir, '%s.png' %name)):
            name_match = name_format.match(name)
            name = name_match.group(1)
            num = name_match.group(2)
            if not num:
                num = 0
            else:
                num = int(num) + 1
            name = '%s.%03d' %(name, num)
        success = self.driver.get_screenshot_as_file(os.path.join(self.screenshot_dir, '%s.png' %name))
        self.assertTrue(success)
        self.assertTrue(os.path.isfile(os.path.join(self.screenshot_dir, '%s.png' %name)))
