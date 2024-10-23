# ruff: noqa: ANN201, D100, D101, D102

import os
from tempfile import TemporaryDirectory
from unittest import TestCase

from git import Repo
from ibex_device_generator.exc import (
    CannotOpenRepoError,
    FailedToSwitchBranchError,
)
from ibex_device_generator.utils.git_utils import RepoWrapper, commit_changes


class GitUtilTests(TestCase):
    def test_repo_can_init_in_git_directory(self):
        with TemporaryDirectory() as tmpdir:
            Repo.init(tmpdir)
            try:
                RepoWrapper(tmpdir)
            except CannotOpenRepoError:
                self.fail(("Repo should be able to initialise in a git tracked" " directory."))

    def test_repo_fails_to_init_in_non_git_directory(self):
        with TemporaryDirectory() as tmpdir:
            with self.assertRaises(CannotOpenRepoError):
                RepoWrapper(tmpdir)

    def test_fails_to_commit_changes_on_branch_if_repo_is_dirty(self):
        with TemporaryDirectory() as tmpdir:
            RepoWrapper(tmpdir, init=True)
            # Make repo dirty by adding a file and not committing it
            with open(os.path.join(tmpdir, "README.md"), "w") as f:
                f.write("You were my brother Anakin.")

            with self.assertRaises(FailedToSwitchBranchError):
                with commit_changes(tmpdir, "mustafa", "Commit message"):
                    pass
