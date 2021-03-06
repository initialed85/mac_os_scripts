"""

This script is responsible for enabling scripts to be run at logon time

Commands used:

- defaults write /var/root/Library/Preferences/com.apple.loginwindow EnableMCXLoginScripts TRUE
- defaults write var/root/Library/Preferences/com.apple.loginwindow MCXScriptTrust -string (trust level)

"""

from common import CLITieIn


class LoginScriptEnabler(CLITieIn):
    def enable_mcx_login_scripts(self):
        command = '/usr/bin/defaults write /var/root/Library/Preferences/com.apple.loginwindow EnableMCXLoginScripts TRUE'
        command_output = self.command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def set_mcx_script_trust(self, trust_level):
        """

        :param value: string FullTrust, PartialTrust or Anonymous
        :return:
        """
        command = '/usr/bin/defaults write var/root/Library/Preferences/com.apple.loginwindow MCXScriptTrust -string \'{0}\''.format(
            trust_level
        )
        command_output = self.command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def run(self, trust_level):
        if not self.enable_mcx_login_scripts():
            self._logger.error('failed enable_mcx_login_scripts; cannot continue')
            return False

        if not self.set_mcx_script_trust(trust_level):
            self._logger.error('failed set_mcx_script_trust with trust_level {0}; cannot continue'.format(
                repr(trust_level)
            ))
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    parser.add_argument(
        '-t',
        '--trust-level',
        type=str,
        required=True,
        help='trust level to use (FullTrust, PartialTrust or Anonymous)'
    )

    args = get_args(parser)

    actor = LoginScriptEnabler(
        sudo_password=args.sudo_password,
    )

    result = actor.run(
        trust_level=args.trust_level,
    )

    if not result:
        exit(1)

    exit(0)
