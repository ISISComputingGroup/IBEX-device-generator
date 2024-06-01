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
    GitError,
    InvalidGitRepositoryError,
    NoSuchPathError,
    Repo,
    RepositoryDirtyError,
)
from rich.prompt import Confirm


class FailedToSwitchBranchError(GitError):
    """Switching branch failed."""

    pass


class CannotOpenRepoError(GitError):
    """Thrown when GitPython cannot be initialised at path."""

    def __init__(self, path: str) -> None:  # noqa: D107
        self.path = path

    def __str__(self) -> str:  # noqa: D105
        return (
            "Cannot open git repository at %s."
            " Check if git repo exists at location." % self.path
        )


class RepoWrapper(Repo):
    """A wrapper around a git repository."""

    def __init__(
        self,
        path: str,
        init: bool = False,
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

        """
        try:
            super().__init__(path)
        except (InvalidGitRepositoryError, NoSuchPathError):
            # This might be overkill for our use case but here we go
            if init:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                self.init(path, initial_branch="main")
            else:
                raise CannotOpenRepoError(path)

    def switch(self, branch: str = "main") -> None:
        """Switch to branch. Creates it if needed.

        Args:
            branch: Name of the branch to switch to. Defaults to 'main'

        """
        try:
            logging.info(
                f"Switching to branch '{branch}' in {self.working_dir}"
            )
            if str(branch) == str(self.active_branch):
                logging.info(f"Already on branch '{branch}'")
                return

            if branch in self.branches:
                logging.info("Branch exists, switching to it")
                self.git.checkout(branch)
            else:
                logging.info("Branch does not exist, making new branch")
                self.git.checkout("-b", branch)

        except GitCommandError as e:
            raise FailedToSwitchBranchError(
                "Error whilst creating git branch, {}".format(e)
            )

    def commit_all(self, msg: str) -> None:
        """Commit all changes and untracked files in the repository.

        Args:
            msg: The commit message

        """
        logging.debug(
            (
                f"Attempting to commit all changes and untracked files in"
                f" '{self.working_tree_dir}'."
            )
        )

        try:
            self.git.add(A=True)
            self.git.commit(m=msg)
        except (OSError, GitCommandError) as e:
            raise RuntimeError(
                "Error whilst creating commit in {}: {}".format(
                    self.working_dir, e
                )
            )

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
    confirm_commit: bool = True,
) -> Generator[RepoWrapper, None, None]:
    """Switches to a branch and makes commit.

    Args:
        repo_path: Path to the repo
        branch: branch to commit on
        msg: commit message
        confirm_commit: prompt the user to confirm the commit

    """
    repo = RepoWrapper(repo_path)

    if repo.is_dirty(untracked_files=True) or (
        str(repo.active_branch) != "main"
        and str(repo.active_branch) != "master"
        and str(repo.active_branch) != branch
    ):
        raise RepositoryDirtyError(
            repo,
            (
                f"Please make sure git status is clean in"
                f"'{repo.working_tree_dir}' and that the active branch"
                f" is main/master or {branch}."
            ),
        )

    repo.switch(branch)

    yield repo

    if not confirm_commit or Confirm.ask(
        (
            f"Commit all changes and untracked files in"
            f" '{repo.working_tree_dir}'?"
        ),
        default="y",
    ):
        repo.commit_all(msg)
