"""

This script is responsible for enabling NTP and setting the NTP server

Commands used:

- defaults write /var/root/Library/Preferences/com.apple.loginwindow EnableMCXLoginScripts TRUE
- defaults write var/root/Library/Preferences/com.apple.loginwindow MCXScriptTrust -string (trust level)

"""

from common import CLITieIn


class NTPConfigurator(CLITieIn):
    def enable_ntp(self):
        command = 'systemsetup -setusingnetworktime on'
        command_output = self.sudo_command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def set_ntp_server(self, server):
        command = 'systemsetup -setnetworktimeserver {0}'.format(server)
        command_output = self.sudo_command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def run(self, server):
        if not self.enable_ntp():
            self._logger.error('failed enable_ntp; cannot continue')
            return False

        if not self.set_ntp_server(server):
            self._logger.error('failed set_ntp_server; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    parser.add_argument(
        '-s',
        '--server',
        type=str,
        required=True,
        help='NTP server to use'
    )

    args = get_args(parser)

    actor = NTPConfigurator(
        sudo_password=args.sudo_password,
    )

    actor.run(
        server=args.server,
    )
