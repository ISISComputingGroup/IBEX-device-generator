"""Main file for command line interface."""

from ibex_device_generator.generate import (
    IBEXDeviceGenerator,
    _configure_logging,
)
from ibex_device_generator.utils.arg_parser import parse_arguments
from ibex_device_generator.utils.device_info import DeviceInfo


def main() -> None:
    """Run cli interface."""
    args = parse_arguments()

    _configure_logging(level=args.log_level)

    device = DeviceInfo(
        args.ioc_name, args.device_name, device_count=args.device_count
    )

    IBEXDeviceGenerator(
        device, args.use_git, args.github_token, args.ticket
    ).run()


if __name__ == "__main__":
    main()
