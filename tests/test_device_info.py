"""Test device info."""

from os.path import join
from unittest import TestCase

import ibex_device_generator.utils.placeholders as p
from ibex_device_generator.exc import (
    InvalidDeviceNameError,
    InvalidIOCNameError,
)
from ibex_device_generator.paths import EPICS, EPICS_SUPPORT
from ibex_device_generator.utils.device_info import (
    DeviceInfo,
    get_year,
)

from tests.test_placeholders import get_placeholders


class DeviceInfoTests(TestCase):
    """Test Device Info."""

    def setUp(self) -> None:
        """Create a device."""
        self.placeholders = get_placeholders()
        self.device = DeviceInfo("ND1", "New Device 1", device_count=4)

    def test_all_keys_present_in_device_info_substitutions(self) -> None:
        """Check that all placeholders are used as keys in the device info."""
        # -> Check all vars in substitution_keys are used
        for name, value in self.placeholders.items():
            self.assertIn(
                value,
                self.device,
                msg=(
                    f"Key '{name}' ('{value}') is missing from the"
                    " device info substitutions."
                ),
            )
        # <- Check all keys in device info substitutions exists
        # in substitution_keys
        for key, value in self.device.items():
            self.assertIn(
                key,
                self.placeholders.values(),
                msg=(
                    f"Deice info substitutions contains a key ('{key}')"
                    " that is not present in utils.substitution_keys"
                ),
            )

    def test_device_info_substitutions_are_correct(self) -> None:
        """Test substitution correctness."""
        expected_substitutions = {
            p.IOC_NAME: "ND1",
            p.DEVICE_NAME: "New Device 1",
            p.DEVICE_SUPPORT_MODULE_NAME: "new_device_1",
            p.LEWIS_DEVICE_NAME: "new_device_1",
            p.DEVICE_DATABASE_NAME: "new_device_1",
            p.DEVICE_PROTOCOL_NAME: "new_device_1",
            p.LEWIS_DEVICE_CLASS_NAME: "NewDevice1",
            p.SUPPORT_PATH: join(EPICS_SUPPORT, "new_device_1"),
            p.SUPPORT_MASTER_PATH: join(
                EPICS_SUPPORT, "new_device_1", "master"
            ),
            p.GITHUB_REPO_NAME: "EPICS-New_Device_1",
            p.DEVICE_COUNT: 4,
            p.IOC_PATH: join(EPICS, "ioc", "master", "ND1"),
            p.IOC_APP_PATH: join(EPICS, "ioc", "master", "ND1", "ND1App"),
            p.OPI_FILE_NAME: "new_device_1",
            p.OPI_KEY: "ND1",
            p.YEAR: get_year(),
        }

        for key, value in expected_substitutions.items():
            self.assertEqual(
                self.device[key],
                value,
                msg=f"Values for key '{key}' are incosistent.",
            )

    def test_invalid_name_raises_error(self) -> None:
        """Test argument validations."""
        with self.assertRaises(InvalidIOCNameError):
            # Non-alphanumeric character
            DeviceInfo("ND 1", "New Device 1")

        with self.assertRaises(InvalidIOCNameError):
            # Too many characters
            DeviceInfo("ND1234567", "New Device 1")

        with self.assertRaises(InvalidDeviceNameError):
            # Non-ascii character
            DeviceInfo("ND1", "New Device Â")
