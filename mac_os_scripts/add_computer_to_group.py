"""

This script is responsible for adding a computer to a group via LDAP

Commands used:

- (in /tmp/register.ldif)
    - dn: CN=(new group),OU=(group),OU=(sub-group),DC=(www),DC=(domain),DC=(com),DC=(au) > /tmp/register.ldif
    - changetype: modify >> /tmp/register.ldif
    - add: member >> /tmp/register.ldif
    - member: CN=(computer name),OU=(old group),OU=(old sub-group),DC=(www),DC=(domain),DC=(com),DC=(au) >> /tmp/register.ldif
- ldapmodify -H ldap://www.domain.com -f /usr/local/zetta/register.ldif -D (username) -w (password) -x -c -v

"""

from common import CLITieIn


class ComputerToGroupAdder(CLITieIn):
    def build_register_ldif(self, source_ou_path, destination_ou_path):

        data = (
            'dn: {0}\n'
            'changetype: modify\n'
            'add: member\n'
            'member: {1}\n'
        ).format(
            source_ou_path,
            destination_ou_path,
        )

        try:
            self.write_file('/tmp/register.ldif', data)
        except:
            return False

        return True

    def add_computer_to_group(self, fqdn, domain_username, domain_password):
        command = 'ldapmodify -H ldap://{0} -f /tmp/register.ldif -D {1} -w {2} -x -c -v'.format(
            fqdn, domain_username, domain_password
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

    def run(self, source_ou_path, destination_ou_path, fqdn, domain_username, domain_password):
        if not self.build_register_ldif(source_ou_path, destination_ou_path):
            self._logger.error(
                'failed build_register_ldif with source_ou_path={0}, destination_ou_path={1}; cannot continue'.format(
                    repr(source_ou_path),
                    repr(destination_ou_path),
                )
            )
            return False

        if not self.add_computer_to_group(fqdn, domain_username, domain_password):
            self._logger.error(
                'failed register_computer_account with fqdn={0}, domain_username={1}, domain_password={2}; cannot continue'.format(
                    repr(fqdn),
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
        '-s',
        '--source-ou-path',
        type=str,
        required=True,
        help='OU path to source object'
    )

    parser.add_argument(
        '-d',
        '--destination-ou-path',
        type=str,
        required=True,
        help='OU path to destination object'
    )

    parser.add_argument(
        '-f',
        '--fqdn',
        type=str,
        required=True,
        help='fully qualified domain name'
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

    actor = ComputerToGroupAdder(
        sudo_password=args.sudo_password,
    )

    actor.run(
        source_ou_path=args.source_ou_path,
        destination_ou_path=args.destination_ou_path,
        fqdn=args.fqdn,
        domain_username=args.domain_username,
        domain_password=args.domain_password,
    )
