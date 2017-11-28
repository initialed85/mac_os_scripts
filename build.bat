@echo off

del /f -s -q deploy

mkdir deploy\mac_os_scripts

copy /y run_during*.sh deploy\

copy /y mac_os_scripts\*.py deploy\mac_os_scripts\

copy /y mac_os_scripts\*external deploy\mac_os_scripts\
