#!/bin/bash

echo -ne "info: $0 started\n\n"

TARGET_USER_TEMPLATE=/System/Library/User\ Template/English.lproj
TARGET_USER_TEMPLATE_BACKUP=./English.lproj

if [[ "$USER" != "root" ]] ; then
    echo "error: must be run as root/sudo"
    exit 1
fi

if [[ ! -d "$TARGET_USER_TEMPLATE_BACKUP" ]] ; then
    echo "error: TARGET_USER_TEMPLATE_BACKUP doesn't exist- can't restore!"
    exit 1
fi

echo "info: restoring backup at $TARGET_USER_TEMPLATE_BACKUP to $TARGET_USER_TEMPLATE"
rm -fr "$TARGET_USER_TEMPLATE"
mv -fv "$TARGET_USER_TEMPLATE_BACKUP" "$TARGET_USER_TEMPLATE"

echo -ne "info: $0 finished\n\n"
