import datetime
from os.path import join
from typing import Any

from paths import EPICS, EPICS_SUPPORT
from utils.placeholders import (
    DEVICE_COUNT,
    DEVICE_DATABASE_NAME,
    DEVICE_NAME,
    DEVICE_PROTOCOL_NAME,
    DEVICE_SUPPORT_MODULE_NAME,
    GITHUB_REPO_NAME,
    IOC_APP_PATH,
    IOC_NAME,
    IOC_PATH,
    LEWIS_DEVICE_CLASS_NAME,
    LEWIS_DEVICE_NAME,
    OPI_FILE_NAME,
    OPI_KEY,
    SUPPORT_MASTER_PATH,
    SUPPORT_PATH,
    YEAR,
)


class InvalidIOCNameError(Exception):
    "Raised when IOC name is invalid."

    pass


class InvalidDeviceNameError(Exception):
    "Raised when Device name is invalid."

    pass


class InvalidIOCCountError(Exception):
    "Raised when IOC count is invalid."

    pass


class DeviceInfo(dict):
    """
    Generates info used in setting up a device under IBEX based on the name
    """

    def __init__(self, ioc_name: str, device_name: str, device_count: int = 1):
        """
        Args:
            ioc_name: The name of the IOC
                (Must be between 1 and 8 alphanumeric characters)
            device_name: The longer, more descriptive name of the device.

        Raises:
            InvalidIOCNameError: if IOC name is invalid.
            InvalidDeviceNameError: if device name is invalid
            InvalidIOCCountError: if device count is invalid
        """
        if not is_valid_ioc_name(ioc_name):
            raise InvalidIOCNameError()

        if not is_valid_device_name(device_name):
            raise InvalidDeviceNameError()

        if not is_valid_device_count(device_count):
            raise InvalidIOCCountError()

        device_name_lower_underscores = device_name.lower().replace(" ", "_")

        # Set up the substitutions according to the device's details

        # fmt: off
        self[IOC_NAME]                      = ioc_name # noqa
        self[DEVICE_NAME]                   = device_name # noqa
        self[DEVICE_COUNT]                  = device_count # noqa
        self[DEVICE_SUPPORT_MODULE_NAME]    = device_name_lower_underscores # noqa
        self[LEWIS_DEVICE_NAME]             = device_name_lower_underscores # noqa
        self[LEWIS_DEVICE_CLASS_NAME]       = device_name.title().replace(" ", "") # noqa
        self[DEVICE_DATABASE_NAME]          = device_name_lower_underscores # noqa
        self[DEVICE_PROTOCOL_NAME]          = device_name_lower_underscores # noqa
        self[SUPPORT_PATH]                  = join(EPICS_SUPPORT, device_name_lower_underscores) # noqa
        self[SUPPORT_MASTER_PATH]           = join(EPICS_SUPPORT, device_name_lower_underscores, "master") # noqa
        self[GITHUB_REPO_NAME]              = f"EPICS-{device_name.replace(' ', '_')}" # noqa
        self[IOC_PATH]                      = join(EPICS, "ioc", "master", ioc_name) # noqa
        self[IOC_APP_PATH]                  = join(EPICS, "ioc", "master", ioc_name, f"{ioc_name}App") # noqa
        self[OPI_FILE_NAME]                 = device_name_lower_underscores # noqa
        self[OPI_KEY]                       = ioc_name # noqa
        self[YEAR]                          = get_year() # noqa
        # fmt: on

    def __setitem__(self, key: Any, value: Any):
        if self.get(key):
            # Prevent modifying values
            raise Exception(
                "Attempting to modify value in device info dictionary"
            )
        else:
            super().__setitem__(key, value)

    @property
    def github_repo_url(self):
        return f"https://github.com/ISISComputingGroup/{self[GITHUB_REPO_NAME]}.git"

    def ioc_indexed_name(self, index: int) -> str:
        """
        Args:
            index: The index of the application

        Returns: The name of the application name for the given index
            "${ioc_name}-IOC-${ioc_index}" e.g. ABC-IOC-01
        """
        if not 0 < index < 100:
            raise InvalidIOCCountError()

        return "{}-IOC-{:02d}".format(self._ioc_name, index)

    def ioc_boot_path(self, index: int):
        """
        Args:
            index: The index of the application

        Returns: The path to the boot folder for ioc application
            at the given index
        """
        return join(
            self[IOC_PATH],
            "iocBoot",
            self.ioc_indexed_name(index),
        )

    def ioc_app_path(self, index: int) -> str:
        """
        Returns:
        """
        return join(
            self[IOC_PATH], f"{self.ioc_indexed_name(index)}App"
        )


def get_year() -> str:
    """
    Get the current year.
    Returns:
         str:  The current year formatted as a string
    """
    return str(datetime.datetime.now().year)


# Validation


def is_valid_ioc_name(name: str) -> bool:
    """
    Args:
        name: Name to check for validity

    Returns: True is name valid, else False
    """
    return name.isalnum() and name.upper() == name and 1 <= len(name) <= 8


def is_valid_device_name(name: str) -> bool:
    """
    Args:
        name: Name to check for validity

    Returns: True is name valid, else False
    """
    return name.isascii()


def is_valid_device_count(count: int) -> bool:
    """
    Args:
        count: Number of device IOCs

    Returns: True is device count is valid, else False
    """
    return 0 < count < 100
