"""

This script is responsible for setting the root password and then disabling the root user

Commands used:

- dscl . -passwd /Users/root (root password)
- dsenableroot -d -u (admin username) -p (admin password) -r (root password)

"""

from common import CLITieIn


class RootUserConfigurator(CLITieIn):
    def set_root_password(self, root_password):
        command = 'dscl . -passwd /Users/root \'{0}\''.format(root_password)
        command_output = self.command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def disable_root_user(self, admin_username, admin_password, root_password):
        command = 'dsenableroot -d -u \'{0}\' -p \'{1}\' -r \'{2}\''.format(
            admin_username, admin_password, root_password
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

    def run(self, admin_username, admin_password, root_password):
        if not self.set_root_password(root_password):
            self._logger.error(
                'failed set_root_password with root_password={0}; cannot continue'.format(
                    root_password
                )
            )
            return False

        if not self.disable_root_user(admin_username, admin_password, root_password):
            self._logger.error(
                'failed disable_root_user with admin_username={0} admin_password={1} root_password={2}; cannot continue'.format(
                    admin_username, admin_password, root_password
                )
            )
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    parser.add_argument(
        '-u',
        '--admin-username',
        type=str,
        required=True,
        help='admin username'
    )

    parser.add_argument(
        '-p',
        '--admin-password',
        type=str,
        required=True,
        help='admin password'
    )

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
        admin_username=args.admin_username,
        admin_password=args.admin_password,
        root_password=args.root_password,
    )
