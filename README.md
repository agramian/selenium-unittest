Selenium Unittest
=================
Contents
--------
### [Overview](#overview-1)
### [Setup](#setup-1)
##### [Installation](#installation-1)
##### [WebDrivers](#webdrivers-1)
### [Running tests](#running-tests-1)
##### [Usage](usage-1)
##### [Example](example-1)
### [Using the Chrome Developer Console](#using-the-chrome-developer-console-1)
##### [Description](#description-1)
##### [Useful commands](#useful-commands-1)
##### [Element query examples](#element-query-examples-1)
##### [More info](#more-info-1)
### [Code organization](#code-organization-1)
### [TODO](#todo-1)

Overview
--------
A Selenium Unit Test Framework for [Selenium](http://www.seleniumhq.org/) with the [Selenium Python client](https://selenium-python.readthedocs.org/index.html).

Selenium is an open-source **web application automation and testing framework**.  Tests are written using WebDriver-compatible language-specific client libraries.

The Selenium tests are written in *Python* and run through the language's built-in *unittest* framework.  A custom test runner and reporter handle boilerplate Selenium setup along with storage of results in a json file for post-processing.

###### [Back to top](#contents)

Setup
-----

###### Installation
```
pip install selenium_unittest
```

###### WebDrivers
Download one or more WebDriver executables from [here](http://www.seleniumhq.org/download/) to a desired location.

*Note: Make sure the executables allow read and execution permission*

###### [Back to top](#contents)

Running tests
-------------

For basic usage, execute the following command in a directory.  By default test discovery will occur relative to the working directory and will look for any filenames containing the string "test".  The command below also assumes that the chromedriver executable is located in a directory named webdrivers inside the working directory.

`python -m selenium_unittest.selenium_test_runner.py --browser_name "Chrome" --webdriver_path "webdrivers/chromedriver"`

###### Usage
```
usage: -c [-h] --browser_name {Chrome} [--browser_version BROWSER_VERSION]
          [--test_suites TEST_SUITES] [--test_types TEST_TYPES]
          [--pattern PATTERN] [--show_previous_results] [--base_url BASE_URL]

Run a Selenium test

optional arguments:
  -h, --help            show this help message and exit
  --browser_name {Chrome}
                        Browser to run tests on.
  --webdriver_path WEBDRIVER_PATH
                        Path to webdriver executable.
  --webdriver_path_type {absolute,relative}
                        Type of path to use when determining webdriver_path.
  --browser_version BROWSER_VERSION
                        Selenium test browser version.
  --test_dir TEST_DIR   Path to directory containing tests. (path type is
                        based on value of --test_dir_path_type which defaults
                        to relative)
  --test_dir_path_type {absolute,relative}
                        Type of path to use when determining test_dir
                        location.
  --results_dir RESULTS_DIR
                        Path to directory to read/write results from/to.(path
                        type is based on value of --results_dir_path_type
                        which defaults to relative)
  --results_dir_path_type {absolute,relative}
                        Type of path to use when determining results_dir
                        location.
  --test_suites TEST_SUITES
                        Comma-separated test directories.
  --test_types TEST_TYPES
                        Comma-separated list of test types to run (Ex:
                        "Smoke", "Guide-Discovery")
  --pattern PATTERN     Regular expression to filter which file patterns to
                        regard as tests.
  --show_previous_results
                        Whether to combine the results of previous test runs
                        for display at the end.
  --base_url BASE_URL   Base url to use for tests.
```

###### Example
An example test is provided in the test directory.

To run it clone the repo and execute the following command from the main directory:<br />
`python -m selenium_unittest.selenium_test_runner.py --browser_name "Chrome" --test_dir "test" --webdriver_path "test/webdrivers/chromedriver"`

###### [Back to top](#contents)

Using the Chrome Developer Console
----------------------------------

##### Description
Allows direct interaction and inspection of the web app in real-time via the web browser's console.  This is helpful when debugging or writing tests because it allows you to see a list of DOM elements on each page of the web app along with their properties.  For example while writing a test you will need to click buttons, interact with forms, verify properties, etc.  In order to write such a test, you will need to reference elements by id, name, or some other identifiers.  The fastest way to figure out how to reference an element is by navigating to the page of the web app where the test will start from using the browser, right clicking on elements and selecting "Inspect Element" from the context menu, then trying to reference the element through the Chrome Developer Console using the commands below.

##### Useful commands

```$()``` Returns the first element that matches the CSS selector specified within the parantheses. It is a shortcut for document.querySelector()<br />
```$$()``` Returns an array of all the elements that match the CSS selector specified within the parantheses. This is an alias for document.querySelectorAll()<br />
```$x()``` Returns an array of elements that match the XPath specified within the parantheses.<br />

##### Element query examples
```$x("//span[text()='Guidebook']")``` Returns an array of span tag elements containing the text "Guidebook".<br />
```$("p.usm_name span").textContent``` Returns the text content of the first span tag element which is a child of a "p" element with class "usm_name".

##### More info
Additional info regarding the Chrome Developer Console is available [here](https://developer.chrome.com/devtools/docs/console).

###### [Back to top](#contents)

Code organization
-----------------
```js
selenium_unittest
├── selenium_test_base.py // base selenium test class
├── selenium_test_manager.py // handles common server/driver setup/teardown
├── selenium_test_runner.py // receives command line arguments, then discovers and runs selenium tests
```

###### [Back to top](#contents)

TODO
----
- add support for WebDrivers beside ChromeDriver
- implement teardown_suite()
- currently if show_previous_results is specified to the test runner, if the same suite or case is run there is no differentiation in the output or screenshot directory (add timestamp)
- add sample json format of result file in README

###### [Back to top](#contents)
