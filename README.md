# IBEX Device Generator


> [!WARNING]
> **Might fail to commit because of commit hook in ibex_gui**
> On the add OPI to gui step the script might fail to commit due to a git commit hook that usually changes opi-s by adding "dummy widgets"
> Workaround: You can manually commit the added files afterwards or run that step without the --use_git flag.


> [!IMPORTANT]
> This script does not push to remote repositories at any stage __by design__. Instead it makes local commits (if --use_git) that can be verified and later pushed to the appropriate upstream repos by the developer.


## Installation


```
pip install git+https://github.com/ISISComputingGroup/IBEX-device-generator.git@latest_release
```

[More details on pip version control system (VCS) support...](https://pip.pypa.io/en/stable/topics/vcs-support/)

## Example Usage


1. Make sure the following repos are on __master__/__main__ branch and git status is clean: `Instrument/Apps/EPICS`, `Instrument/Apps/EPICS/ioc/master`, `Instrument/Dev/ibex_gui`.

2. Open a terminal that has python installed. (Add `C:\Instrument\Apps\Python3` and `C:/Instrument/Apps/Python3/Scripts` to your PATH if not there alredy.)

3. Run the following command to start device generation:
    ```
    ibex_device_generator <ioc_name> <ticket_number> --device_name <device_name> --device_count <device_count> --use_git --github_token <your_github_token> -i
    ```

4. Verify that the device has been generated successfuly by running the (system tests) `run_tests.bat` in `C:/Instrument/Apps/EPICS/support/<device_name>/master/system_tests`

Throughout this example substitute <ioc_name>, <device_name>, <device_count> etc. according to your needs.


## Usage


```
ibex_device_generator [-h] [--device_name DEVICE_NAME] [--device_count DEVICE_COUNT] [--use_git]
                             [--github_token GITHUB_TOKEN] [--log_level {DEBUG,INFO,WARN,ERROR}]
                             ioc_name ticket
```

For the generator to run smoothly, please make sure the git status is clean in the directories where the script is making modifications.
For example in EPICS top, ioc/master. If git status is not clean the script will raise an error at that step when `--use_git` flag is specified.


#### GitHub Token

The GitHub token is needed for the script to be able to create repository. GitHub authentication token with `repo` scope. Use to create support repository. (How to create token: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)


## Templates


The templates for the file structure generation can be found in the `templates` directory.


### Placeholders


See [src/ibex_device_generator/utils/placeholders.py](./src/ibex_device_generator/utils/placeholders.py) for a complete list of placeholders and their descriptions.

Placeholders in the templates can be anywhere (including file names, directory names or file content). They are preceeded by the '@' delimiter. When the placeholder is not followed by a space use @{placeholder}.

> [!WARNING]
> If the delimiter character needs to be used on it's own escape it by prepending it, i.e. use '@@' to get a single '@' character after substitutions.

When using a template most of these substitutions must be present.


## Development

[Contributing Guidelines](./CONTRIBUTING.md)

To test changes made to this package you can install it directly with pip via:
```
pip install .
```

### Run Tests


With __pytest__ just run the `pytest` command in the project's root.

With __unittest__, run the following command from the `src/` directory:
```
python -m unittest discover -s ..
```
