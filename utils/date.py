"""Helper functions dealing with date."""

import datetime


def get_year() -> str:
    """Get current year."""
    return str(datetime.datetime.now().year)
