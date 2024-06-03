"""Steps of the generator."""

import logging
import os
from os import PathLike

import ibex_device_generator.utils.placeholders as p
from ibex_device_generator.exc import CommandNotFoundError
from ibex_device_generator.paths import (
    CLIENT_SRC,
    EPICS,
    EPICS_SUPPORT,
    IOC_ROOT,
    OPI_RESOURCES,
)
from ibex_device_generator.utils.command import run_make_command_in
from ibex_device_generator.utils.device_info import DeviceInfo
from ibex_device_generator.utils.file_system import add_to_makefile_list
from ibex_device_generator.utils.git_utils import RepoWrapper
from ibex_device_generator.utils.github import github_repo_url
from ibex_device_generator.utils.gui import (
    DuplicateOPIKeyError,
    add_device_opi_to_opi_info,
)
from ibex_device_generator.utils.rich_utils import rich_print, tree_from_paths
from ibex_device_generator.utils.templates import (
    get_template,
    populate_template_dir,
)


def create_submodule(device: DeviceInfo) -> None:
    """Add a new submodule to EPICS top."""
    epics_repo = RepoWrapper(EPICS)

    epics_repo.create_submodule(
        device[p.DEVICE_SUPPORT_MODULE_NAME],
        github_repo_url(device[p.GITHUB_REPO_NAME]),
        device[p.SUPPORT_MASTER_PATH],
    )

    # Copy additional template files
    added_files = populate_template_dir(get_template("3"), EPICS, device)

    did_modify_makefile = add_to_makefile_list(
        EPICS_SUPPORT, "SUPPDIRS", device[p.DEVICE_SUPPORT_MODULE_NAME]
    )

    log_file_changes(
        added_files=added_files,
        modified_files=(
            [os.path.join(EPICS_SUPPORT, "Makefile")]
            if did_modify_makefile
            else []
        ),
    )


def create_submodule_structure(device: DeviceInfo) -> None:
    """Add basic files into support module folder."""
    added_files = populate_template_dir(get_template("4"), EPICS, device)

    # Run make
    try:
        run_make_command_in(device[p.SUPPORT_MASTER_PATH])
    except CommandNotFoundError as e:
        logging.warning(e)

    log_file_changes(added_files=added_files)


def create_ioc_from_template(device: DeviceInfo) -> None:
    """Add basic files into ioc/master's relevant directory for the device."""
    # For 1st and main IOC app
    added_files = populate_template_dir(get_template("5_1"), EPICS, device)

    # For nth IOC apps
    for i in range(2, device[p.DEVICE_COUNT] + 1):
        subs = device
        subs[p.INDEX] = "{:02d}".format(i)

        added_files.extend(
            populate_template_dir(get_template("5_2"), EPICS, subs)
        )

    # Add IOC to Makefile
    did_modify_makefile = add_to_makefile_list(
        IOC_ROOT, "IOCDIRS", device[p.IOC_NAME]
    )
    modified_files = (
        [os.path.join(IOC_ROOT, "Makefile")] if did_modify_makefile else []
    )

    # Run make
    try:
        run_make_command_in(device[p.IOC_PATH])
    except CommandNotFoundError as e:
        logging.warning(e)

    log_file_changes(
        added_files=added_files,
        modified_files=modified_files,
    )


def add_test_framework(device: DeviceInfo) -> None:
    """Add files for testing device in support directory."""
    added_files = populate_template_dir(get_template("6"), EPICS, device)
    log_file_changes(added_files=added_files)


def add_lewis_emulator(device: DeviceInfo) -> None:
    """Add lewis emulator files in support directory."""
    added_files = populate_template_dir(get_template("7"), EPICS, device)
    log_file_changes(added_files=added_files)


def add_opi_to_gui(device: DeviceInfo) -> None:
    """Add basic OPI with device key and add this into opi_info.xml."""
    added_files = populate_template_dir(get_template("8"), CLIENT_SRC, device)

    try:
        add_device_opi_to_opi_info(device)
        modified_files = [os.path.join(OPI_RESOURCES, "opi_info.xml")]
    except DuplicateOPIKeyError:
        modified_files = []

    log_file_changes(added_files=added_files, modified_files=modified_files)


def log_file_changes(
    added_files: list[PathLike] = [],
    modified_files: list[PathLike] = [],
    removed_files: list[PathLike] = [],
) -> None:
    """Print file trees to the user."""
    if added_files:
        logging.info(
            "[green]Added the following files:\n"
            + rich_print(
                tree_from_paths(sorted(added_files, key=str.lower)),
            ),
            extra={"markup": True},
        )
    if modified_files:
        logging.info(
            "[yellow]Modified the following files:\n"
            + rich_print(
                tree_from_paths(sorted(modified_files, key=str.lower)),
            ),
            extra={"markup": True},
        )
    if removed_files:
        logging.info(
            "[red]Removed the following files:\n"
            + rich_print(
                tree_from_paths(sorted(removed_files, key=str.lower)),
            ),
            extra={"markup": True},
        )
