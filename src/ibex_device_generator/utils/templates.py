"""Template handling."""

import logging
import os
import posixpath
from importlib.resources import files
from importlib.resources.abc import Traversable
from os import PathLike
from string import Template

from ibex_device_generator.utils.device_info import DeviceInfo


class DeviceTemplate(Template):
    """Template with custom delimiter '@' for templates of IBEX devices."""

    delimiter = "@"

    def apply(self, device: DeviceInfo) -> str:
        """Apply device substitutions to a template."""
        return self.substitute(device)


# __pycache__ folders get added to template directories when this package is
# installed through pip
ignore_dirs = {"__pycache__"}


def get_template(*pathsegments: str) -> Traversable:
    """Get a resource located in ibex_device_generator.templates.

    Args:
        *pathsegments: Segments as subdirectories within the
            `templates/` directory. If called without any arguments, it returns
            the reference to the `templates/` directory.

    Returns:
        `importlib.resources.abc.Traversable` representing the template
        directory/file

    """
    descendants = posixpath.sep.join(pathsegments)
    item = files("ibex_device_generator.templates").joinpath(descendants)

    if item.is_file() or item.is_dir():
        return item
    else:
        raise ValueError(f"Template does not exist at '{item}'")


def populate_template_file(
    template: Traversable, into: PathLike, substitutions: dict[str, str]
) -> PathLike:
    """Populate a single template file into a directory on the disk.

    Args:
        template: the template that is a Traversable representing a file
        into: the destination into which resulting file is put
        substitutions: the map of substitutions in the form of
            {key: substitution}

    Returns:
        The path to the new file made from the template.

    Raises:
        ValueError: if the template is not a file.

    """
    if not template.is_file():
        raise ValueError(f"Template at '{template}' is not a file.")

    substituted_destination = os.path.join(
        into, DeviceTemplate(template.name).substitute(substitutions)
    )

    logging.debug(
        (
            f"Using template file '{template}'\n"
            f"to populate '{substituted_destination}'"
        )
    )

    os.makedirs(os.path.dirname(substituted_destination), exist_ok=True)

    with open(substituted_destination, "w") as file:
        substituted_content = DeviceTemplate(template.read_text()).substitute(
            substitutions
        )

        file.write(substituted_content)
    return substituted_destination


def populate_template_dir(
    template: Traversable, into: PathLike, substitutions: dict[str, str]
) -> list[PathLike]:
    """Populate a template directory into a location on the disk.

    This only creates folders that contain at least one file.

    Args:
        template: the template that is a Traversable representing either
            a directory or a single file.
        into: the destination into which resulting items are put
        substitutions: The map of substitutions in the form of
            {key: substitution}

    Returns:
        A list of paths to the new files made from the template.

    """
    if not template.is_dir():
        raise ValueError(f"Template at '{template}' is not a directory.")

    files = []

    if template.name in ignore_dirs:
        logging.debug(
            f"[yellow]Ignoring template directory '{template}'",
            extra={"markup": True},
        )
        return files

    for item in template.iterdir():
        if item.is_file():
            files.append(populate_template_file(item, into, substitutions))

        if item.is_dir():
            substituted_destination = os.path.join(
                into, DeviceTemplate(item.name).substitute(substitutions)
            )
            files.extend(
                populate_template_dir(
                    item, substituted_destination, substitutions
                )
            )
    return files
