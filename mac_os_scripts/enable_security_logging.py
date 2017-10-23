from common import CLITieIn


class SecurityLoggingEnabler(CLITieIn):
    def enable_security_logging(self):
        command = 'launchctl load -w /System/Library/LaunchDaemons/com.apple.auditd.plist'
        command_output = self.sudo_command(command)

        if command_output.stdout is None:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def run(self):
        return self.enable_security_logging()


if __name__ == '__main__':
    from sys import argv

    try:
        sudo_password = argv[1]
    except:
        sudo_password = None

    actor = SecurityLoggingEnabler(
        sudo_password=sudo_password,
    )

    actor.run()
