"""

This script is responsible for disabling core dumps

Commands used:

- /usr/local/zetta/mac_os_scripts/external/gfxCardStatus.app/Contents/MacOS/gfxCardStatus --discrete

"""

from common import CLITieIn


class DiscreteGraphicsEnabler(CLITieIn):
    def enable_discrete_graphics(self):
        command = '/usr/local/zetta/mac_os_scripts/external/gfxCardStatus.app/Contents/MacOS/gfxCardStatus --discrete'
        command_output = self.command(command, timeout=5)

        if command_output.error_level != -9:  # -9 because we killed it after 5 seconds
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def run(self):
        if not self.enable_discrete_graphics():
            self._logger.error('failed enable_discrete_graphics; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    args = get_args(parser)

    actor = DiscreteGraphicsEnabler(
        sudo_password=args.sudo_password,
    )

    actor.run()
