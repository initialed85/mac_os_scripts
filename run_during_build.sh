#!/bin/bash

# this file is applicable for all users (hence run at build time)

# you'll need to have copied the inner mac_os_scripts folder to /usr/local/zetta as well
# as the two bash scripts

# WARNING: all special characters need to be strings with single quotes in order to not get
# interpreted by the shell, e.g. P@$$w0rd123!@# should be 'P@$$w0rd123!@#'- basically, it's
# it's safest to pass all strings as single quotes unless you need to include variables in them

# credentials that are required
LOCAL_ADMIN_USERNAME='admin_username'
LOCAL_ADMIN_PASSWORD='Password1'

# credentials that'll be set
ROOT_PASSWORD='P@$$w0rd123!@#'
FIRMWARE_PASSWORD='P@$$w0rd123!@#'

# for adding the computer to a group (note use of $HOSTNAME)
SOURCE_OU_PATH="CN=$HOSTNAME,OU=macOS,OU=Computers,OU=Some Place,DC=some,DC=domain,DC=com"
DESTINATION_OU_PATH="CN=Developers,OU=Users,OU=Groups,OU=Some Place,DC=some,DC=domain,DC=com"
DOMAIN='some.domain.com'
DOMAIN_ADMIN_USERNAME="some.admin@$DOMAIN"
DOMAIN_ADMIN_PASSWORD='Password2'

# this is a comma-separated list of IPs or subnets with prefixes allowed to SSH into machines
SSH_ALLOWED_HOSTS='192.168.137.0/24,10.0.1.0/24,192.168.1.1,127.0.0.1'

# this is the ntp server to configure
NTP_SERVER=time1.google.com

# need to run scripts from here because of Python path requirements
cd /usr/local/zetta/

# disable metadata file creation
python -m mac_os_scripts.disable_metadata_file_creation

# configure auditing flags
python -m mac_os_scripts.configure_auditing_flags

# disable ipv6
python -m mac_os_scripts.disable_ipv6

# enable security logging
python -m mac_os_scripts.enable_security_logging

# enable login scripts
python -m mac_os_scripts.enable_login_scripts

# enable restricted ssh for specified hosts
python -m mac_os_scripts.enable_restricted_ssh -a $SSH_ALLOWED_HOSTS

# enable ntp and set ntp server
python -m mac_os_scripts.configure_ntp -s $NTP_SERVER

# set the user logo for the build user
python -m mac_os_scripts.set_user_account_logo -u $LOCAL_ADMIN_USERNAME -l /usr/local/zetta/user_logo.tiff

# set the root password and then disable the root user
python -m mac_os_scripts.configure_root_user -u $LOCAL_ADMIN_USERNAME -p $LOCAL_ADMIN_PASSWORD -r $ROOT_PASSWORD

# disable core dumps
python -m mac_os_scripts.disable_core_dump

# enable restricted IBSS (ad-hoc/computer-to-computer wireless networking)
python -m mac_os_scripts.enable_restricted_ibss

# register a computer account on the domain for this machine
python -m mac_os_scripts.add_computer_to_group -s $SOURCE_OU_PATH -d $DESTINATION_OU_PATH -u $DOMAIN_ADMIN_USERNAME -p $DOMAIN_ADMIN_PASSWORD

# disable guest connection to shared folders
python -m mac_os_scripts.disable_guest_connection_to_shared_folders

# set firmware password
# python -m mac_os_scripts.set_firmware_password -f $FIRMWARE_PASSWORD

# enable discrete graphics (GPU)
python -m mac_os_scripts.enable_discrete_graphics
