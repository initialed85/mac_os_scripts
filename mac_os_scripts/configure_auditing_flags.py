"""

This script is responsible for configuring the security auditing flags

Commands used:

- (in /etc/security/audit_control)
    - (line that starts with "flags:")
        - (replace with "flags:lo,ad,fd,fm,-all")

"""

import traceback

from common import CLITieIn


class AuditingFlagsConfigurator(CLITieIn):
    def modify_security_auditing_flags(self):
        try:
            data = self.read_file('/etc/security/audit_control').strip()

            output = ''

            for line in data.split('\n'):

                if line.startswith('flags:'):
                    output += 'flags:lo,ad,fd,fm,-all\n'
                else:
                    output += line + '\n'

            self.write_file('/etc/security/audit_control', output)
        except:
            self._logger.error(traceback.format_exc())
            return False

        return True

    def run(self):
        if not self.modify_security_auditing_flags():
            self._logger.error('failed modify_firewall_config; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    args = get_args(parser)

    actor = AuditingFlagsConfigurator(
        sudo_password=args.sudo_password,
    )

    result = actor.run()

    if result != 0:
        exit(1)

    exit(0)
