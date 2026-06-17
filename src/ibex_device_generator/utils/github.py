"""GitHub related helper functions."""

import logging

import requests

from ibex_device_generator.exc import (
    FailedToCreateGitHubRepositoryError,
    FailedToGrantPermissionError,
    NoGitHubTokenError,
)
from ibex_device_generator.utils.device_info import DeviceInfo
from ibex_device_generator.utils.placeholders import GITHUB_REPO_NAME

ORGANIZATION_NAME = "ISISComputingGroup"
EPICS_REPO_NAME = "EPICS"
IBEX_CLIENT_REPO_NAME = "ibex_gui"


def create_github_repository(device: DeviceInfo, github_token: str) -> None:
    """Create a public repo in the ISIS Computing Group organization.

    Args:
        device: Provides name-based information about the device
        github_token: The GitHub authentication token.

    """
    if github_token is None:
        raise NoGitHubTokenError()

    response: requests.Response = requests.post(
        f"https://api.github.com/orgs/{ORGANIZATION_NAME}/repos",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {github_token}",
        },
        json={
            "name": device[GITHUB_REPO_NAME],
            "visibility": "public",
            "auto_init": True,
        },
    )

    if response.status_code == requests.codes["created"]:
        logging.info((f"Repository {response.json().get('html_url')}" " created successfully."))
    else:
        raise FailedToCreateGitHubRepositoryError(
            ORGANIZATION_NAME, device[GITHUB_REPO_NAME], response.reason
        )


def grant_permission(
    github_token: str, team_name: str, permission: str, repository_name: str
) -> None:
    """Grant permission to repo.

    Args:
        github_token: The GitHub authentication token.
        team_name: The name of the team.
        permission: The permission to add. See GitHub documentation for types.
        repository_name: The name of the repository.

    """
    response: requests.Response = requests.put(
        f"https://api.github.com/orgs/{ORGANIZATION_NAME}/teams/{team_name}/repos/{ORGANIZATION_NAME}/{repository_name}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_token}",
        },
        json={"permission": permission},
    )

    if response.status_code == requests.codes["no_content"]:
        logging.info(
            (
                f"Permission '{permission}' granted to team '{team_name}'"
                f" for repository '{repository_name}'."
            )
        )
    else:
        raise FailedToGrantPermissionError(permission, repository_name, response.reason)


def grant_permissions_for_github_repository(device: DeviceInfo, github_token: str) -> None:
    """Grant permissions to teams for the GitHub repository.

    Args:
        device: Provides name-based information about the device
        github_token: The GitHub authentication token.

    """
    if github_token is None:
        raise NoGitHubTokenError()

    grant_permission(
        github_token,
        "ICP-Write",
        "push",
        device[GITHUB_REPO_NAME],
    )
    grant_permission(
        github_token,
        "ICP-WriteAndMerge",
        "maintain",
        device[GITHUB_REPO_NAME],
    )
    grant_permission(
        github_token,
        "ICP-Read",
        "read",
        device[GITHUB_REPO_NAME],
    )


def does_github_issue_exist_and_is_open(issue_number: int) -> bool:
    """Check whether GitHub issue exists and is open.

    Args:
        issue_number: The GitHub issue/ticket number.

    Returns:
        Whether or not ticket exists and is open on GitHub.

    """
    result = requests.get(
        f"https://api.github.com/repos/{ORGANIZATION_NAME}/IBEX/issues/{issue_number}"
    )
    return result.ok and result.json()["state"] == "open"


def github_repo_url(repo_name: str, organisation: str = ORGANIZATION_NAME) -> str:
    """Get repo url for repo of the organisation.

    Args:
        repo_name: Name of the repository
        organisation: The GitHub organisation owning the repository

    Returns:
        The url to the repository

    """
    return f"https://github.com/{organisation}/{repo_name}.git"
