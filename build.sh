#!/bin/bash

rm -fr deploy

mkdir -p deploy/mac_os_scripts

cp -frv run_during*.sh deploy/

cp -frv mac_os_scripts/*.py deploy/mac_os_scripts

rm -fr deploy/mac_os_scripts/*_test.py

cp -frv mac_os_scripts/shell_scripts deploy/mac_os_scripts/shell_scripts
