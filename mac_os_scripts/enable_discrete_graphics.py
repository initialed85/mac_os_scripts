"""

This script is responsible for enabling discrete graphics (GPU)

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

    def remove_gfxcardstatus_login_item(self):
        command = 'osascript -e \'tell application "System Events" to delete login item "gfxCardStatus"\''
        self.command(command)

        # don't check if this succeeded or failed

        return True

    def run(self):
        if not self.enable_discrete_graphics():
            self._logger.error('failed enable_discrete_graphics; cannot continue')
            return False

        self.remove_gfxcardstatus_login_item()

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    args = get_args(parser)

    actor = DiscreteGraphicsEnabler(
        sudo_password=args.sudo_password,
    )

    result = actor.run()

    if not result:
        exit(1)

    exit(0)
