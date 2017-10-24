#!/bin/bash

echo "before"
defaults read /Users/`whoami`/Library/Preferences/ByHost/com.apple.coreservices.lsuseractivityd.plist ActivityAdvertisingAllowed -bool no
defaults read /Users/`whoami`/Library/Preferences/ByHost/com.apple.coreservices.lsuseractivityd.plist ActivityReceivingAllowed -bool no
defaults read /Users/`whoami`/Library/Preferences/ByHost/com.apple.coreservices.useractivityd.plist ActivityAdvertisingAllowed -bool no
defaults read /Users/`whoami`/Library/Preferences/ByHost/com.apple.coreservices.useractivityd.plist ActivityReceivingAllowed -bool no

echo "fixing"
defaults write /Users/`whoami`/Library/Preferences/ByHost/com.apple.coreservices.lsuseractivityd.plist ActivityAdvertisingAllowed -bool no
defaults write /Users/`whoami`/Library/Preferences/ByHost/com.apple.coreservices.lsuseractivityd.plist ActivityReceivingAllowed -bool no
defaults write /Users/`whoami`/Library/Preferences/ByHost/com.apple.coreservices.useractivityd.plist ActivityAdvertisingAllowed -bool no
defaults write /Users/`whoami`/Library/Preferences/ByHost/com.apple.coreservices.useractivityd.plist ActivityReceivingAllowed -bool no

echo "after"
defaults read /Users/`whoami`/Library/Preferences/ByHost/com.apple.coreservices.lsuseractivityd.plist ActivityAdvertisingAllowed -bool no
defaults read /Users/`whoami`/Library/Preferences/ByHost/com.apple.coreservices.lsuseractivityd.plist ActivityReceivingAllowed -bool no
defaults read /Users/`whoami`/Library/Preferences/ByHost/com.apple.coreservices.useractivityd.plist ActivityAdvertisingAllowed -bool no
defaults read /Users/`whoami`/Library/Preferences/ByHost/com.apple.coreservices.useractivityd.plist ActivityReceivingAllowed -bool no

exit 0
