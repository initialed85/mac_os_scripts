"""

This script is responsible for disabling core dumps

Commands used:

- sysctl kern.coredump=0

"""

from common import CLITieIn


class CoreDumpDisabler(CLITieIn):
    def disable_core_dump(self):
        command = 'sysctl kern.coredump=0'
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
        if not self.disable_core_dump():
            self._logger.error('failed disable_airdrop; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    args = get_args(parser)

    actor = CoreDumpDisabler(
        sudo_password=args.sudo_password,
    )

    actor.run()
