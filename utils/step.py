"""Steps of the generator."""

import os

import utils.placeholders as p
from paths import CLIENT_SRC, EPICS, EPICS_SUPPORT, IOC_ROOT
from utils.command import run_command
from utils.device_info import DeviceInfo
from utils.file_system import add_to_makefile_list
from utils.git_utils import RepoWrapper
from utils.github import github_repo_url
from utils.gui import add_device_opi_to_opi_info
from utils.templates import TEMPLATES, fill_template_tree


def create_submodule(device: DeviceInfo) -> None:
    """Add a new submodule to EPICS top."""
    epics_repo = RepoWrapper(EPICS)

    epics_repo.create_submodule(
        device[p.DEVICE_SUPPORT_MODULE_NAME],
        github_repo_url(device[p.GITHUB_REPO_NAME]),
        device[p.SUPPORT_MASTER_PATH],
    )

    # Copy additional template files
    fill_template_tree(
        os.path.join(TEMPLATES, "phase_add_submodule"),
        EPICS,
        device,
    )

    add_to_makefile_list(
        EPICS_SUPPORT, "SUPPDIRS", device[p.DEVICE_SUPPORT_MODULE_NAME]
    )


def create_submodule_structure(device: DeviceInfo) -> None:
    """Add basic files into support module folder."""
    fill_template_tree(
        os.path.join(TEMPLATES, "phase_add_support_submodule"),
        EPICS,
        device,
    )


def create_ioc_from_template(device: DeviceInfo) -> None:
    """Add basic files into ioc/master's relevant directory for the device."""
    # For 1st and main IOC app
    fill_template_tree(
        os.path.join(TEMPLATES, "phase_add_1st_ioc"),
        EPICS,
        device,
    )

    # For nth IOC apps
    for i in range(2, device[p.DEVICE_COUNT] + 1):
        subs = device
        subs["ioc_number"] = "{:02d}".format(i)

        fill_template_tree(
            os.path.join(TEMPLATES, "phase_add_nth_ioc"), EPICS, subs
        )

    # Add IOC to Makefile
    add_to_makefile_list(IOC_ROOT, "IOCDIRS", device[p.IOC_NAME])

    # Run make
    run_command(["make"], device[p.IOC_PATH])


def add_test_framework(device: DeviceInfo) -> None:
    """Add files for testing device in support directory."""
    fill_template_tree(
        os.path.join(TEMPLATES, "phase_add_test_framework"),
        EPICS,
        device,
    )


def add_lewis_emulator(device: DeviceInfo) -> None:
    """Add lewis emulator files in support directory."""
    fill_template_tree(
        os.path.join(TEMPLATES, "phase_add_lewis_emulator"),
        EPICS,
        device,
    )


def add_opi_to_gui(device: DeviceInfo) -> None:
    """Add basic OPI with device key and add this into opi_info.xml."""
    fill_template_tree(
        os.path.join(TEMPLATES, "phase_add_opi_to_gui"),
        CLIENT_SRC,
        device,
    )

    add_device_opi_to_opi_info(device)
