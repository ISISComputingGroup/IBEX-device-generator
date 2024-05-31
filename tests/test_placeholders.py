"""Test placeholders."""

from os.path import join
from tempfile import TemporaryDirectory, gettempdir
from unittest import TestCase

import ibex_device_generator.utils.placeholders as keys_file
from ibex_device_generator.utils.templates import (
    get_template,
    populate_template_dir,
)


class PlaceholderTests(TestCase):
    """Tests in connection with placeholders in the templates."""

    def setUp(self) -> None:
        """Retrieve the placeholders from the placeholder.py file."""
        self.placeholders = get_placeholders()

    def test_all_placeholders_in_templates_are_present(self) -> None:
        """Check templates directory for unknown placeholder."""
        with TemporaryDirectory() as tmpdir:
            substitutions = {
                key: "value" for key in self.placeholders.values()
            }

            try:
                populate_template_dir(
                    get_template(), join(gettempdir(), tmpdir), substitutions
                )
            except KeyError as e:
                self.fail(
                    (
                        "There is an undefined placeholder in the"
                        f" templates directory: {e}"
                    )
                )


def get_placeholders() -> dict[str, str]:
    """Get all the placeholders from the placeholders.py file.

    Returns:
        A dictionary of {name: value} where name is the variable name and
        value is the variable's value

    """
    placeholders = {
        name: value
        for (name, value) in vars(keys_file).items()
        if not name.startswith("__")
    }
    return placeholders
