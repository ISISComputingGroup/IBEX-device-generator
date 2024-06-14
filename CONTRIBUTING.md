# Let's get coding...

## Getting started

Get set up by cloning the repository.

### Issues

Issues are currently tracked within the [IBEX](https://github.com/ISISComputingGroup/IBEX/issues) repository.

### Development Workflow

__For developers within the team with push access to the repository.__

1. Pick up an issue related to this project from the [Project Board](https://github.com/ISISComputingGroup/IBEX/projects/1).
1. Create a new branch off main following our branch naming convention `ticket<number>-<short_description>` e.g. `ticket1234-add-amazing-feature`.
1. Do the work on this branch locally and then push the branch onto github via `git push -u origin <branch_name>` e.g. `git push -u origin ticket1234-add-amazing-feature`
1. Create a new Pull Request to merge your ticket branch into main with detailed description of the work done.
1. Wait for a reviewer to accept your changes and merge the Pull Request. ✨

### Issue a New Release

1. Following the major-minor-patch versioning decide the next version number based on the changes since last version.
You can do this at https://github.com/ISISComputingGroup/IBEX-device-generator/compare/latest_release...HEAD
1. Change the version number accordingly in the [pyproject.toml](https://github.com/ISISComputingGroup/IBEX-device-generator/blob/main/pyproject.toml#L7) file.
1. Create a new annotated tag with the new version number in the form of `v0.0.0`. e.g. `git tag -a v1.0.3` then push it to GitHub via `git push origin tag v1.0.3`
1. [Create a new release](https://github.com/ISISComputingGroup/IBEX-device-generator/releases/new) on GitHub pointing at the tag just created.
1. Move the `latest_release` tag to the latest release commit and push to GitHub. e.g. `git tag -a latest_release -f` and `git push origin tag latest_release -f`

