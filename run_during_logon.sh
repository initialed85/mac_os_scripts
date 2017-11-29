#!/bin/bash

# this file is applicable for each user that logs on (hence runs at log on time)

# prerequisites
#
# have copied the inner mac_os_scripts folder to /usr/local/zetta as well as the
# two bash scripts

# logging stuff
LOG_FILENAME=/tmp/mac_os_scripts_${USER}_run_during_logon.log
STDOUT_LOG_FILENAME=/tmp/mac_os_scripts_${USER}_run_during_logon_stdout.log
STDERR_LOG_FILENAME=/tmp/mac_os_scripts_${USER}_run_during_logon_stderr.log

echo "" > $LOG_FILENAME
echo "" > $STDOUT_LOG_FILENAME
echo "" > $STDERR_LOG_FILENAME

log() {
    echo `/bin/date` $0 $@ >> $LOG_FILENAME
}

log_stdout() {
    echo `/bin/date` $0 $@ >> $STDOUT_LOG_FILENAME
}

log_stderr() {
    echo `/bin/date` $0 $@ >> $STDERR_LOG_FILENAME
}

run_and_log() {
    log_stdout "calling $@"
    log_stderr "calling $@"

    log "calling $@"
    "$@" 2>>$STDERR_LOG_FILENAME 1>>$STDOUT_LOG_FILENAME
    RETURN_LEVEL=$?
    log "return level $RETURN_LEVEL"

    echo -ne "\n---- ---- ---- ----\n\n" >>$STDERR_LOG_FILENAME
    echo -ne "\n---- ---- ---- ----\n\n" >>$STDOUT_LOG_FILENAME
}

log '!!!! started'

log 'setting some environment variables'

# fully qualified domain name of the file server
FQDN='grayfs01.grayman.com.au'

# will be suffixed with \(current username)
SHARE_PREFIX='homedrives$'

# need to run scripts from here because of Python path requirements
run_and_log cd /usr/local/zetta/
run_and_log python -m mac_os_scripts.disable_handoff
# python -m mac_os_scripts.change_background  # set in user template
run_and_log python -m mac_os_scripts.disable_airdrop
run_and_log python -m mac_os_scripts.enable_reduced_transparency
run_and_log python -m mac_os_scripts.disable_metadata_file_creation
run_and_log python -m mac_os_scripts.map_user_drive -f "$FQDN" -s "$SHARE_PREFIX"

log '!!!! finished'
