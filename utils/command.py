"""Execute commands in the terminal programatically."""

import logging
import subprocess
from os import PathLike, devnull
from typing import Sequence, TypeAlias

StrOrBytesPath: TypeAlias = str | bytes | PathLike[str] | PathLike[bytes]


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
