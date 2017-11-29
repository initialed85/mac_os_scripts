"""

This script is responsible for disabling guest connection to shared folders

Commands used:

- defaults write /Library/Preferences/SystemConfiguration/com.apple.smb.server AllowGuestAccess false

"""

from common import CLITieIn


class GuestConnectionToSharedFoldersDisabler(CLITieIn):
    def disable_guest_connection_to_shared_folders(self):
        command = 'defaults write /Library/Preferences/SystemConfiguration/com.apple.smb.server AllowGuestAccess false'
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
        if not self.disable_guest_connection_to_shared_folders():
            self._logger.error('failed disable_guest_connection_to_shared_folders; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    args = get_args(parser)

    actor = GuestConnectionToSharedFoldersDisabler(
        sudo_password=args.sudo_password,
    )

    result = actor.run()

    if not result:
        exit(1)

    exit(0)
