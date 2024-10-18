"""Utilities for interacting with the file system."""

import logging
from os.path import join


def _add_entry_to_list(
    text: list[str], list_name: str, entry: str
) -> list[str]:
    """Add entry to prefixed list in list of strings.

    Check if 'list_name += entry' already exists in text and add it if not.

    Args:
        text: The original text
        list_name: The name of the list to add to
        entry: The entry to add to the list

    Returns:
        The original text with the requested entry added to the named list

    """
    new_text = []
    last_line = ""
    marker = "{} += ".format(list_name)

    new_line = marker + entry + "\n"
    # Go to the end of the list of IOCDIRS/SUPPDIRS += iocname,
    # and add our new IOC
    for line in text:
        if entry in line:
            # Entry already in the list
            return text
        elif marker in last_line and marker not in line:
            # We found the end of the list
            new_text.append(new_line)
        # Copy rest of the lines into new text as usual
        new_text.append(line)
        last_line = line
    return new_text  # return Makefile with new entry


def add_to_makefile_list(directory: str, list_name: str, entry: str) -> bool:
    """Add entry to prefixed list in a Makefile.

    Adds an entry to a list in a makefile. Finds the last line of the form
    "list_name += ..." and puts a new line containing the entry after it

    Args:
        directory: Directory containing the makefile
        list_name: The name of the list in the makefile to append to
        entry: The entry to add to the list

    """
    logging.info(
        "Adding {} to list {} in Makefile for directory {}".format(
            entry, list_name, directory
        )
    )
    makefile = join(directory, "Makefile")
    with open(makefile) as f:
        old_lines = f.readlines()

    new_lines = _add_entry_to_list(old_lines, list_name, entry)

    if old_lines == new_lines:
        logging.warn(
            (
                f"Entry '{entry}' is already added to list '{list_name}' in"
                f" '{makefile}'."
            )
        )
        return False

    with open(makefile, "w") as f:
        f.writelines(new_lines)

    return True
