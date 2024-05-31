"""Template handling."""

import logging
import os
from string import Template

from ibex_device_generator.utils.device_info import DeviceInfo


class DeviceTemplate(Template):
    """Template with custom delimiter '@' for templates of IBEX devices."""

    delimiter = "@"

    def apply(self, device: DeviceInfo) -> str:
        """Apply device substitutions to a template."""
        return self.substitute(device)


# __pycache__ folders get added when this package is installed through pip
ignore_folders = {"__pycache__"}


def fill_template_file(
    template: str, destination: str, substitutions: dict[str, str]
) -> None:
    """Create a new file based on a template and substitutions.

    Take template file at location and write it out to destination
    with the substitutions

    Args:
        template: template file path
        destination: where to put new file
        substitutions: substitutions for the template file's content

    Raises:
        KeyError if placeholders are missing from mapping

    """
    logging.debug(
        (
            f"Using template at '{template}' with substitutions"
            f" ({substitutions}) to populate '{destination}'"
        )
    )

    # Make directories along the path to the file
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    # Read template
    with open(template, "r") as template_file:
        src = DeviceTemplate(template_file.read())
        result = src.substitute(substitutions)
        # Write substituted file out to destination
        with open(destination, "w") as destination_file:
            destination_file.write(result)


def fill_template_tree(
    src: str, dst: str, substitutions: dict[str, str]
) -> str:
    """Recursively create new files based on a template directory.

    Copies the template files located in src directory recursively into
    the destination directory dst substituting all placeholders within
    directory names and file contents.

    Args:
        src: Root directory of template files
        dst: Destination root directory
        substitutions: The map of substitutions in the form of
            {key: substitution}

    Returns:
        List of absolute file paths that were written out.

    """
    logging.debug(
        (
            f"Using templates in directory '{src}' with substitutions"
            f" ({substitutions}) to populate '{dst}'"
        )
    )

    result_files = []

    for item in os.listdir(src):
        if item in ignore_folders:
            logging.debug(
                (f"Ignoring '{item}' in '{src}' while substituting templates.")
            )
            continue

        # Source
        s = os.path.join(src, item)
        # Substituted destination
        d = DeviceTemplate(os.path.join(dst, item)).substitute(substitutions)

        if os.path.isdir(s):
            os.makedirs(d, exist_ok=True)
            files = fill_template_tree(s, d, substitutions)
            result_files.extend(files)
        else:
            fill_template_file(s, d, substitutions)
            result_files.append(d)

    return result_files
