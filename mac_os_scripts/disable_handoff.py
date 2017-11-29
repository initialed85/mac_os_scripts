"""

This script is responsible for disabling Handoff

Commands used:

-  /usr/local/zetta/mac_os_scripts/external/disable_handoff.sh

Scripts referenced:

- disable_handoff.sh
#!/bin/bash

hardware_uuid=$(/usr/sbin/system_profiler SPHardwareDataType | grep "Hardware UUID" | cut -d ':' -f 2 | xargs)
current_user=$USER

echo "hardware_uuid: $hardware_uuid"
echo "current_user: $current_user"

echo "fixing"
defaults write /Users/$current_user/Library/Preferences/ByHost/com.apple.coreservices.lsuseractivityd.$hardware_uuid.plist ActivityAdvertisingAllowed -bool NO
defaults write /Users/$current_user/Library/Preferences/ByHost/com.apple.coreservices.lsuseractivityd.$hardware_uuid.plist ActivityReceivingAllowed -bool NO
defaults write /Users/$current_user/Library/Preferences/com.apple.coreservices.lsuseractivityd.plist ActivityAdvertisingAllowed -bool NO
defaults write /Users/$current_user/Library/Preferences/com.apple.coreservices.lsuseractivityd.plist ActivityReceivingAllowed -bool NO

defaults write /Users/$current_user/Library/Preferences/ByHost/com.apple.coreservices.useractivityd.$hardware_uuid.plist ActivityAdvertisingAllowed -bool NO
defaults write /Users/$current_user/Library/Preferences/ByHost/com.apple.coreservices.useractivityd.$hardware_uuid.plist ActivityReceivingAllowed -bool NO
defaults write /Users/$current_user/Library/Preferences/com.apple.coreservices.useractivityd.plist ActivityAdvertisingAllowed -bool NO
defaults write /Users/$current_user/Library/Preferences/com.apple.coreservices.useractivityd.plist ActivityReceivingAllowed -bool NO

exit 0

"""

from common import CLITieIn


class HandoffDisabler(CLITieIn):
    def disable_handoff(self):
        command = '/usr/local/zetta/mac_os_scripts/external/disable_handoff.sh'
        command_output = self.command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def run(self):
        if not self.disable_handoff():
            self._logger.error('failed disable_handoff; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    args = get_args(parser)

    actor = HandoffDisabler(
        sudo_password=args.sudo_password,
    )

    result = actor.run()

    if not result:
        exit(1)

    exit(0)
