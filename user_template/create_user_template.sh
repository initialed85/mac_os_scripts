#!/bin/bash

echo -ne "info: $0 started\n\n"

TARGET_USER_TEMPLATE=/System/Library/User\ Template/English.lproj
TARGET_USER_TEMPLATE_BACKUP=./English.lproj

if [[ "$USER" != "root" ]] ; then
    echo "error: must be run as root/sudo"
    exit 1
fi

TARGET_USER=$1
if [[ "$TARGET_USER" == "" ]] ; then
    echo "error: must have target user specified as argument"
    exit 1
fi

if [[ ! -d "/Users/$TARGET_USER" ]] ; then
    echo "error: $TARGET_USER is unknown"
    exit 1
fi

TARGET_USER_HOME=/Users/$TARGET_USER

echo "info: backing up current user template"
mv -fv "$TARGET_USER_TEMPLATE" "$TARGET_USER_TEMPLATE_BACKUP"
echo ""

echo "info: dittoing the user $TARGET_USER"
ditto -v "$TARGET_USER_HOME" "$TARGET_USER_TEMPLATE"
echo ""

echo "info: deleting some unrequired files from the new template"
rm -frv "$TARGET_USER_TEMPLATE/Library/Application Support/com.apple.sharedfilelist"
rm -frv "$TARGET_USER_TEMPLATE/Library/Keychains/"*
rm -frv "$TARGET_USER_TEMPLATE/Library/Keychains/".* 2>/dev/null
rm -frv "$TARGET_USER_TEMPLATE/".bash_*
echo ""

echo "info: modifying com.apple.dock.plist as required"
plutil -convert xml1 -o com.apple.dock.plist-before "$TARGET_USER_TEMPLATE/Library/Preferences/com.apple.dock.plist"
cat com.apple.dock.plist-before | python -c "import sys; import re; open('com.apple.dock.plist-after', 'w').write(re.sub(r'\n\s+<key>_CFURLString</key>\n\s+<string>file:///Users/$TARGET_USER/Downloads/</string>\n', '\n', sys.stdin.read()))"
plutil -convert xml1 -o "$TARGET_USER_TEMPLATE/Library/Preferences/com.apple.dock.plist" com.apple.dock.plist-after
defaults read "$TARGET_USER_TEMPLATE/Library/Preferences/com.apple.dock.plist" | grep \"_CFURLString\" -A 1 | grep "/Downloads/"
if [[ $? -ne 0 ]]; then
    echo "info: seems to have worked (no mention of Downloads)"
else
    echo "warning: failed to modify com.apple.dock.plist- strange behaviour may occur!"
fi
rm -fr com.apple.dock.plist-before
rm -fr com.apple.dock.plist-after
echo ""

echo "info: fixing premissions on the new template"
chown -fR root:wheel "$TARGET_USER_TEMPLATE"
chmod -fR 755 "$TARGET_USER_TEMPLATE"
echo ""

echo -ne "info: $0 finished\n\n"
