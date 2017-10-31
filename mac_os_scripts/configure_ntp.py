"""

This script is responsible for the enabling scripts to be run at logon time

Commands used:

- defaults write /var/root/Library/Preferences/com.apple.loginwindow EnableMCXLoginScripts TRUE
- defaults write var/root/Library/Preferences/com.apple.loginwindow MCXScriptTrust -string (trust level)

"""

from common import CLITieIn


class NTPConfigurator(CLITieIn):
    def set_ntp_time(self):
        command = 'defaults write /var/root/Library/Preferences/com.apple.loginwindow EnableMCXLoginScripts TRUE'
        command_output = self.sudo_command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def run(self):
        if not self.enable_mcx_login_scripts():
            self._logger.error('failed enable_mcx_login_scripts; cannot continue')
            return False

        if not self.set_mcx_script_trust(self._trust_level):
            self._logger.error('failed set_mcx_script_trust with trust_level {0}; cannot continue'.format(
                repr(self._trust_level)
            ))
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    args = get_args(parser)

    actor = NTPConfigurator(
        sudo_password=args.sudo_password,
    )

    actor.run()
