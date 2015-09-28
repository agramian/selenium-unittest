#!/usr/bin/env python

from distutils.core import setup

setup(name='selenium_unittest',
      version='0.1',
      description='Selenium Unit Test Framework',
      author='Abtin Gramian',
      author_email='abtin.gramian@gmail.com',
      url='https://github.com/agramian/selenium-unittest',
      packages=['selenium_unittest'],
      install_requires=[
        'custom_text_test_runner',
        'selenium',
        'Appium-Python-Client==0.11'
      ],
      download_url = 'https://github.com/agramian/selenium-unittest/tarball/v0.1',
      keywords = ['selenium', 'unittest', 'unit', 'test', 'testing'],
      classifiers = [],
     )
