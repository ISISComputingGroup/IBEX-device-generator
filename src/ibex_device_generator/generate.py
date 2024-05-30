"""Main file."""

import logging

from rich.logging import RichHandler
from rich.prompt import Confirm

from ibex_device_generator.paths import CLIENT, EPICS, IOC_ROOT
from ibex_device_generator.utils.arg_parser import parse_arguments
from ibex_device_generator.utils.device_info import DeviceInfo
from ibex_device_generator.utils.git_utils import commit_changes
from ibex_device_generator.utils.github import (
    create_github_repository,
    grant_permissions_for_github_repository,
)
from ibex_device_generator.utils.placeholders import (
    DEVICE_NAME,
    SUPPORT_MASTER_PATH,
)
from ibex_device_generator.utils.step import (
    add_lewis_emulator,
    add_opi_to_gui,
    add_test_framework,
    create_ioc_from_template,
    create_submodule,
    create_submodule_structure,
)


class IBEXDeviceGenerator:
    """IBEX device generator."""

    def __init__(
        self,
        device: DeviceInfo,
        use_git: bool,
        github_token: str,
        ticket_num: int,
        retry: bool = True,
    ) -> None:
        """Create a device generator instance."""
        device_name_underscores = device[DEVICE_NAME].replace(" ", "_")
        ticket_branch = f"Ticket{ticket_num}_Add_IOC_{device_name_underscores}"

        self.device = device
        self.use_git = use_git
        self.github_token = github_token
        self.ticket_num = ticket_num
        self.ticket_branch = ticket_branch
        self.retry = retry

    def run(self) -> None:
        """Run the generator."""
        # Generator steps below

        self.add_step(
            None,
            "Create GitHub repository",
            create_github_repository,
            self.device,
            self.github_token,
        )

        self.add_step(
            None,
            "Grant permissions for GitHub repository",
            grant_permissions_for_github_repository,
            self.device,
            self.github_token,
        )

        self.add_step(
            EPICS,
            "Add support submodule to EPICS",
            create_submodule,
            self.device,
        )

        self.add_step(
            self.device[SUPPORT_MASTER_PATH],
            "Add template file structure in support submodule",
            create_submodule_structure,
            self.device,
        )

        self.add_step(
            IOC_ROOT, "Add template IOC", create_ioc_from_template, self.device
        )

        self.add_step(
            self.device[SUPPORT_MASTER_PATH],
            "Add device to test framework",
            add_test_framework,
            self.device,
        )

        self.add_step(
            self.device[SUPPORT_MASTER_PATH],
            "Add Lewis emulator",
            add_lewis_emulator,
            self.device,
        )

        self.add_step(CLIENT, "Add OPI to gui", add_opi_to_gui, self.device)

    def add_step(
        self,
        repo_path: str,
        commit_msg: str,
        action: callable,
        *args,
        **kwargs,
    ) -> None:
        """Add a generator step.

        Each step asks the user before running. This also takes care of
        commiting if use git is specified.

        Args:
            repo_path: path to the repository being modified by this step.
            commit_msg: the commit message
            action: the function to execute as this step
            *args: any positional arguments for the action
            **kwargs: any keywoprd arguments for the action

        """
        if not Confirm.ask(f"Do '{commit_msg}'?", default="y"):
            logging.info(
                ":right_arrow:  Skipping step.", extra={"markup": True}
            )
            return

        try:
            if self.use_git and repo_path and commit_msg:
                with commit_changes(repo_path, self.ticket_branch, commit_msg):
                    action(*args, **kwargs)
            else:
                action(*args, **kwargs)

            logging.info(
                ":white_check_mark: [bold green]Successfully executed step.",
                extra={"markup": True},
            )

        except Exception as e:
            logging.error(
                ":red_square: Encountered an error: {}".format(e),
                extra={"markup": True},
            )
            if self.retry:
                logging.info("Retrying...")
                self.add_step(repo_path, commit_msg, action, *args, **kwargs)


def _configure_logging(level: str = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )


if __name__ == "__main__":
    args = parse_arguments()

    _configure_logging(level=args.log_level)

    device = DeviceInfo(
        args.ioc_name, args.device_name, device_count=args.device_count
    )

    IBEXDeviceGenerator(
        device, args.use_git, args.github_token, args.ticket
    ).run()
