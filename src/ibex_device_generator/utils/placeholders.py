"""Placeholders within the template files, file and directory names.

List of all the possible placeholders in the template files.
All of these keys should be present in the device info substitutions.
"""

IOC_NAME = "ioc"
""" IOC name as the user entered it. Validity checks are run """

DEVICE_NAME = "device_name"
""" Can be longer and may contain spoaces and any ascii characters."""

DEVICE_SUPPORT_MODULE_NAME = "device_"
""" Device support module name in EPICS/support/... """

DEVICE_DATABASE_NAME = "device_database_name"
""" The device support module's deffault db file's name """

DEVICE_PROTOCOL_NAME = "device_protocol_name"
""" The device support module's deffault proto file's name """

# Lewis
LEWIS_DEVICE_NAME = "lewis_device_name"
""" Used for naming the lewis device folder """

LEWIS_DEVICE_CLASS_NAME = "lewis_emulator_device_class_name"
""" Used for naming python classes related to lewis device """

SUPPORT_PATH = "support_path"
SUPPORT_MASTER_PATH = "support_master_path"

YEAR = "year"
""" For files that require current year """

GITHUB_REPO_NAME = "github_repo_name"
""" GitHub repository name """

DEVICE_COUNT = "device_count"

# ioc/master
IOC_PATH = "ioc_path"
""" The path to the ioc usually: EPICS/ioc/master/<ioc> """

IOC_APP_PATH = "ioc_app_path"
""" The path to the ioc app directory usually:
EPICS/ioc/master/<ioc>/<ioc>App """

# gui
OPI_FILE_NAME = "opi_file_name"
OPI_KEY = "opi_key"
