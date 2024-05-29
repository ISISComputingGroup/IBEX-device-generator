"""Runs tests associated with the IOC generation script"""

import argparse
import os
import sys
import unittest
from xmlrunner import XMLTestRunner
from tests.test_device_info import DeviceInfoTests

DEFAULT_TEST_LOCATION = "test-reports\\"


def run_tests(test_reports_path=DEFAULT_TEST_LOCATION):
    """
    Runs the test suite

    Args:
        test_reports_path: Path to test reports

    Returns:
        True if the tests passed, false otherwise
    """
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for case in [DeviceInfoTests]:
        suite.addTests(loader.loadTestsFromTestCase(case))

    return (
        XMLTestRunner(
            output=str(os.path.join(test_reports_path)), stream=sys.stdout
        )
        .run(suite)
        .wasSuccessful()
    )


def main():
    """
    Routine to run when script executed from the command line
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Runs tests for the IOC generation script",
    )
    parser.add_argument(
        "--reports_path",
        type=str,
        help="The folder in which test reports should be stored",
        default=DEFAULT_TEST_LOCATION,
    )

    args = parser.parse_args()
    run_tests(args.reports_path)


if __name__ == "__main__":
    main()
