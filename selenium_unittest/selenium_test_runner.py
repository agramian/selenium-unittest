#!/usr/bin/python

# parse command line args
import argparse

parser = argparse.ArgumentParser(description='Run a Selenium test')
parser.add_argument('--browser_name',
                    dest='browser_name',
                    help='Browser to run tests on.',
                    choices=['Chrome'],
                    required=True)
parser.add_argument('--browser_version',
                    dest='browser_version',
                    help='Selenium test browser version.',
                    default='latest')
parser.add_argument('--test_suites',
                    dest='test_suites',
                    help='Comma-separated test directories.')
parser.add_argument('--test_types',
                    dest='test_types',
                    help='Comma-separated list of test types to run (Ex: "Smoke", "Guide-Discovery")')
parser.add_argument('--pattern',
                    dest='pattern',
                    default='*test*.py',
                    help='Regular expression to filter which file patterns to regard as tests.')
parser.add_argument('--show_previous_results',
                    action='store_true',
                    help='Whether to combine the results of previous test runs for display at the end.')
parser.add_argument('--base_url',
                    dest='base_url',
                    help='Base url to use for tests.',
                    default='https://beta.guidebook.com')
args = parser.parse_args()

# write selenium parameters to file
import json
kwargs = {
    'browser_name': args.browser_name,
    'browser_version': args.browser_version,
    'base_url': args.base_url
}
import os
current_script_path = os.path.dirname(os.path.abspath(__file__))
selenium_config_file_path = os.path.join(current_script_path, "selenium.cfg")
json.dump(kwargs, open(selenium_config_file_path,'w'))

# discover and run tests
import unittest
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "../../"))
from utils.python_unittest.custom_text_test_runner import CustomTextTestRunner

def run_tests(start_dir, pattern, top_level_dir):
    test_modules = unittest.defaultTestLoader.discover(start_dir=start_dir, pattern=pattern, top_level_dir=top_level_dir)
    for suites in test_modules._tests:
        for suite in suites._tests:
            for test in suite._tests:
                test.__dict__.update(kwargs.items())
    return test_modules
start_dir = os.path.normpath('%s/../tests' %(current_script_path))
results_dir = os.path.abspath(os.path.normpath('%s/../results/' %current_script_path))
results_file_path = os.path.join(results_dir, args.browser_version, '%s.json' %(args.browser_name))
result_screenshots_dir = os.path.join(results_dir, 'screenshots')
# delete previous results if show_previous_results not specified
if not args.show_previous_results and os.path.exists(results_file_path):
    os.remove(results_file_path)
return_code = 0
if args.test_types:
    test_types = [x.strip() for x in args.test_types.split(',')]
else:
    test_types = None
if args.test_suites:
    for suite in args.test_suites.split(','):
        if not suite: continue
        suite_start_dir = os.path.normpath('%s/%s' %(start_dir, suite))
        try:
            tests = run_tests(suite_start_dir, args.pattern, start_dir)
        except:
            return_code = 1
            raise Exception("No tests found for suite: %s" %suite)
        rc = CustomTextTestRunner(verbosity=5,
                                  results_file_path=results_file_path,
                                  result_screenshots_dir=result_screenshots_dir,
                                  show_previous_results=True,
                                  #selenium_cfg=kwargs,
                                  test_types=test_types).run(tests).returnCode()
        if return_code == 0: return_code = rc
else:
    try:
        tests = run_tests(start_dir, args.pattern, start_dir)
    except:
        return_code = 1
        raise Exception("No tests found")
    return_code = CustomTextTestRunner(verbosity=5,
                                       results_file_path=results_file_path,
                                       result_screenshots_dir=result_screenshots_dir,
                                       show_previous_results=True if args.show_previous_results else False,
                                       #selenium_cfg=kwargs,
                                       test_types=test_types).run(tests).returnCode()
import sys
sys.exit(return_code)
