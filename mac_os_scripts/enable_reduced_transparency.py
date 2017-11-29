"""

This script is responsible for enabling reduced transparency

Commands used:

- defaults write com.apple.universalaccess reduceTransparency -bool true

"""

from common import CLITieIn


class ReducedTransparencyEnabler(CLITieIn):
    def enable_reduced_transparency(self):
        command = 'defaults write com.apple.universalaccess reduceTransparency -bool true'
        command_output = self.command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def restart_dock(self):
        command = 'pkill -9 -f Dock.app'
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
        if not self.enable_reduced_transparency():
            self._logger.error('failed enable_reduced_transparency; cannot continue')
            return False

        if not self.restart_dock():
            self._logger.error('failed enable_reduced_transparency; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    args = get_args(parser)

    actor = ReducedTransparencyEnabler(
        sudo_password=args.sudo_password,
    )

    result = actor.run()

    if result != 0:
        exit(1)

    exit(0)
