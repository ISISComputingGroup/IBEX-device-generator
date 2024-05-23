# IBEX Device Generator

> [!WARNING]
> **Known limitation**
> On the add OPI to gui step the script will fail to commit due to a git commit hook that usually changes opi-s by adding "dummy widgets"
> Workaround: You can manually commit the added files afterwards

## Overview

```
usage: generate.py [-h] [--device_name DEVICE_NAME] [--device_count DEVICE_COUNT] [--use_git]
                   [--github_token GITHUB_TOKEN] [--log_level {DEBUG,INFO,WARN,ERROR}]
                   ioc_name ticket

IBEX Device IOC Generator. Generate boilerplate code for IBEX device support.

positional arguments:
  ioc_name              Name of the IOC. This name is used in the ioc/master submodule and PVs will use this name.
  ticket                GitHub issue 'ticket' number within our development workflow.

options:
  -h, --help            show this help message and exit
  --device_name DEVICE_NAME
                        Name of the device, this name will be used to create suppport submodule and GitHub repository.
                        If not specified it defaults to be the same as the IOC name.
  --device_count DEVICE_COUNT
                        Number of duplicate device IOCs to generate.
  --use_git             Create/switch to ticket branches and make commits accordingly at every step. The script will
                        abort if the git status is dirty at the respective repositories.
  --github_token GITHUB_TOKEN
                        GitHub token with "repo" scope. Use to create support repository.
  --log_level {DEBUG,INFO,WARN,ERROR}
                        Logging level.
```

For the generator to run smoothly, please make sure the git status is clean in the directories where the script is making modifications.
For example in EPICS top, ioc/master. If git status is not clean the script will abort at that step when `--use_git` flag is specified.

#### Example usage in an EPICS terminal:

```
%python3% generate.py <ioc name> <ticket> --device_name <device name> --use_git --github_token <github token>
```

#### GitHub Token

The GitHub token is needed for the script to be able to create repository. GitHub authentication token with `repo` scope. Use to create support repository. (How to create token: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)


## Templates

The templates for the file structure generation can be found in the `templates` directory.

### Placeholders

For a fill list of placeholders see [substitution_keys.py](./utils/substitution_keys.py).

Placeholders in the templates can be anywhere (including file names, directory names or file content). They are preceeded by the '@' delimiter. When the placeholder is not followed by a space use @{placeholder}.

> [!WARNING]
> If the delimiter character needs to be used on it's own escape it by prepending it, i.e. use '@@' to get a single '@' character after substitutions.

When using a template most of these substitutions must be present.

| placeholder | comments |
| ----------- | -------- |
| `ioc_name` | This is the IOC name passed down as command line argument when invoking the script. |
| `device_name` | The device name can be longer and can contain spaces. This will be used to name the support module folder and the GitHub repository. |
| `device_support_module_name` | This is the name of the directory within `EPICS/support/@{device_support_module_name}`. It is usually the lower case device name where we use '_'-s instead of spaces. |
| `ioc_number` | This is relevant when referring to the structure of the n-nth IOC. If there are multiple device IOCs within the `EPICS/ioc/master/@{ioc_name}` such as `@{ioc_name}-IOC-01App`, `@{ioc_name}-IOC-02App` etc. `ioc_number` must be a string that represents a number using two digits always (e.g. 01, 03, 14).
| `lewis_device_name` | This is usually the lower case device name where spaces have been replaced with '_'-s. This is used for example in the `EPICS/support/@{device_support_module_name}\system_tests` directory to create the lewis emulator folder. |
| `lewis_emulator_device_class_name` | This is a snake case representation of the `device_name` usually to use for naming the python class that represents the emulator for the device. |