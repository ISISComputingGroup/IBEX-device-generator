#!../../bin/windows-x64/@{ioc}-IOC-@{ioc_number}

## You may have to change @{ioc}-IOC-@{ioc_number} to something else
## everywhere it appears in this file

# Increase this if you get <<TRUNCATED>> or discarded messages warnings in your errlog output
errlogInit2(65536, 256)

< envPaths

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/@{ioc}-IOC-@{ioc_number}.dbd"
@{ioc}_IOC_@{ioc_number}_registerRecordDeviceDriver pdbbase

## calling common command file in ioc 01 boot dir
< ${TOP}/iocBoot/ioc@{ioc}-IOC-01/st-common.cmd
