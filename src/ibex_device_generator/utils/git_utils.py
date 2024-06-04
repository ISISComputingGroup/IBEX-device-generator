"""Utilities for interacting with Git.

This is sometimes done via the command line and other times the PythonGit API.
"""

import logging
import os
import subprocess
from contextlib import contextmanager
from os.path import relpath
from typing import Generator

from git import (
    GitCommandError,
    InvalidGitRepositoryError,
    NoSuchPathError,
    Repo,
)

from ibex_device_generator.exc import (
    CannotOpenRepoError,
    FailedToSwitchBranchError,
    NothingToCommitError,
)


class RepoWrapper(Repo):
    """A wrapper around a git repository."""

    def __init__(
        self,
        path: str,
        init: bool = False,
        *args,
        **kwargs,
    ) -> None:
        """Attach to existing git repository or initialise a new.

        Args:
            path: The path to the git repository
            origin: The url to repo's remote origin. During initialisation if
                this does not equal the repo's remote origin a
                WrongRepositoryOriginError is raised.
                When a new repository is initialised this is used to set up
                remote origin.
            init: If True git repo is initialised at directory if it
                doesn't exist.
            *args: any additional positional arguments
            **kwargs: any additional keyword arguments

        """
        try:
            super().__init__(path, *args, **kwargs)
        except (InvalidGitRepositoryError, NoSuchPathError):
            # This might be overkill for our use case but here we go
            if init:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                self.init(path, initial_branch="main")
                super().__init__(path, *args, **kwargs)
            else:
                raise CannotOpenRepoError(path)

    @property
    def active_branch_or_none(self) -> str | None:
        """Get active branch or None if HEAD is detached."""
        try:
            return str(self.active_branch)
        except TypeError:
            # HEAD is detached
            return None

    def switch(self, branch: str = "main") -> None:
        """Switch to branch. Creates it if needed.

        Args:
            branch: Name of the branch to switch to. Defaults to 'main'

        """
        try:
            logging.info(
                f"Switching to branch '{branch}' in {self.working_dir}"
            )
            if str(branch) == self.active_branch_or_none:
                logging.info(f"Already on branch '{branch}'")
                return

            if branch in self.branches:
                logging.info("Branch exists, switching to it")
                self.git.checkout(branch)
            else:
                logging.info("Branch does not exist, making new branch")
                self.git.checkout("-b", branch)

        except GitCommandError as e:
            raise FailedToSwitchBranchError(self, branch, e)

    def commit_all(self, msg: str) -> None:
        """Commit all changes and untracked files in the repository.

        Args:
            msg: The commit message

        """
        logging.info(
            (
                f"Committing all changes and untracked files in"
                f" '{self.working_tree_dir}'."
            )
        )

        if self.is_dirty(untracked_files=True):
            self.git.add(A=True)
            self.git.commit(m=msg)
            sha = self.head.object.hexsha
            logging.info(f"Commit {sha[:9]} made")
        else:
            raise NothingToCommitError(self)

    def create_submodule(self, name: str, url: str, path: str) -> None:
        """Create submodule in this repository.

        Args:
            name: Name of the submodule
            url: Url to the submodule repo
            path: Local system path to the submodule

        """
        try:
            branch = "main"
            # create path relative to current root in case path is absolute
            sub_path = relpath(path, start=self.working_tree_dir)
            # We use subprocess here because gitpython seems to add a
            # /refs/heads/ prefix to any branch you give it,
            # and this breaks the repo checks.

            cmd = (
                f"git submodule add -b {branch} --name {name} {url} {sub_path}"
            )
            subprocess.run(
                cmd,
                cwd=self.working_tree_dir,
                check=True,
            )

        except subprocess.CalledProcessError as e:
            logging.error(
                "Cannot add {} as a submodule, error: {}".format(path, e)
            )
            raise e
        except Exception as e:
            raise RuntimeError(
                (
                    f"Unknown error {e} of type {type(e)} whilst"
                    f" creating submodule in {path}"
                )
            )


@contextmanager
def commit_changes(
    repo_path: str,
    branch: str,
    msg: str,
) -> Generator[RepoWrapper, None, None]:
    """Switches to a branch and makes commit.

    Args:
        repo_path: Path to the repo
        branch: branch to commit on
        msg: commit message
        confirm_commit: prompt the user to confirm the commit

    """
    repo = RepoWrapper(repo_path)

    if repo.is_dirty(untracked_files=True):
        raise FailedToSwitchBranchError(repo, branch, "Repo is dirty.")

    try:
        active_branch = repo.active_branch
        if str(active_branch) not in ["main", "master", branch]:
            raise FailedToSwitchBranchError(
                repo,
                branch,
                (
                    "Your active branch should be main/master or the ticket"
                    f" branch but it is {repo.active_branch}"
                ),
            )
    except TypeError:
        # Head is detached

        # Treat this as ok because our way of updating submodules leaves them
        # in a detached head state. Which probably only occurs if someone just
        # updated their submodules.

        logging.warning(
            (
                f"Git HEAD is detached in {repo.working_tree_dir}."
                " Treating this as OK."
            )
        )

    repo.switch(branch)

    yield repo

    repo.commit_all(msg)
