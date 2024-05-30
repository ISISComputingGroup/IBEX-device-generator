import logging

import requests

from utils.device_info import GITHUB_REPO_NAME, DeviceInfo

ORGANIZATION_NAME = "ISISComputingGroup"


class NoGitHubTokenError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("GitHub token is not specified.", *args)


def create_github_repository(device: DeviceInfo, github_token: str) -> None:
    """
    Creates a public repo in the ISIS Computing Group organization.

    Args:
        device_info: Provides name-based information about the device
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
        logging.info(
            f"Repository {response.json().get('html_url')} created successfully."
        )
    else:
        raise Exception(
            f"Failed to create repository [{response.status_code}]: {response.reason}"
        )


def grant_permission(
    github_token: str, team_name: str, permission: str, repository_name: str
) -> None:
    """
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
            f"Permission '{permission}' granted to team '{team_name}' for repository '{repository_name}'."
        )
    else:
        raise Exception(
            f"Failed to grant permission [{response.status_code}]: {response.reason}"
        )


def grant_permissions_for_github_repository(
    device: DeviceInfo, github_token: str
) -> None:
    """
    Grant permissions to teams for the GitHub repository.

    Args:
        device_info: Provides name-based information about the device
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


def does_github_issue_exist_and_is_open(issue_number: int) -> bool:
    """
    Args:
        issue_number: The GitHub issue/ticket number.

    Returns: Whether or not ticket exists on GitHub.
    """
    result = requests.get(
        f"https://api.github.com/repos/{ORGANIZATION_NAME}/IBEX/issues/{issue_number}"
    )
    return result.ok and result.json()["state"] == "open"
