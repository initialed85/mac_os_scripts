#!/bin/bash

# this file is applicable for all users (hence run at build time)

# prerequisites
#
# have copied the inner mac_os_scripts folder to /usr/local/zetta as well as the
# two bash scripts

# this is the password of the admin user in the sudo group (localuser currently)
# it's not yet proven that this mightn't be needed at all (depending on which privileges
# the build user has)
SUDO_PASSWORD=Password1

# need to run scripts from here because of Python path requirements
cd /usr/local/zetta/

# disable ipv6
python -m mac_os_scripts.disable_ipv6 -x $SUDO_PASSWORD

# enable security logging
python -m mac_os_scripts.enable_security_logging -x $SUDO_PASSWORD

# enable login scripts
python -m mac_os_scripts.enable_login_scripts -x $SUDO_PASSWORD

# enable restricted ssh for specified hosts
python -m mac_os_scripts.enable_restricted_ssh -x $SUDO_PASSWORD -a 192.168.1.1,192.168.1.2
