# Support submodule makefile to be placed in: C:\Instrument\Apps\EPICS\support\{name}

TOP = ../../extensions/master
include $$(TOP)/configure/CONFIG

DIRS_NOTBUILD = Makefile NULL

DIRS := $$(DIRS) $$(filter-out $$(DIRS) $$(DIRS_NOTBUILD), $$(wildcard *))

include $$(TOP)/configure/RULES_DIRS_INT
