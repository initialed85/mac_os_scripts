#!/bin/bash

# this file is applicable for all users (hence run at build time)

# you'll need to have copied the inner mac_os_scripts folder to /usr/local/zetta as well
# as the two bash scripts

# WARNING: all special characters need to be strings with single quotes in order to not get
# interpreted by the shell, e.g. P@$$w0rd123!@# should be 'P@$$w0rd123!@#'- basically, it's
# it's safest to pass all strings as single quotes unless you need to include variables in them

# credentials that are required
LOCAL_ADMIN_USERNAME='bwadmin'
LOCAL_ADMIN_PASSWORD='Password1'

# credentials that'll be set
ROOT_PASSWORD='P@$$w0rd123!@#'
FIRMWARE_PASSWORD='P@$$w0rd123!@#'
VNC_PASSWORD='Password1'z

# for adding the computer to a group (note use of $HOSTNAME)
SOURCE_OU_PATH="CN=$HOSTNAME,OU=macOS,OU=Computers,OU=Gray Lab,DC=grayman,DC=com,DC=au"
DESTINATION_OU_PATH="CN=Role-Adm-WSUS.Administrator-U-GS,OU=Admin Roles,OU=Groups,OU=Gray Lab,DC=grayman,DC=com,DC=au"
DOMAIN='grayman.com.au'
DOMAIN_ADMIN_USERNAME="administrator@$DOMAIN"
DOMAIN_ADMIN_PASSWORD='Password1'

USER_LOGO_PATH='/Library/Caches/bankwest_userlogo.png'

# this is a comma-separated list of IPs or subnets with prefixes allowed to SSH into machines
SSH_ALLOWED_HOSTS='10.0.1.11'

# this is the ntp server to configure
NTP_SERVER=graydc01.grayman.com.au

# extract some stuff
cd /usr/local/zetta/mac_os_scripts/external/
tar -xzvf gfxCardStatus.app.tar.gz

# fix some permissions
chmod 777 *.app
chmod 777 *.sh
chmod 777 *.expect

# need to run scripts from here because of Python path requirements
cd /usr/local/zetta/

# backup the old user template
mv -f "/System/Library/User Template/English.lproj" "/System/Library/User Template/English.lproj-backup"

# setup the new user template
tar -xzvf English.lproj.tar.gz
ditto -v English.lproj "/System/Library/User Template/English.lproj"

# fix some more permissions
chmod 777 run_during_logon.sh

# configure auditing flags
python -m mac_os_scripts.configure_auditing_flags

# disable ipv6
python -m mac_os_scripts.disable_ipv6

# enable security logging
python -m mac_os_scripts.enable_security_logging

# enable login scripts
# python -m mac_os_scripts.enable_login_scripts -t PartialTrust

# enable restricted ssh for specified hosts
python -m mac_os_scripts.enable_restricted_ssh -a $SSH_ALLOWED_HOSTS

# enable ntp and set ntp server
python -m mac_os_scripts.configure_ntp -s $NTP_SERVER

# set the user logo for the build user
python -m mac_os_scripts.set_user_account_logo -u $LOCAL_ADMIN_USERNAME -l $USER_LOGO_PATH

# set the root password and then disable the root user
python -m mac_os_scripts.configure_root_user -u $LOCAL_ADMIN_USERNAME -p $LOCAL_ADMIN_PASSWORD -r $ROOT_PASSWORD

# disable core dumps
python -m mac_os_scripts.disable_core_dump

# enable restricted IBSS (ad-hoc/computer-to-computer wireless networking)
python -m mac_os_scripts.enable_restricted_ibss

# register a computer account on the domain for this machine
python -m mac_os_scripts.add_computer_to_group -s "$SOURCE_OU_PATH" -d "$DESTINATION_OU_PATH" -u "$DOMAIN_ADMIN_USERNAME" -p "$DOMAIN_ADMIN_PASSWORD" -f "$DOMAIN"

# disable guest connection to shared folders
python -m mac_os_scripts.disable_guest_connection_to_shared_folders

# set firmware password
python -m mac_os_scripts.set_firmware_password -f $FIRMWARE_PASSWORD

# enable discrete graphics (GPU)
python -m mac_os_scripts.enable_discrete_graphics

# configure vnc and set password
python -m mac_os_scripts.configure_vnc -v $VNC_PASSWORD
