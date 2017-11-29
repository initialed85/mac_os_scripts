#!/bin/bash

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
