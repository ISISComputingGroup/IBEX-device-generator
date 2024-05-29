import logging
import subprocess
from os import devnull


def run_command(command, working_dir):
    """
    Runs a command using subprocess. Waits for completion

    Args:
        command: A list defining the command to run
        working_dir: The directory to run the command in
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
    cmd.wait()
