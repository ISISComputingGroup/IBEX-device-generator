"""Standard system paths used in the IBEX distribution."""

from os import getenv
from os.path import abspath, dirname, join

PROJECT_ROOT = join(dirname(abspath(__file__)))

INSTRUMENT = join("C:\\", "Instrument")
EPICS = getenv("EPICS_KIT_ROOT", join(INSTRUMENT, "Apps", "EPICS"))

IOC_ROOT = join(EPICS, "ioc", "master")
EPICS_SUPPORT = join(EPICS, "support")

CLIENT = join(INSTRUMENT, "Dev", "ibex_gui")
CLIENT_SRC = join(CLIENT, "base")
OPI_RESOURCES = join(CLIENT_SRC, "uk.ac.stfc.isis.ibex.opis", "resources")
