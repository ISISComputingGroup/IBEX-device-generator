import unittest

from ibex_device_generator.utils.channel_access import ChannelAccess
from ibex_device_generator.utils.ioc_launcher import get_default_ioc_dir
from ibex_device_generator.utils.test_modes import TestModes
from ibex_device_generator.utils.testing import get_running_lewis_and_ioc, skip_if_recsim


DEVICE_PREFIX = "@{ioc}_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("@{ioc}"),
        "macros": {},
        "emulator": "@{lewis_device_name}",
    },
]


TEST_MODES = [TestModes.RECSIM, TestModes.DEVSIM]


class @{lewis_emulator_device_class_name}Tests(unittest.TestCase):
    """
    Tests for the _Device_ IOC.
    """
    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("@{lewis_device_name}", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX)

    def test_that_fails(self):
        self.fail("You haven't implemented any tests!")
