#!/bin/bash

echo "running for user $USER"

UUID=$(/usr/sbin/system_profiler SPHardwareDataType | grep "Hardware UUID" | cut -d ':' -f 2 | xargs)
echo "got uuid $UUID"

echo "adjusting settings in useractivityd with uuid"
/usr/bin/defaults write ~/Library/Preferences/ByHost/com.apple.coreservices.useractivityd.$UUID.plist ActivityReceivingAllowed -bool false
/usr/bin/defaults write ~/Library/Preferences/ByHost/com.apple.coreservices.useractivityd.$UUID.plist ActivityAdvertisingAllowed -bool false

echo "adjusting settings in useractivityd without uuid"
/usr/bin/defaults write ~/Library/Preferences/ByHost/com.apple.coreservices.useractivityd ActivityAdvertisingAllowed -bool false
/usr/bin/defaults write ~/Library/Preferences/ByHost/com.apple.coreservices.useractivityd ActivityReceivingAllowed -bool false

exit 0
