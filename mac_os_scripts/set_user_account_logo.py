"""

This script is responsible for setting the logo for the current user

Commands used:

- dscl . delete /Users/(username) JPEGPhoto
- dscl . delete /Users/(username) Picture
- dscl . create /Users/(username) Picture "(new user logo path)"

"""

from common import CLITieIn


class LocalUserAccountLogoSetter(CLITieIn):
    def delete_user_account_logo_jpeg(self, username):
        command = '/usr/bin/dscl . delete /Users/{0} JPEGPhoto'.format(
            username
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

    def delete_user_account_logo(self, username):
        command = '/usr/bin/dscl . delete /Users/{0} Picture'.format(
            username
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

    def create_user_account_logo(self, username, logo_path):
        command = '/usr/bin/dscl . create /Users/{0} Picture "{1}"'.format(
            username, logo_path
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

    def run(self, username, logo_path):
        if not self.delete_user_account_logo_jpeg(username):
            self._logger.error('failed delete_user_account_logo with username={0}; cannot continue'.format(
                username
            ))
            return False

        if not self.delete_user_account_logo(username):
            self._logger.error('failed delete_user_account_logo with username={0}; cannot continue'.format(
                username
            ))
            return False

        if not self.create_user_account_logo(username, logo_path):
            self._logger.error(
                'failed create_user_account_logo with username={0}, logo_path={1}; cannot continue'.format(
                    username, logo_path
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
        '--username',
        type=str,
        required=True,
        help='user to set logo for'
    )

    parser.add_argument(
        '-l',
        '--logo-path',
        type=str,
        required=True,
        help='path for user account logo file to use (normally .tif)'
    )

    args = get_args(parser)

    actor = LocalUserAccountLogoSetter(
        sudo_password=args.sudo_password,
    )

    result = actor.run(
        username=args.username,
        logo_path=args.logo_path
    )

    if not result:
        exit(1)

    exit(0)
