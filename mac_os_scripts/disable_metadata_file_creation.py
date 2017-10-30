"""

This script is responsible for the disabling the creation of .DS_Store files

Commands used:

- defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true
- defaults read com.apple.desktopservices DSDontWriteNetworkStores

"""

from common import CLITieIn


class MetadataFileCreationDisabler(CLITieIn):
    def set_ds_dont_write_network_stores(self):
        command = 'defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true'
        command_output = self.command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def get_ds_dont_write_network_stores(self):
        command = 'defaults read com.apple.desktopservices DSDontWriteNetworkStores'
        command_output = self.command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return command_output.stdout.strip().lower() == '1'

    def run(self):
        if not self.set_ds_dont_write_network_stores():
            self._logger.error('failed set_ds_dont_write_network_stores; cannot continue')
            return False

        if not self.get_ds_dont_write_network_stores():
            self._logger.error('failed get_ds_dont_write_network_stores; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    args = get_args(parser)

    actor = MetadataFileCreationDisabler(
        sudo_password=args.sudo_password,
    )

    actor.run()
