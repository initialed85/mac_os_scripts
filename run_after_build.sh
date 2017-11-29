#!/bin/bash

# this file is intended to run after the build (to clean up logs etc)

# logging stuff
LOG_FILENAME=/tmp/mac_os_scripts_${USER}_run_during_logon.log
STDOUT_LOG_FILENAME=/tmp/mac_os_scripts_${USER}_run_during_logon_stdout.log
STDERR_LOG_FILENAME=/tmp/mac_os_scripts_${USER}_run_during_logon_stderr.log

source /usr/local/zetta/include.sh

log '!!!! started'

run_and_log rm -frv /usr/local/zetta/run_during_build.sh
run_and_log rm -frv /tmp/mac_os_scripts*

log '!!!! finished'
