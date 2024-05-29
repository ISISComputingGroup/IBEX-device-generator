"""Standard system paths used in the IBEX distribution"""

from os import getenv
from os.path import abspath, dirname, join

INSTRUMENT = join("C:\\", "Instrument")
EPICS = getenv("EPICS_KIT_ROOT", join(INSTRUMENT, "Apps", "EPICS"))

IOC_ROOT = join(EPICS, "IOC", "master")
PERL = join("C:\\", "Strawberry", "perl", "bin", "perl.exe")
EPICS_BASE_BUILD = join(EPICS, "base", "master", "bin")
ARCHITECTURE = getenv("EPICS_HOST_ARCH", "windows-x64")
PERL_IOC_GENERATOR = join(EPICS_BASE_BUILD, ARCHITECTURE, "makeBaseApp.pl")

EPICS_SUPPORT = join(EPICS, "support")

CLIENT = join(INSTRUMENT, "Dev", "ibex_gui")
CLIENT_SRC = join(CLIENT, "base")
OPI_RESOURCES = join(CLIENT_SRC, "uk.ac.stfc.isis.ibex.opis", "resources")

PERL_SUPPORT_GENERATOR = join(
    EPICS_SUPPORT, "asyn", "master", "bin", ARCHITECTURE, "makeSupport.pl"
)

PROJECT_ROOT = join(dirname(abspath(__file__)))
TEMPLATES = join(PROJECT_ROOT, "templates")
