"""Rich helper functions."""

import os
from os import PathLike
from typing import Any

from rich.console import Console
from rich.tree import Tree


def rich_print(*objects: Any) -> str:
    """..."""
    console = Console()
    with console.capture() as capture:
        console.print(*objects)
    return capture.get()


# TODO suggest a function to rich public
# something like
def tree_from_paths(paths: list[PathLike]) -> Tree:
    """..."""
    root = os.path.commonpath([os.path.dirname(path) for path in paths])

    tree = Tree(root)

    for path in paths:
        remaining_path = os.path.relpath(path, root)

        node = tree
        for segment in remaining_path.split(os.sep):
            segment_in_tree = next(
                (child for child in node.children if child.label == segment),
                None,
            )
            if segment_in_tree:
                node = segment_in_tree
            else:
                node = node.add(segment)

    return tree
