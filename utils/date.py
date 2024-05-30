"""Helper functions dealing with date"""

import datetime


def get_year() -> str:
    """
    Returns: The current year formatted as a string
    """
    return str(datetime.datetime.now().year)
