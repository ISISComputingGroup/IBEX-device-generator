"""
Utilities for interacting with Git. This is sometimes done via the command line and other times the PythonGit API.
"""
import logging
import os
import subprocess
from contextlib import contextmanager
from os.path import relpath

from git import (GitCommandError, InvalidGitRepositoryError, NoSuchPathError,
                 Repo)
from rich.prompt import Confirm


class DirtyRepositoryError(Exception):
    "Raised when git repository is dirty."
    pass

def use_git_conditionally(use_git: bool, repo_path: str, branch: str, commit_msg: str, action: callable, *args, **kwargs):
    if use_git:
        with commit_changes(repo_path, branch, commit_msg):
            action(*args, **kwargs)
    else:
        action(*args, **kwargs)
    
@contextmanager
def commit_changes(repo_path, branch, msg, confirm_commit=True):
    repo = RepoWrapper(repo_path)

    if repo.is_dirty(untracked_files=True) or (str(repo.active_branch) != "main" and str(repo.active_branch) != "master" and str(repo.active_branch) != branch):
        raise DirtyRepositoryError(f"Please make sure git status is clean in '{repo.working_tree_dir}' and that the active branch is main/master or {branch}.")
    
    repo.switch(branch)

    yield repo

    if not confirm_commit or Confirm.ask(f"Commit all changes and untracked files in '{repo.working_tree_dir}'?", default="y"):
        repo.commit_all(msg)


class RepoWrapper(Repo):
    """
    A wrapper around a git repository
    """
    def __init__(self, path, origin=None):
        """
        Args:
            path: The path to the git repository
        """
        super().__init__(path)
        try:
            self._repo = self
            # assert self._repo.remote().url == origin
        except (InvalidGitRepositoryError, NoSuchPathError):
            os.makedirs(path)
            self._repo = Repo.init(path, initial_branch='main')
            self._repo.create_remote("origin", origin)
            
        except Exception as e:
            raise RuntimeError("Unable to attach to git repository at path {}: {}".format(path, e))
    

    def switch(self, branch="main"):
        """
        Switch to branch. Creates it if needed.

        Args:
            branch: Name of the branch to switch to. Defaults to 'main'
        """
        try:
            logging.info(f"Switching to branch '{branch}' in {self._repo.working_dir}")
            if str(branch) == str(self._repo.active_branch):
                logging.info(f"Already on branch '{branch}'")
                return
            
            if branch in self._repo.branches:
                logging.info("Branch exists, switching to it")
                self._repo.git.checkout(branch)
            else:
                logging.info("Branch does not exist, making new branch")
                self._repo.git.checkout("-b", branch)
            
        except GitCommandError as e:
            raise RuntimeError("Error whilst creating git branch, {}".format(e))

    def commit_all(self, msg: str):
        """
        Commits all changes and untracked files in the repository.

        Args:
            msg: the commit message
        """

        logging.debug(f"Attempting to commit all changes and untracked files in '{self.working_tree_dir}'.")

        try:
            self._repo.git.add(A=True)
            self._repo.git.commit(m=msg)
        except (OSError, GitCommandError) as e:
            raise RuntimeError("Error whilst creating commit in {}: {}"
                               .format(self._repo.working_dir, e))
        
    def create_submodule(self, name, url, path):
        """
        Args:
            name: Name of the submodule
            url: Url to the submodule repo
            path: Local system path to the submodule
        """
        try:
            branch = "main"
            # create path relative to current root in case path is absolute
            sub_path = relpath(path, start=self._repo.working_tree_dir)
            # We use subprocess here because gitpython seems to add a /refs/heads/ prefix to any branch you give it,
            # and this breaks the repo checks. 
            subprocess.run(f"git submodule add -b {branch} --name {name} {url} {sub_path}", cwd = self._repo.working_tree_dir, check=True)
                
        except subprocess.CalledProcessError as e:
            logging.error("Cannot add {} as a submodule, error: {}".format(path, e))
        except Exception as e:
            raise RuntimeError("Unknown error {} of type {} whilst creating submodule in {}".format(e, type(e), path))
