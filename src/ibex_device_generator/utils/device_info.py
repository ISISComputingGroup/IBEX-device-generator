"""Device information derived from ioc name, device name and device count."""

from os.path import join
from typing import Any

import ibex_device_generator.utils.placeholders as p
from ibex_device_generator.exc import (
    InvalidDeviceCountError,
    InvalidDeviceNameError,
    InvalidIOCNameError,
    ReassignPlaceholderError,
)
from ibex_device_generator.paths import EPICS, EPICS_SUPPORT
from ibex_device_generator.utils.date import get_year


class DeviceInfo(dict):
    """Device info is a dictionary of placeholders and substitutions.

    Device specific information is derived from IOC name, device name
    and device count.
    """

    editable_substitutions = {p.INDEX}

    def __init__(
        self, ioc_name: str, device_name: str, device_count: int = 1
    ) -> None:
        """Make a device info dictionary.

        All placeholders are derived from ioc and device name.

        Args:
            ioc_name: The name of the IOC
                (Must be between 1 and 8 alphanumeric characters)
            device_name: The longer, more descriptive name of the device.
            device_count: Number of IOCs to generate. Defaults to 1

        Raises:
            InvalidIOCNameError: if IOC name is invalid.
            InvalidDeviceNameError: if device name is invalid
            InvalidIOCCountError: if device count is invalid

        """
        if not is_valid_ioc_name(ioc_name):
            raise InvalidIOCNameError(ioc_name)

        if not is_valid_device_name(device_name):
            raise InvalidDeviceNameError(device_name)

        if not is_valid_device_count(device_count):
            raise InvalidDeviceCountError(device_count)

        device_name_lower_underscores = device_name.lower().replace(" ", "_")

        # Set up the substitutions according to the device's details

        # fmt: off
        self[p.IOC_NAME]                      = ioc_name # noqa
        self[p.DEVICE_NAME]                   = device_name # noqa
        self[p.DEVICE_COUNT]                  = device_count # noqa
        self[p.DEVICE_SUPPORT_MODULE_NAME]    = device_name_lower_underscores # noqa
        self[p.LEWIS_DEVICE_NAME]             = device_name_lower_underscores # noqa
        self[p.LEWIS_DEVICE_CLASS_NAME]       = device_name.title().replace(" ", "") # noqa
        self[p.DEVICE_DATABASE_NAME]          = device_name_lower_underscores # noqa
        self[p.DEVICE_PROTOCOL_NAME]          = device_name_lower_underscores # noqa
        self[p.SUPPORT_PATH]                  = join(EPICS_SUPPORT, device_name_lower_underscores) # noqa
        self[p.SUPPORT_MASTER_PATH]           = join(EPICS_SUPPORT, device_name_lower_underscores, "master") # noqa
        self[p.GITHUB_REPO_NAME]              = f"EPICS-{device_name.replace(' ', '_')}" # noqa
        self[p.IOC_PATH]                      = join(EPICS, "ioc", "master", ioc_name) # noqa
        self[p.IOC_APP_PATH]                  = join(EPICS, "ioc", "master", ioc_name, f"{ioc_name}App") # noqa
        self[p.OPI_FILE_NAME]                 = device_name_lower_underscores # noqa
        self[p.OPI_KEY]                       = ioc_name # noqa
        self[p.YEAR]                          = get_year() # noqa
        self[p.INDEX]                         = "01" # noqa
        # fmt: on

    def __setitem__(self, key: Any, value: Any) -> None:
        """Disable value reassignment."""
        if self.get(key) and key not in self.editable_substitutions:
            # Prevent modifying values other than INDEX
            raise ReassignPlaceholderError(key)
        else:
            super().__setitem__(key, value)

    def ioc_indexed_name(self, index: int) -> str:
        """Get IOCs indexed name.

        Args:
            index: The index of the application

        Returns:
            The name of the application name for the given index
            "${ioc_name}-IOC-${ioc_index}" e.g. ABC-IOC-01

        """
        if not 0 < index < 100:
            raise InvalidDeviceCountError(index)

        return "{}-IOC-{:02d}".format(self._ioc_name, index)

    def ioc_boot_path(self, index: int) -> str:
        """Get IOCs indexed booth path.

        Args:
            index: The index of the application

        Returns:
            The path to the boot folder for ioc application
            at the given index

        """
        return join(
            self[p.IOC_PATH],
            "iocBoot",
            self.ioc_indexed_name(index),
        )

    def ioc_app_path(self, index: int) -> str:
        """Get IOCs indexed app path.

        Args:
            index: The index of the application

        Returns:
            The path to the app folder for ioc application
            at the given index

        """
        return join(self[p.IOC_PATH], f"{self.ioc_indexed_name(index)}App")


# Validation


def is_valid_ioc_name(name: str) -> bool:
    """Verify IOC name validty.

    Args:
        name: Name to check for validity

    Returns:
        True is name valid, else False

    """
    return name.isalnum() and name.upper() == name and 1 <= len(name) <= 8


def is_valid_device_name(name: str) -> bool:
    """Verify device name validity.

    Args:
        name: Name to check for validity

    Returns:
        True is name valid, else False

    """
    return name.isascii()


def is_valid_device_count(count: int) -> bool:
    """Verify device count validity.

    Args:
        count: Number of device IOCs

    Returns:
        True is device count is valid, else False

    """
    return 0 < count < 100
