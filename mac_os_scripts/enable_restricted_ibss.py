"""

This script is responsible for enabling restricted IBSS (ad-hoc/computer-to-computer wireless networking)

Commands used:

- /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport prefs RequireAdminIBSS=YES

"""

from common import CLITieIn


class RestrictedIBSSEnabler(CLITieIn):
    def enable_restricted_ibss(self):
        command = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport prefs RequireAdminIBSS=YES'
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
        if not self.enable_restricted_ibss():
            self._logger.error('failed disable_airdrop; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    args = get_args(parser)

    actor = RestrictedIBSSEnabler(
        sudo_password=args.sudo_password,
    )

    result = actor.run()

    if not result:
        exit(1)

    exit(0)
