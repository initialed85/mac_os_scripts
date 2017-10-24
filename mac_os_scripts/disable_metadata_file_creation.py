from common import CLITieIn


class MetadataFileCreationDisabler(CLITieIn):
    def set_ds_dont_write_network_stores(self):
        command = 'defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true'
        command_output = self.command(command)

        if command_output.stdout is None:
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

        if command_output.stdout is None:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return command_output.stdout.strip().lower() == '1'

    def run(self):
        self.set_ds_dont_write_network_stores()

        passed = self.get_ds_dont_write_network_stores()
        if not passed:
            self._logger.error('failed')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from sys import argv

    try:
        sudo_password = argv[1]
    except:
        sudo_password = None

    actor = MetadataFileCreationDisabler(
        sudo_password=sudo_password,
    )

    actor.run()
