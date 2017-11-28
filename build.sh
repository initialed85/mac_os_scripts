#!/bin/bash

rm -fr deploy

mkdir -p deploy/mac_os_scripts

cp -frv run_during*.sh deploy/

cp -frv mac_os_scripts/*.py deploy/mac_os_scripts

cp -frv mac_os_scripts/external deploy/mac_os_scripts/
