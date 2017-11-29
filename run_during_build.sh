#!/bin/bash

# this file is applicable for all users (hence run at build time)

# you'll need to have copied the inner mac_os_scripts folder to /usr/local/zetta as well
# as the two bash scripts

# WARNING: all special characters need to be strings with single quotes in order to not get
# interpreted by the shell, e.g. P@$$w0rd123!@# should be 'P@$$w0rd123!@#'- basically, it's
# it's safest to pass all strings as single quotes unless you need to include variables in them

# logging function
LOG_FILENAME=/tmp/mac_os_scripts_run_during_build.log
log() {
    echo `date` $0 $@ >> $LOG_FILENAME
}

log '--------'
log 'started'
log '--------'

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

USER_LOGO_PATH='/Library/Caches/bankwest_userlogo.tif'

# this is a comma-separated list of IPs or subnets with prefixes allowed to SSH into machines
SSH_ALLOWED_HOSTS='10.0.1.11'

# this is the ntp server to configure (commented- will be called before domain join)
# NTP_SERVER=graydc01.grayman.com.au

cd /usr/local/zetta/mac_os_scripts/external/

log 'extracting some stuff'
tar -xzvf gfxCardStatus.app.tar.gz
log "return level $?"

log 'fixing some permissions'
chmod 777 *.app
log "return level $?"
chmod 777 *.sh
log "return level $?"
chmod 777 *.expect
log "return level $?"

cd /usr/local/zetta/

log 'backing up old user template'
mv -f "/System/Library/User Template/English.lproj" "/System/Library/User Template/English.lproj-backup"
log "return level $?"

log 'extracting new user template'
tar -xzvf English.lproj.tar.gz
log "return level $?"

log 'dittoing new user template into place'
ditto -v English.lproj "/System/Library/User Template/English.lproj"
log "return level $?"

log 'fixing some more permissions'
chmod 777 run_during_logon.sh
log "return level $?"

log 'python -m mac_os_scripts.configure_auditing_flags'
python -m mac_os_scripts.configure_auditing_flags
log "return level $?"

log 'python -m mac_os_scripts.disable_ipv6'
python -m mac_os_scripts.disable_ipv6
log "return level $?"

log 'python -m mac_os_scripts.enable_security_logging'
python -m mac_os_scripts.enable_security_logging
log "return level $?"

# skipping- handled with LaunchDaemon
# log 'python -m mac_os_scripts.enable_login_scripts -t PartialTrust'
# python -m mac_os_scripts.enable_login_scripts -t PartialTrust
# log "return level $?"

log "python -m mac_os_scripts.enable_restricted_ssh -a $SSH_ALLOWED_HOSTS"
python -m mac_os_scripts.enable_restricted_ssh -a $SSH_ALLOWED_HOSTS  # $SSH_ALLOWED_HOSTS required to be not empty but is ignored for now
log "return level $?"

# skipping- handled in another script
# log 'python -m mac_os_scripts.configure_ntp -s $NTP_SERVER'
# python -m mac_os_scripts.configure_ntp -s $NTP_SERVER
# log "return level $?"

log "python -m mac_os_scripts.set_user_account_logo -u $LOCAL_ADMIN_USERNAME -l $USER_LOGO_PATH"
python -m mac_os_scripts.set_user_account_logo -u $LOCAL_ADMIN_USERNAME -l $USER_LOGO_PATH
log "return level $?"

log "python -m mac_os_scripts.configure_root_user -u $LOCAL_ADMIN_USERNAME -p $LOCAL_ADMIN_PASSWORD -r $ROOT_PASSWORD"
python -m mac_os_scripts.configure_root_user -u $LOCAL_ADMIN_USERNAME -p $LOCAL_ADMIN_PASSWORD -r $ROOT_PASSWORD
log "return level $?"

log 'python -m mac_os_scripts.disable_core_dump'
python -m mac_os_scripts.disable_core_dump
log "return level $?"

log 'python -m mac_os_scripts.enable_restricted_ibss'
python -m mac_os_scripts.enable_restricted_ibss
log "return level $?"

log "python -m mac_os_scripts.add_computer_to_group -s $SOURCE_OU_PATH -d $DESTINATION_OU_PATH -u $DOMAIN_ADMIN_USERNAME -p $DOMAIN_ADMIN_PASSWORD -f $DOMAIN"
python -m mac_os_scripts.add_computer_to_group -s "$SOURCE_OU_PATH" -d "$DESTINATION_OU_PATH" -u "$DOMAIN_ADMIN_USERNAME" -p "$DOMAIN_ADMIN_PASSWORD" -f "$DOMAIN"
log "return level $?"

log 'python -m mac_os_scripts.disable_guest_connection_to_shared_folders'
python -m mac_os_scripts.disable_guest_connection_to_shared_folders
log "return level $?"

log "python -m mac_os_scripts.set_firmware_password -f $FIRMWARE_PASSWORD"
python -m mac_os_scripts.set_firmware_password -f $FIRMWARE_PASSWORD
log "return level $?"

log 'python -m mac_os_scripts.enable_discrete_graphics'
python -m mac_os_scripts.enable_discrete_graphics
log "return level $?"

log "python -m mac_os_scripts.configure_vnc -v $VNC_PASSWORD"
python -m mac_os_scripts.configure_vnc -v $VNC_PASSWORD
log "return level $?"

log '--------'
log 'finished'
log '--------'
