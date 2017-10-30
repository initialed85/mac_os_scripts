from common import CLITieIn


class BackgroundChanger(CLITieIn):
    def change_background(self, background_path):
        command = '/usr/bin/osascript /usr/local/zetta/mac_os_scripts/shell_scripts/change_background.scpt {0}'.format(
            background_path
        )
        command_output = self.command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def run(self, background_path):
        if not self.change_background(background_path):
            self._logger.error('failed change_background; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    parser.add_argument(
        '-b',
        '--background-path',
        type=str,
        required=True,
        help='path for background file to use'
    )

    args = get_args(parser)

    actor = BackgroundChanger(
        sudo_password=args.sudo_password,
    )

    actor.run(
        background_path=args.background_path
    )
