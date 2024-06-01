"""Execute commands in the terminal programatically."""

import logging
import shutil
import subprocess
from os import PathLike, devnull
from typing import Sequence, TypeAlias

StrOrBytesPath: TypeAlias = str | bytes | PathLike[str] | PathLike[bytes]


class MakeCommandNotFoundError(Exception):
    """Raised when make command is not found on system."""


def run_command(
    command: StrOrBytesPath | Sequence[StrOrBytesPath], working_dir: str
) -> int:
    """Run a command using subprocess, waits for completion.

    Args:
        command: A list defining the command to run
        working_dir: The directory to run the command in

    Returns:
        The exit code after running the command

    """
    logging.info(
        "Running command {} from {}".format(" ".join(command), working_dir)
    )
    with open(devnull, "w") as null_out:
        cmd = subprocess.Popen(
            command,
            cwd=working_dir,
            stdout=null_out,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
        )
    return cmd.wait()


def run_make_command_in(
    dir: PathLike, raise_if_make_not_found: bool = False
) -> int:
    """Run make command in directory.

    By default allow this command to fail. If not called from EPICS terminal
    `make` might not be available.

    Args:
        dir: directory to run the command in
        raise_if_make_not_found: whether or not to raise
            `MakeCommandNotFoundError` if make is not available

    Returns:
        the exit code after running the command

    Raises:
        MakeCommandNotFoundError: if make is unavailable and
            `raise_if_make_not_found` flag is set to True.

    """
    make_command = "make"

    fully_qualified_executable_path = shutil.which(make_command)

    if fully_qualified_executable_path:
        return run_command(fully_qualified_executable_path, dir)
    else:
        logging.warning(
            (
                f"Failed to execute command '{make_command}' in '{dir}'."
                f"Cannot find executable for command '{make_command}'"
            )
        )
        if raise_if_make_not_found:
            raise MakeCommandNotFoundError

        return 1
