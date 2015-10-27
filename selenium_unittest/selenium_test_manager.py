#!/usr/bin/python

import sys, os, traceback
import inspect
import threading
import time
import timeit
from selenium import webdriver

def get_function_args(func_ref):
    try:
        return [p for p in inspect.getargspec(func_ref).args if p != 'self']
    except:
        return None

def store_class_fields(class_ref, args_passed):
    """ Store the passed in class fields in self
    """
    params = get_function_args(class_ref.__init__)
    for p in params: setattr(class_ref, p, args_passed[p])

class StartWebDriverError(Exception): pass

class SeleniumTestManager():
    """ A Class for managing and abstracting
    server and driver setup and usage for Selenium tests
    """

    def __init__(self,
                 browser_name,
                 browser_version,
                 webdriver_path,
                 base_url,
                 start_webdriver_num_tries=3):
        store_class_fields(self, locals())
        self.stdout_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        'selenium_server_stdout.log')

    def setup(self):
        """Start a web driver and return it
        """
        try:
            self._start_driver()
        except:
            print(traceback.format_exc())
            self.teardown()
            raise

    def teardown(self):
        """Stop the web driver
        """
        try:
            self._stop_driver()
        except:
            print(traceback.format_exc())
            pass

    def _start_driver(self):
        """Start the selenium web driver
        """
        for i in range(self.start_webdriver_num_tries):
            try:
                print "Starting the Selenium WebDriver...\n"
                if self.browser_name.lower() == 'chrome':
                    self.driver = webdriver.Chrome(self.webdriver_path)
                break
            except Exception as e:
                if i == self.start_webdriver_num_tries - 1:
                    raise StartWebDriverError('Failed to start WebDriver!\n[%s] %s'
                                              %(type(e).__name__, e))
                else:
                    print 'Failed to start WebDriver!\nTrying again...\n'
                    pass
        print "Selenium WebDriver started.\n"

    def _stop_driver(self):
        """Stop the selenium driver
        """
        print "Stopping the Selenium WebDriver...\n"
        self.driver.close()
        print "Selenium WebDriver stopped.\n"
