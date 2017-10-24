#!/bin/bash

# probably needs to run with each user logon; straight from some helpful internet guy at
# https://www.jamf.com/jamf-nation/discussions/12545/a-script-to-disable-handoff

loggedInUser=$(ls -l /dev/console | awk '{ print $3 }')

uuid=$(/usr/sbin/system_profiler SPHardwareDataType | grep "Hardware UUID" | cut -c22-57)

handoff1=$(defaults read /Users/$loggedInUser/Library/Preferences/ByHost/com.apple.coreservices.lsuseractivityd.$uuid.plist ActivityAdvertisingAllowed)

handoff2=$(defaults read /Users/$loggedInUser/Library/Preferences/ByHost/com.apple.coreservices.lsuseractivityd.$uuid.plist ActivityReceivingAllowed)

echo "$handoff1"

echo "$handoff2"

if [[ "$handoff1" == "0" || "$handoff2" == 0 ]]; then
    echo "Exit Message: OK"
    exit 0
else
    defaults write /Users/$loggedInUser/Library/Preferences/ByHost/com.apple.coreservices.lsuseractivityd.$uuid.plist ActivityAdvertisingAllowed -bool no defaults write /Users/$loggedInUser/Library/Preferences/ByHost/com.apple.coreservices.lsuseractivityd.$uuid.plist ActivityReceivingAllowed -bool no
    echo "Exit Message: Handoff Disabled"
fi

exit 1
