"""

This script is responsible for mapping the user's shared drive

Commands used:

- ping -c 4 -W 1000 -t 5 (file server)
- open "smb://(file server)/(user share)/(user)

"""

import os

from common import CLITieIn


class UserDriveMapper(CLITieIn):
    def ping_hostname(self, hostname):
        command = 'ping -c 4 -W 1000 -t 5 {0}"'.format(
            hostname,
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

    def map_user_drive(self, hostname, share, username):
        command = 'open "smb://{0}/{1}/{2}"'.format(
            hostname, share, username
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

    def run(self, hostname, share, username):
        if not self.ping_hostname(hostname=hostname):
            self._logger.error('failed to ping {0}; cannot continue mapping user drive'.format(hostname))
            return False

        if not self.map_user_drive(
                hostname=hostname,
                share=share,
                username=username,
        ):
            self._logger.error('failed enable_security_logging; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    parser.add_argument(
        '-f',
        '--fqdn',
        type=str,
        required=True,
        help='FQDN of server (or hostname or IP)'
    )

    parser.add_argument(
        '-s',
        '--share',
        type=str,
        required=True,
        help='base share name (will be suffixed with /(logged on username)'
    )

    args = get_args(parser)

    try:
        username = os.environ['USER']
    except:
        raise Exception('unable to get USER environment variable; cannot continue')

    actor = UserDriveMapper(
        sudo_password=args.sudo_password,
    )

    actor.run(
        hostname=args.fqdn,
        share=args.share,
        username=username,
    )
