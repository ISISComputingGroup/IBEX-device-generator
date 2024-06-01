"""Main file."""

import logging

from rich.prompt import Confirm

from ibex_device_generator.paths import CLIENT, EPICS, IOC_ROOT
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
        interactive: bool = True,
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
        self.interactive = interactive
        self.retry = retry

    def safe_run(self) -> None:
        """."""
        try:
            self.run()
        except Exception:
            logging.error("The last step has failed.")

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
            IOC_ROOT,
            "Add template IOC",
            create_ioc_from_template,
            self.device,
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

        self.add_step(
            CLIENT,
            "Add OPI to gui",
            add_opi_to_gui,
            self.device,
        )

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
        if self.interactive and not Confirm.ask(
            f"Do '{commit_msg}'?", default="y"
        ):
            logging.debug(
                ":right_arrow:  Skipping step.", extra={"markup": True}
            )
            return

        try:
            if self.use_git and repo_path and commit_msg:
                logging.info(f"Running '{commit_msg}' with git...")
                with commit_changes(repo_path, self.ticket_branch, commit_msg):
                    action(*args, **kwargs)
            else:
                logging.info(f"Running '{commit_msg}'...")
                action(*args, **kwargs)

            logging.info(
                ":white_check_mark: [bold green]Successfully executed step.",
                extra={"markup": True},
            )

        except Exception as e:
            logging.error(
                f"[red]{e}",
                extra={"markup": True},
            )

            if self.interactive and self.retry:
                logging.info("Retrying...")
                self.add_step(repo_path, commit_msg, action, *args, **kwargs)
            else:
                raise Exception("Failed.")
