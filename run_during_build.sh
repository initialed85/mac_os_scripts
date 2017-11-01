#!/bin/bash

# this file is applicable for all users (hence run at build time)

# you'll need to have copied the inner mac_os_scripts folder to /usr/local/zetta as well
# as the two bash scripts

# this is the password of the admin user in the sudo group (localuser currently) it's not
# yet proven that this mightn't be needed at all (depending on which privileges the build
# user has)
# WARNING: this password needs to be correctly escaped- e.g. "Password\ 123\!\@\#" (without
# the quotes)
SUDO_PASSWORD=Password1

# this is the root password to set before disabling the root user
# WARNING: this password needs to be correctly escaped- e.g. "Password\ 123\!\@\#" (without
# the quotes)
ROOT_PASSWORD=P\@\$\$w0rd123\!\@\#

# this is a comma-separated list of IPs allowed to SSH into machines
SSH_ALLOWED_HOSTS=192.168.1.1,192.168.1.2

# this is the ntp server to configure
NTP_SERVER=time1.google.com

# need to run scripts from here because of Python path requirements
cd /usr/local/zetta/

# disable ipv6
python -m mac_os_scripts.disable_ipv6 -x $SUDO_PASSWORD

# enable security logging
python -m mac_os_scripts.enable_security_logging -x $SUDO_PASSWORD

# enable login scripts
python -m mac_os_scripts.enable_login_scripts -x $SUDO_PASSWORD

# enable restricted ssh for specified hosts
python -m mac_os_scripts.enable_restricted_ssh -x $SUDO_PASSWORD -a $SSH_ALLOWED_HOSTS

# enable ntp and set ntp server
python -m mac_os_scripts.configure_ntp -x $SUDO_PASSWORD -s $NTP_SERVER

# set the user logo for the build user
python -m mac_os_scripts.set_user_account_logo -x $SUDO_PASSWORD -l /usr/local/zetta/user_logo.tiff

# set the root password and then disable the root user
python -m mac_os_scripts.configure_root_user -x $SUDO_PASSWORD -r $ROOT_PASSWORD

# disable core dumps
python -m mac_os_scripts.disable_core_dump -x $SUDO_PASSWORD

# enable restricted IBSS (ad-hoc/computer-to-computer wireless networking)
python -m mac_os_scripts.enable_restricted_ibss -x $SUDO_PASSWORD
