"""

This script is responsible for disabling AirDrop

Commands used:

- defaults write com.apple.NetworkBrowser DisableAirDrop -bool YES
- pkill -9 -f Finder.app

"""

from common import CLITieIn


class AirDropDisabler(CLITieIn):
    def disable_airdrop(self):
        command = '/usr/bin/defaults write com.apple.NetworkBrowser DisableAirDrop -bool YES'
        command_output = self.command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def restart_finder(self):
        command = '/usr/bin/pkill -9 -f Finder.app'
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
        if not self.disable_airdrop():
            self._logger.error('failed disable_airdrop; cannot continue')
            return False

        if not self.restart_finder():
            self._logger.error('failed restart_finder; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    args = get_args(parser)

    actor = AirDropDisabler(
        sudo_password=args.sudo_password,
    )

    result = actor.run()

    if not result:
        exit(1)

    exit(0)
