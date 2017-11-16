#!/bin/bash

find ./mac_os_scripts -name '*.py' | entr -c py.test -v
