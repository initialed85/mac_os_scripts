"""

This script is responsible for setting the logo for the current user (needs sudo)

Commands used:

- dscl . delete /Users/(username) Picture
- dscl . create /Users/(username) Picture "(new user logo path)"

"""

from common import CLITieIn


class LocalUserAccountLogoSetter(CLITieIn):
    def delete_user_account_logo(self):
        command = 'dscl . delete /Users/{0} Picture'.format(
            self.get_username()
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

    def create_user_account_logo(self, logo_path):
        command = 'dscl . create /Users/{0} Picture "{1}"'.format(
            self.get_username(), logo_path
        )
        command_output = self.sudo_command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def run(self, logo_path):
        if not self.delete_user_account_logo():
            self._logger.error('failed delete_user_account_logo ; cannot continue')
            return False

        if not self.create_user_account_logo(logo_path):
            self._logger.error('failed create_user_account_logo with logo_path={0}; cannot continue'.format(
                logo_path
            ))
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    parser.add_argument(
        '-l',
        '--logo-path',
        type=str,
        required=True,
        help='path for background file to use'
    )

    args = get_args(parser)

    actor = LocalUserAccountLogoSetter(
        sudo_password=args.sudo_password,
    )

    actor.run(
        logo_path=args.logo_path
    )
