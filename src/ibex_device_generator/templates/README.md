> [!CAUTION]
> Template folder names are kept short to avid long path error on Windows.

| Template directory name | Description |
| ----------------------- | ----------- |
| 3 | This step adds the support submodule to EPICS top. Files here will be added to EPICS top repo. |
| 4 | Create the support submodule structure within EPICS/support/device_name. |
| 5_1 | Create first IOC in EPICS/ioc/master/ioc_name. |
| 5_2 | Create n-th IOC in EPICS/ioc/master/ioc_name. (This is run with the previous step) |
| 6 | Create the files in the support module needed for the test framework. |
| 7 | Create the files neccessary for the lewis emulator. |
| 8 | Files to be added to the gui source code. |