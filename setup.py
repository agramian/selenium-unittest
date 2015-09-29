#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(name='selenium_unittest',
      version='0.1.2',
      description='Selenium Unit Test Framework',
      long_description=read_md('README.md'),
      author='Abtin Gramian',
      author_email='abtin.gramian@gmail.com',
      url='https://github.com/agramian/selenium-unittest',
      packages=['selenium_unittest'],
      install_requires=[
        'custom_text_test_runner',
        'selenium',
        'Appium-Python-Client==0.11'
      ],
      download_url = 'https://github.com/agramian/selenium-unittest/tarball/v0.1.2',
      keywords = ['selenium', 'unittest', 'unit', 'test', 'testing'],
      classifiers = [],
     )
