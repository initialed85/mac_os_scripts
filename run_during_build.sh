#!/bin/bash

# this file is intended to run during build time (after the machine has been registered on the 
# domain)

# WARNING: all special characters need to be strings with single quotes in order to not get
# interpreted by the shell, e.g. P@$$w0rd123!@# should be 'P@$$w0rd123!@#'- basically, it's
# it's safest to pass all strings as single quotes unless you need to include variables in them

# logging stuff
LOG_FILENAME=/tmp/mac_os_scripts_run_during_build.log
STDOUT_LOG_FILENAME=/tmp/mac_os_scripts_run_during_build_stdout.log
STDERR_LOG_FILENAME=/tmp/mac_os_scripts_run_during_build_stderr.log

source /usr/local/zetta/include.sh

log '!!!! started'

log 'setting some environment variables'

# credentials that are required
LOCAL_ADMIN_USERNAME='bwadmin'
LOCAL_ADMIN_PASSWORD='Password1'

# credentials that'll be set
ROOT_PASSWORD='P@$$w0rd123!@#'
FIRMWARE_PASSWORD='P@$$w0rd123!@#'
VNC_PASSWORD='Password1'

# for adding the computer to a group (note use of $HOSTNAME)
SOURCE_OU_PATH="CN=$HOSTNAME,OU=macOS,OU=Computers,OU=Gray Lab,DC=grayman,DC=com,DC=au"
DESTINATION_OU_PATH="CN=Role-Adm-WSUS.Administrator-U-GS,OU=Admin Roles,OU=Groups,OU=Gray Lab,DC=grayman,DC=com,DC=au"
DOMAIN='grayman.com.au'
DOMAIN_ADMIN_USERNAME="administrator@$DOMAIN"
DOMAIN_ADMIN_PASSWORD='Password1'

# we believe this needs to be a tif and probably certain dimensions
USER_LOGO_PATH='/Library/User Pictures/Bankwest/bankwest.tiff'

# this is a comma-separated list of IPs or subnets with prefixes allowed to SSH into machines
SSH_ALLOWED_HOSTS='10.0.1.11'

# this is the ntp server to configure (commented- will be called before domain join)
# NTP_SERVER=graydc01.grayman.com.au

cd /usr/local/zetta/mac_os_scripts/external/

run_and_log tar -xzvf gfxCardStatus.app.tar.gz

run_and_log chmod 777 *.app
run_and_log chmod 777 *.sh
run_and_log chmod 777 *.expect

# need to run scripts from here because of Python path requirements
run_and_log cd /usr/local/zetta/
run_and_log mv -f "/System/Library/User Template/English.lproj" "/System/Library/User Template/English.lproj-backup"
run_and_log tar -xzvf English.lproj.tar.gz
run_and_log ditto -v English.lproj "/System/Library/User Template/English.lproj"
run_and_log chmod 777 run_during_logon.sh
run_and_log /usr/bin/python -m mac_os_scripts.configure_auditing_flags
run_and_log /usr/bin/python -m mac_os_scripts.disable_ipv6
run_and_log /usr/bin/python -m mac_os_scripts.enable_security_logging
# run_and_log /usr/bin/python -m mac_os_scripts.enable_login_scripts -t PartialTrust  # handled with launchDaemon
run_and_log /usr/bin/python -m mac_os_scripts.enable_restricted_ssh -a $SSH_ALLOWED_HOSTS  # need $SSH_ALLOWED_HOSTS, but not used
# run_and_log /usr/bin/python -m mac_os_scripts.configure_ntp -s $NTP_SERVER  # handled before domain join
run_and_log /usr/bin/python -m mac_os_scripts.set_user_account_logo -u $LOCAL_ADMIN_USERNAME -l "$USER_LOGO_PATH"
run_and_log /usr/bin/python -m mac_os_scripts.configure_root_user -u $LOCAL_ADMIN_USERNAME -p $LOCAL_ADMIN_PASSWORD -r $ROOT_PASSWORD
run_and_log /usr/bin/python -m mac_os_scripts.disable_core_dump
run_and_log /usr/bin/python -m mac_os_scripts.enable_restricted_ibss
run_and_log /usr/bin/python -m mac_os_scripts.add_computer_to_group -s "$SOURCE_OU_PATH" -d "$DESTINATION_OU_PATH" -u "$DOMAIN_ADMIN_USERNAME" -p "$DOMAIN_ADMIN_PASSWORD" -f "$DOMAIN"
run_and_log /usr/bin/python -m mac_os_scripts.disable_guest_connection_to_shared_folders
run_and_log /usr/bin/python -m mac_os_scripts.set_firmware_password -f $FIRMWARE_PASSWORD
run_and_log /usr/bin/python -m mac_os_scripts.enable_discrete_graphics
run_and_log /usr/bin/python -m mac_os_scripts.configure_vnc -v $VNC_PASSWORD

log '!!!! finished'
