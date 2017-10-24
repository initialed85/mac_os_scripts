from common import CLITieIn


class HandoffDisabler(CLITieIn):
    def disable_handoff(self):
        command = '/usr/local/zetta/mac_os_scripts/shell_scripts/disable_handoff.sh'
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
        if not self.disable_handoff():
            self._logger.error('failed disable_handoff; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from sys import argv

    try:
        sudo_password = argv[1]
    except:
        sudo_password = None

    actor = HandoffDisabler(
        sudo_password=sudo_password,
    )

    actor.run()