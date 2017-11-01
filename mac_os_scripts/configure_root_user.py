"""

This script is responsible for setting the root user password and then disabling the root user

Commands used:

- dscl . -passwd /Users/root (root password)
- dsenableroot -d

"""

from common import CLITieIn


class RootUserConfigurator(CLITieIn):
    def set_root_password(self, root_password):
        command = 'dscl . -passwd /Users/root {0}'.format(root_password)
        command_output = self.sudo_command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def disable_root_user(self):
        command = 'dsenableroot -d'
        command_output = self.sudo_command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def run(self, root_password):
        if not self.set_root_password(root_password):
            self._logger.error('failed set_root_password with root_password={0}; cannot continue'.format(
                root_password
            ))
            return False

        if not self.disable_root_user():
            self._logger.error('failed disable_root_user; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    parser.add_argument(
        '-r',
        '--root-password',
        type=str,
        required=True,
        help='root password to set'
    )

    args = get_args(parser)

    actor = RootUserConfigurator(
        sudo_password=args.sudo_password,
    )

    actor.run(
        root_password=args.root_password,
    )
