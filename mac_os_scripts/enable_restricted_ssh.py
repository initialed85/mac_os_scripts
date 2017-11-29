"""

This script is responsible for enabling scripts to be run at logon time

Commands used:

- systemsetup -setremotelogin on
- (in /etc/pf.conf)
    - pass in quick inet proto tcp from (host) to any port 22
    - block drop in quick inet proto tcp from any to any port 22
- pfctl -d
- pfctl -F all
- pfctl -f /etc/pf.conf -e

"""

from common import CLITieIn


class RestrictedSSHEnabler(CLITieIn):
    def set_remote_login_on(self):
        command = '/usr/sbin/systemsetup -setremotelogin on'
        command_output = self.command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def modify_firewall_config(self, allowed_hosts):
        try:
            data = self.read_file('/etc/pf.conf').split('# !!!! added by Zetta')[0].strip()

            data += (
                '\n\n# !!!! added by Zetta (WARNING: place any other rules above this line)\n'
                '\n'
                '# permit SSH for certain hosts\n'
            )

            for host in [x.strip() for x in allowed_hosts.split(',')]:
                data += 'pass in quick inet proto tcp from {0} to any port 22\n'.format(
                    host
                )

            data += (
                '\n'
                '# drop SSH for all other hosts\n'
                'block drop in quick inet proto tcp from any to any port 22\n'
            )

            data = data.replace('\r', '')

            self.write_file('/etc/pf.conf', data)
        except:
            return False

        return True

    def restart_firewall(self):
        commands = [
            '/sbin/pfctl -d',
            '/sbin/pfctl -F all',
            '/sbin/pfctl -f /etc/pf.conf -e',
        ]
        failed = False
        for command in commands:
            command_output = self.command(command)

            if command_output.error_level != 0:
                self._logger.error(
                    '{0} failed stating {1}'.format(
                        command, command_output
                    )
                )
                failed = True

        return not failed

    def run(self, allowed_hosts):
        if not self.set_remote_login_on():
            self._logger.error('failed change_background; cannot continue')
            return False

        # if not self.modify_firewall_config(allowed_hosts):
        #     self._logger.error('failed modify_firewall_config; cannot continue')
        #     return False

        # if not self.restart_firewall():
        #     self._logger.error('failed restart_firewall; cannot continue')
        #     return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    parser.add_argument(
        '-a',
        '--allowed-hosts',
        type=str,
        required=True,
        help='comma-separated list of hosts to allow SSH (e.g. 192.168.1.1, 192.168.1.2)'
    )

    args = get_args(parser)

    actor = RestrictedSSHEnabler(
        sudo_password=args.sudo_password,
    )

    result = actor.run(
        allowed_hosts=args.allowed_hosts,
    )

    if not result:
        exit(1)

    exit(0)
