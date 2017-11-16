#!/bin/bash

hardware_uuid=$(/usr/sbin/system_profiler SPHardwareDataType | grep "Hardware UUID" | cut -d ':' -f 2 | xargs)
current_user=$USER

echo "hardware_uuid: $hardware_uuid"
echo "current_user: $current_user"

echo "fixing"
defaults write /Users/$current_user/Library/Preferences/ByHost/com.apple.coreservices.lsuseractivityd.$hardware_uuid.plist ActivityAdvertisingAllowed -bool false
defaults write /Users/$current_user/Library/Preferences/ByHost/com.apple.coreservices.lsuseractivityd.$hardware_uuid.plist ActivityReceivingAllowed -bool false
defaults write /Users/$current_user/Library/Preferences/com.apple.coreservices.lsuseractivityd.plist ActivityAdvertisingAllowed -bool false
defaults write /Users/$current_user/Library/Preferences/com.apple.coreservices.lsuseractivityd.plist ActivityReceivingAllowed -bool false

defaults write /Users/$current_user/Library/Preferences/ByHost/com.apple.coreservices.useractivityd.$hardware_uuid.plist ActivityAdvertisingAllowed -bool false
defaults write /Users/$current_user/Library/Preferences/ByHost/com.apple.coreservices.useractivityd.$hardware_uuid.plist ActivityReceivingAllowed -bool false
defaults write /Users/$current_user/Library/Preferences/com.apple.coreservices.useractivityd.plist ActivityAdvertisingAllowed -bool no
defaults write /Users/$current_user/Library/Preferences/com.apple.coreservices.useractivityd.plist ActivityReceivingAllowed -bool no

exit 0
