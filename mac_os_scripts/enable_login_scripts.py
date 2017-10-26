from common import CLITieIn


class LoginScriptEnabler(CLITieIn):
    def __init__(self, trust_level, *args, **kwargs):
        super(LoginScriptEnabler, self).__init__(*args, **kwargs)

        self._trust_level = trust_level

    def enable_mcx_login_scripts(self):
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

    def set_mcx_script_trust(self, value):
        """

        :param value: string FullTrust, PartialTrust or Anonymous
        :return:
        """
        command = 'defaults write var/root/Library/Preferences/com.apple.loginwindow MCXScriptTrust -string {0}'.format(
            value
        )
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
        trust_level=args.trust_level,
    )

    actor.run()
