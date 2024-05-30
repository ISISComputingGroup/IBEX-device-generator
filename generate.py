import logging

from rich.logging import RichHandler
from rich.prompt import Confirm

from paths import CLIENT, EPICS, IOC_ROOT
from utils.arg_parser import parse_arguments
from utils.device_info import DeviceInfo
from utils.git_utils import commit_changes
from utils.github_requests import (
    create_github_repository,
    grant_permissions_for_github_repository,
)
from utils.placeholders import DEVICE_NAME, SUPPORT_MASTER_PATH
from utils.step import (
    add_lewis_emulator,
    add_opi_to_gui,
    add_test_framework,
    create_ioc_from_template,
    create_submodule,
    create_submodule_structure,
)


class IBEXDeviceGenerator:
    def __init__(
        self,
        device: DeviceInfo,
        use_git: bool,
        github_token: str,
        ticket_num: int,
        retry: bool = True,
    ) -> None:
        self.device = device
        self.use_git = use_git
        self.github_token = github_token
        self.ticket_num = ticket_num
        self.ticket_branch = f"Ticket{self.ticket_num}_Add_IOC_{self.device[DEVICE_NAME].replace(' ', '_')}"
        self.retry = retry

    def run(self):
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

    def add_step(self, repo_path, commit_msg, action, *args, **kwargs):
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


def _configure_logging(level=logging.INFO):
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
