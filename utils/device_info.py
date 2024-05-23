""" Helper to generate information about the device based on the name used in device setup """
import datetime
from os.path import join

from paths import EPICS, EPICS_SUPPORT
from utils.substitution_keys import DEVICE_COUNT, DEVICE_DATABASE_NAME, DEVICE_NAME, DEVICE_PROTOCOL_NAME, DEVICE_SUPPORT_MODULE_NAME, GITHUB_REPO_NAME, IOC_APP_PATH, IOC_NAME, IOC_PATH, LEWIS_DEVICE_CLASS_NAME, LEWIS_DEVICE_NAME, OPI_FILE_NAME, OPI_KEY, SUPPORT_MASTER_PATH, SUPPORT_PATH, YEAR


class InvalidIOCNameError(Exception):
    "Raised when IOC name is invalid."
    pass

class InvalidDeviceNameError(Exception):
    "Raised when Device name is invalid."
    pass

class InvalidIOCCountError(Exception):
    "Raised when IOC count is invalid."
    pass

class DeviceInfo:
    """"
    Generates info used in setting up a device under IBEX based on the name
    """

    def __init__(self, ioc_name: str, device_name: str, device_count: int=1):
        """
        Args:
            ioc_name: The name of the IOC (Must be between 1 and 8 alphanumeric characters)
            device_name: The longer, more descriptive name of the device.

        Raises:
            InvalidIOCNameError: if IOC name is invalid.
        """
        if not is_valid_ioc_name(ioc_name):
            raise InvalidIOCNameError()
        
        if not is_valid_device_name(device_name):
            raise InvalidDeviceNameError()
        
        if not is_valid_device_count(device_count):
            raise InvalidIOCCountError()
        
        # Basic info
        self._ioc_name = ioc_name
        self._device_name = device_name
        self._device_name_lower_underscores = device_name.lower().replace(" ", "_")

        # For EPICS/ioc/master
        self._ioc_path = join(EPICS, "ioc", "master", self._ioc_name)

        # For EPICS/support/<device>/master
        self._support_name = device_name.lower().replace(" ", "_")
        self._support_path = join(EPICS_SUPPORT, self._support_name)
        self._support_master_path = join(self._support_path, "master")

        # For lewis emulator code
        self._lewis_device_class_name = device_name.title().replace(" ", "")

        self._device_count = device_count

        #TODO add repo name

        self._substitutions = {
            IOC_NAME:                   ioc_name,
            DEVICE_NAME:                device_name,
            DEVICE_SUPPORT_MODULE_NAME: self._device_name_lower_underscores,
            LEWIS_DEVICE_NAME:          self._device_name_lower_underscores,
            DEVICE_DATABASE_NAME:       self._device_name_lower_underscores,
            DEVICE_PROTOCOL_NAME:       self._device_name_lower_underscores,
            LEWIS_DEVICE_CLASS_NAME:    device_name.title().replace(" ", ""),
            SUPPORT_PATH:               join(EPICS_SUPPORT, self.device_name_lower_underscores),
            SUPPORT_MASTER_PATH:        join(EPICS_SUPPORT, self.device_name_lower_underscores, "master"),
            GITHUB_REPO_NAME:           f"EPICS-{device_name.replace(' ', '_')}",
            DEVICE_COUNT:               device_count,
            IOC_PATH:                   join(EPICS, "ioc", "master", ioc_name),
            IOC_APP_PATH:               join(EPICS, "ioc", "master", ioc_name, f"{ioc_name}App"),
            OPI_FILE_NAME:              self._device_name_lower_underscores,
            OPI_KEY:                    ioc_name,
            YEAR:                       get_year()
        }

    @property
    def device_name_lower_underscores(self):
        return self._device_name.lower().replace(" ", "_")
    
    @property
    def support_name(self):
        return self._support_name
    
    @property
    def support_path(self):
        return self._support_path
    
    @property
    def support_master_path(self):
        return self._support_master_path
    
    @property
    def github_repo_url(self):
        return f"https://github.com/ISISComputingGroup/{self.substitutions[GITHUB_REPO_NAME]}.git"
    
    
    @property
    def substitutions(self):
        """
        Returns: The name of the IOC based on the input name. Must be between 1 and 8 characters
        """
        return self._substitutions

    @property
    def ioc_name(self):
        """
        Returns: The name of the device that can be different to the IOC name.
        """
        return self._ioc_name
    
    @property
    def device_name(self):
        """
        Returns: The name of the device that can be different to the IOC name.
        """
        return self._device_name
    
    def ioc_indexed_name(self, index: int) -> str:
        """
        Args:
            index: The IOC application name for the given index

        Returns: The name of the application "${ioc_name}-IOC-${ioc_index}" e.g. ABC-IOC-01
        """
        if not 0 < index < 100:
            raise InvalidIOCCountError()
        
        return "{}-IOC-{:02d}".format(self._ioc_name, index)
    
    def ioc_boot_path(self, index: int):
        """
        Returns: 
        """
        return join(self.substitutions[IOC_PATH], "iocBoot", self.ioc_indexed_name(index))

    def ioc_app_path(self, index: int) -> str:
        """
        Returns: 
        """
        return join(self.substitutions[IOC_PATH], f"{self.ioc_indexed_name(index)}App")

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