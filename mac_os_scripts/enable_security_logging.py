from common import CLITieIn


class SecurityLoggingEnabler(CLITieIn):
    def enable_security_logging(self):
        command = 'launchctl load -w /System/Library/LaunchDaemons/com.apple.auditd.plist'
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
        if not self.enable_security_logging():
            self._logger.error('failed enable_security_logging; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    args = get_args(parser)

    actor = SecurityLoggingEnabler(
        sudo_password=args.sudo_password,
    )

    actor.run()
