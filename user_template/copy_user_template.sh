#!/bin/bash

echo -ne "info: $0 started\n\n"

TARGET_USER_TEMPLATE=/System/Library/User\ Template/English.lproj

if [[ "$USER" != "root" ]] ; then
    echo "error: must be run as root/sudo"
    exit 1
fi

echo "info: copying the current user template to this folder"
cp -fr "$TARGET_USER_TEMPLATE" .
echo ""

echo "info: compressing into a .tar.gz"
tar -czf English.lproj.tar.gz ./English.lproj
echo ""

echo "note: this file is owned by root; you'll need to fix the permissions if you want to access it"
echo ""

echo -ne "info: $0 finished\n\n"
