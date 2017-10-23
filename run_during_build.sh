#!/bin/bash

# assuming you've copied the contents of the mac_os_scripts folder to /usr/local/mac_os_scripts
cd /usr/local/

# disable ipv6
python -m mac_os_scripts.disable_ipv6

# enable security logging
python -m mac_os_scripts.enable_security_logging
