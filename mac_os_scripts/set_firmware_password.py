"""

This script is responsible for setting the firmware password

Commands used:

- expect -d -f /usr/local/zetta/mac_os_scripts/external/set_firmware_password_expect
set password [lindex $argv 0];

spawn firmwarepasswd -setpasswd -setmode command

expect {

        "Enter new password:" {
                send "$password\r"
                exp_continue
        }

        "Re-enter new password:" {
                send "$password\r"
                exp_continue
        }
}
"""

from common import CLITieIn


class FirmwarePasswordSetter(CLITieIn):
    def set_firmware_password(self, password):
        command = 'expect -d -f /usr/local/zetta/mac_os_scripts/external/set_firmware_password.expect \'{0}\''.format(password)
        command_output = self.command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def run(self, password):
        if not self.set_firmware_password(password):
            self._logger.error('failed set_firmware_password; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    parser.add_argument(
        '-f',
        '--firmware-password',
        type=str,
        required=True,
        help='firmware password to set'
    )

    args = get_args(parser)

    actor = FirmwarePasswordSetter(
        sudo_password=args.sudo_password,
    )

    actor.run(
        password=args.firmware_password
    )
