"""Exceptions thrown by this package."""

from git import Repo


class IBEXDeviceGeneratorError(Exception):
    """Base class for all package exceptions."""


class CommandNotFoundError(IBEXDeviceGeneratorError):
    """Raised when a command is not found on system."""

    def __init__(self, cmd: str, msg: str) -> None:  # noqa: D107
        self.cmd = cmd
        self.msg = msg

    def __str__(self) -> str:  # noqa: D105
        return "Could not find executable for command '%s': %s" % (
            self.cmd,
            self.msg,
        )


class NoGitHubTokenError(IBEXDeviceGeneratorError):
    """GitHub token is not specified."""

    def __str__(self) -> str:  # noqa: D105
        return (
            "GitHub token is not specified. Rerun the command with the"
            " '--github_token <your_token>' option."
        )


class FailedToCreateGitHubRepositoryError(IBEXDeviceGeneratorError):
    """Thrown when repo could not be created on GitHub."""

    def __init__(self, org: str, repo: str, msg: str) -> None:  # noqa: D107
        self.org = org
        self.repo = repo
        self.msg = msg

    def __str__(self) -> str:  # noqa: D105
        return "Failed to create GitHub repo '%s' within %s: %s" % (
            self.repo,
            self.org,
            self.msg,
        )


class FailedToGrantPermissionError(IBEXDeviceGeneratorError):
    """For some reason could not grant permission."""

    def __init__(self, permission: str, repo: str, msg: str) -> None:  # noqa: D107
        self.permission = permission
        self.repo = repo
        self.msg = msg

    def __str__(self) -> str:  # noqa: D105
        return "Failed to grant %s permission for %s: %s" % (
            self.permission,
            self.repo,
            self.msg,
        )


# Device info related


class InvalidIOCNameError(IBEXDeviceGeneratorError):
    """Indicate that IOC name is invalid."""

    def __init__(self, name: str) -> None:  # noqa: D107
        self.name = name

    def __str__(self) -> str:  # noqa: D105
        return (
            "'%s' is an invalid IOC name, it can only contain alphanumeric"
            " upper case characters and must be between 1 and 8 characters"
            " long." % self.name
        )


class InvalidDeviceNameError(IBEXDeviceGeneratorError):
    """Indicate that device name is invalid."""

    def __init__(self, name: str) -> None:  # noqa: D107
        self.name = name

    def __str__(self) -> str:  # noqa: D105
        return (
            "'%s' is an invalid device name,"
            " it can only cantain ASCII characters." % self.name
        )


class InvalidDeviceCountError(IBEXDeviceGeneratorError):
    """Indicate that device count is invalid."""

    def __init__(self, count: int) -> None:  # noqa: D107
        self.count = count

    def __str__(self) -> str:  # noqa: D105
        return (
            "'%d' is an invalid device count. This must be between 1 and 99."
            % self.count
        )


class ReassignPlaceholderError(IBEXDeviceGeneratorError):
    """Thrown when a device info value is reassigned after initialisation."""

    def __init__(self, placeholder: str) -> None:  # noqa: D107
        self.placeholder = placeholder

    def __str__(self) -> str:  # noqa: D105
        return (
            "Cannot reassign value of '%s' after device info instantiation."
            % self.placeholder
        )


# Git related


class CannotOpenRepoError(IBEXDeviceGeneratorError):
    """Thrown when GitPython cannot be initialised at path."""

    def __init__(self, path: str) -> None:  # noqa: D107
        self.path = path

    def __str__(self) -> str:  # noqa: D105
        return (
            "Cannot open git repository at %s."
            " Check if git repo exists at location." % self.path
        )


class FailedToSwitchBranchError(IBEXDeviceGeneratorError):
    """Thrown when switching branch failed."""

    def __init__(self, repo: Repo, branch: str, msg: str) -> None:  # noqa: D107
        self.repo = repo
        self.branch = branch
        self.msg = msg

    def __str__(self) -> str:  # noqa: D105
        return "Failed to switch to branch '%s' in repo '%s': %s" % (
            self.branch,
            self.repo.working_tree_dir,
            self.msg,
        )
