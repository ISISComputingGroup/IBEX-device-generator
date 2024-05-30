import argparse
from argparse import ArgumentTypeError

from utils.device_info import (
    is_valid_device_count,
    is_valid_device_name,
    is_valid_ioc_name,
)
from utils.github import does_github_issue_exist_and_is_open


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="IBEX Device IOC Generator. Generate boilerplate code for IBEX device support.",
    )

    parser.add_argument(
        "ioc_name",
        type=ioc_name_checker,
        help="Name of the IOC. This name is used in the ioc/master submodule and PVs will use this name.",
    )
    parser.add_argument(
        "ticket",
        type=ticket_number_checker,
        help="GitHub issue 'ticket' number within our development workflow.",
    )

    parser.add_argument(
        "--device_name",
        type=device_name_checker,
        help="Name of the device, this name will be used to create suppport submodule and GitHub repository. If not specified it defaults to be the same as the IOC name.",
    )
    parser.add_argument(
        "--device_count",
        type=device_count_checker,
        help="Number of duplicate device IOCs to generate.",
        default=1,
        nargs=1,
    )
    parser.add_argument(
        "--use_git",
        action="store_true",
        help="Create/switch to ticket branches and make commits accordingly at every step. The script will abort if the git status is dirty at the respective repositories.",
    )
    parser.add_argument(
        "--github_token",
        type=str,
        help='GitHub token with "repo" scope. Use to create support repository.',
    )
    parser.add_argument(
        "--log_level",
        type=str,
        help="Logging level.",
        choices=["DEBUG", "INFO", "WARN", "ERROR"],
        default="INFO",
    )

    args = parser.parse_args()

    if not args.device_name:
        args.device_name = args.ioc_name

    return args


# Input checkers


def ioc_name_checker(ioc_name: str) -> str:
    if not is_valid_ioc_name(ioc_name):
        raise ArgumentTypeError(
            "IOC Name is invalid. Make sure IOC name is an alphanumeric string, all upper case and the length is between 1 to 8."
        )
    return ioc_name


def device_name_checker(device_name: str) -> str:
    if not is_valid_device_name(device_name):
        raise ArgumentTypeError(
            "Device name is invalid. Must consist of ASCII characters."
        )
    return device_name


def device_count_checker(val: str) -> int:
    count = int(val)
    if not is_valid_device_count(count):
        raise ArgumentTypeError("Device count must be between 0 and 100.")
    return count


def ticket_number_checker(val: str) -> int:
    ticket_number = int(val)
    if not does_github_issue_exist_and_is_open(ticket_number):
        raise ArgumentTypeError(
            f"GitHub issue {ticket_number} is closed or does not exist."
        )
    return ticket_number
