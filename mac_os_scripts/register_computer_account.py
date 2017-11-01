"""

This script is responsible for registering a computer account on the domain for the current machine

Commands used:

- (in /tmp/register.ldif)
    - dn: CN=(computer group),OU=(group),OU=(sub-group),DC=(www),DC=(domain),DC=(com),DC=(au) > /tmp/register.ldif
    - changetype: modify >> /tmp/register.ldif
    - add: member >> /tmp/register.ldif
    - member: CN=(computer name),OU=(group),OU=(sub-group),DC=(www),DC=(domain),DC=(com),DC=(au) >> /tmp/register.ldif
- ldapmodify -H ldap://www.domain.com -f /usr/local/zetta/register.ldif -D (username) -w (password) -x -c -v

"""

from common import CLITieIn


class ComputerAccountRegisterer(CLITieIn):
    def build_register_ldif(self, computer_group, ou_path, dc_path, computer_name):

        ou_path_formatted = ','.join([
            'OU={0}'.format(x) for x in ou_path.split('.')
        ])

        dc_path_formatted = ','.join([
            'DC={0}'.format(x) for x in dc_path.split('.')
        ])

        data = (
            'dn: CN={computer_group},{ou_path_formatted},{dc_path_formatted}\n'
            'changetype: modify\n'
            'add: member\n'
            'member: CN={computer_name},{ou_path_formatted},{dc_path_formatted}\n'
        ).format(
            computer_group=computer_group,
            ou_path_formatted=ou_path_formatted,
            dc_path_formatted=dc_path_formatted,
            computer_name=computer_name
        )

        try:
            self.write_file('/tmp/register.ldif', data)
        except:
            return False

        return True

    def register_computer_account(self, dc_path, domain_username, domain_password):
        command = 'ldapmodify -H ldap://{0} -f /tmp/register.ldif -D {1} -w {2} -x -c -v'.format(
            dc_path, domain_username, domain_password
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

    def run(self, computer_group, ou_path, dc_path, computer_name, domain_username, domain_password):
        if not self.build_register_ldif(computer_group, ou_path, dc_path, computer_name):
            self._logger.error(
                'failed build_register_ldif with computer_group={0}, ou_path={1}, dc_path={2}, computer_name={3}; cannot continue'.format(
                    repr(computer_group),
                    repr(ou_path),
                    repr(dc_path),
                    repr(computer_name),
                )
            )
            return False

        if not self.register_computer_account(dc_path, domain_username, domain_password):
            self._logger.error(
                'failed register_computer_account with dc_path={0}, domain_username={1}, domain_password={2}; cannot continue'.format(
                    repr(dc_path),
                    repr(domain_username),
                    repr(domain_password),
                )
            )
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    parser.add_argument(
        '-g',
        '--computer-group',
        type=str,
        required=True,
        help='group that contains the computer accounts'
    )

    parser.add_argument(
        '-o',
        '--ou-path',
        type=str,
        required=True,
        help='OU path in dotted format (e.g. users.developers.senior)'
    )

    parser.add_argument(
        '-d',
        '--dc-path',
        type=str,
        required=True,
        help='DC path in dotted format (e.g. customer.domain.com.au)'
    )

    parser.add_argument(
        '-c',
        '--computer-name',
        type=str,
        required=True,
        help='computer name to register'
    )

    parser.add_argument(
        '-u',
        '--domain-username',
        type=str,
        required=True,
        help='domain username to authenticate with'
    )

    parser.add_argument(
        '-p',
        '--domain-password',
        type=str,
        required=True,
        help='domain password to authenticate with'
    )

    args = get_args(parser)

    actor = ComputerAccountRegisterer(
        sudo_password=args.sudo_password,
    )

    actor.run(
        computer_group=args.computer_group,
        ou_path=args.ou_path,
        dc_path=args.dc_path,
        domain_username=args.domain_username,
        domain_password=args.domain_password,
        computer_name=args.computer_name,
    )
