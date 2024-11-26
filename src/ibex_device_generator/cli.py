"""Main file for command line interface."""

import logging

from rich.logging import RichHandler

from ibex_device_generator.ibex_device_generator import (
    IBEXDeviceGenerator,
)
from ibex_device_generator.utils.arg_parser import parse_arguments
from ibex_device_generator.utils.device_info import DeviceInfo


def _configure_logging(level: str = str(logging.INFO)) -> None:
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )


def main() -> None:
    """Run cli interface."""
    args = parse_arguments()

    _configure_logging(level=args.log_level)

    device = DeviceInfo(args.ioc_name, args.device_name, device_count=args.device_count)

    IBEXDeviceGenerator(
        device, args.use_git, args.github_token, args.ticket, args.interactive
    ).safe_run()


if __name__ == "__main__":
    main()
