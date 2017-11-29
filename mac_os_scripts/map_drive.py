"""

This script is responsible for mapping the a shared drive

Commands used:

- ping -c 4 -W 1000 -t 5 (file server)
- open "smb://(file server)/(share path)"

"""

from common import CLITieIn


class DriveMapper(CLITieIn):
    def ping_hostname(self, hostname):
        command = '/sbin/ping -c 4 -W 1000 -t 5 {0}'.format(
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

    def map_drive(self, hostname, share):
        command = '/usr/bin/open "smb://{0}/{1}"'.format(
            hostname, share
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

    def run(self, hostname, share):
        if not self.ping_hostname(hostname=hostname):
            self._logger.error(
                'failed to ping {0}; cannot continue mapping user drive'.format(hostname))
            return False

        if not self.map_drive(
                hostname=hostname,
                share=share,
        ):
            self._logger.error('failed map_drive; cannot continue')
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

    actor = DriveMapper(
        sudo_password=args.sudo_password,
    )

    result = actor.run(
        hostname=args.fqdn,
        share=args.share,
    )

    if not result:
        exit(1)

    exit(0)
