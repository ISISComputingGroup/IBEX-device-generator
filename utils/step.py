import os

from paths import CLIENT_SRC, EPICS, EPICS_SUPPORT, IOC_ROOT
from utils.command import run_command
from utils.device_info import DEVICE_COUNT, IOC_PATH, DeviceInfo
from utils.file_system import add_to_makefile_list
from utils.git_utils import RepoWrapper
from utils.gui import add_device_opi_to_opi_info
from utils.templates import TEMPLATES, fill_template_tree


def create_submodule(device: DeviceInfo):
    epics_repo = RepoWrapper(EPICS)

    epics_repo.create_submodule(
        device.support_name, device.github_repo_url, device.support_master_path
    )

    # Copy additional template files
    fill_template_tree(
        os.path.join(TEMPLATES, "phase_add_submodule"),
        EPICS,
        device.substitutions,
    )

    add_to_makefile_list(EPICS_SUPPORT, "SUPPDIRS", device.support_name)


def create_submodule_structure(device: DeviceInfo):
    fill_template_tree(
        os.path.join(TEMPLATES, "phase_add_support_submodule"),
        EPICS,
        device.substitutions,
    )


def create_ioc_from_template(device: DeviceInfo) -> None:
    # For 1st and main IOC app
    fill_template_tree(
        os.path.join(TEMPLATES, "phase_add_1st_ioc"),
        EPICS,
        device.substitutions,
    )

    # For nth IOC apps
    for i in range(2, device.substitutions[DEVICE_COUNT] + 1):
        subs = device.substitutions
        subs["ioc_number"] = "{:02d}".format(i)

        fill_template_tree(
            os.path.join(TEMPLATES, "phase_add_nth_ioc"), EPICS, subs
        )

    # Add IOC to Makefile
    add_to_makefile_list(IOC_ROOT, "IOCDIRS", device.ioc_name)

    # Run make
    run_command(["make"], device.substitutions[IOC_PATH])


def add_test_framework(device: DeviceInfo) -> None:
    fill_template_tree(
        os.path.join(TEMPLATES, "phase_add_test_framework"),
        EPICS,
        device.substitutions,
    )


def add_lewis_emulator(device: DeviceInfo) -> None:
    fill_template_tree(
        os.path.join(TEMPLATES, "phase_add_lewis_emulator"),
        EPICS,
        device.substitutions,
    )


def add_opi_to_gui(device: DeviceInfo) -> None:
    # TODO This step will fail to commit because the git hook changes additional files "dummy widgets". This will need to be fixed somehow

    fill_template_tree(
        os.path.join(TEMPLATES, "phase_add_opi_to_gui"),
        CLIENT_SRC,
        device.substitutions,
    )

    add_device_opi_to_opi_info(device)
