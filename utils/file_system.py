"""Utilities for interacting with the file system"""

import logging
from os.path import join


def _add_entry_to_list(text, list_name, entry):
    """
    Check if IOC name has already been added to support/Makefile or ioc/master/Makefile,
    and add it at the end of IOC | SUPP DIRS list if it isn't there already.

    Args:
        text: The original text
        list_name: The name of the list to add to
        entry: The entry to add to the list

    Returns: The original text with the requested entry added to the named list

    """
    new_text = []
    last_line = ""
    marker = "{} += ".format(list_name)

    new_line = marker + entry + "\n"
    # Go to the end of the list of IOCDIRS/SUPPDIRS += iocname, and add our new IOC
    for line in text:
        if entry in line:
            # Entry already in the list
            logging.warn("IOC name already added to {}".format(list_name))
            return text
        elif marker in last_line and marker not in line:
            # We found the end of the list
            new_text.append(new_line)
        # Copy rest of the lines into new text as usual
        new_text.append(line)
        last_line = line
    return new_text  # return Makefile with new entry


def add_to_makefile_list(directory, list_name, entry):
    """
    Adds an entry to a list in a makefile. Finds the last line of the form "list_name += ..." and puts a new line
    containing the entry after it

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

    with open(makefile, "w") as f:
        f.writelines(_add_entry_to_list(old_lines, list_name, entry))
