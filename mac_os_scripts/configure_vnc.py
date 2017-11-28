"""

This script is responsible for configuring VNC

Commands used:

- /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -activate -configure -access -on -clientopts -setvnclegacy -vnclegacy yes -clientopts -setvncpw -vncpw (password) -restart -agent -privs -all
"""

from common import CLITieIn


class VNCConfigurator(CLITieIn):
    def enable_vnc_and_set_password(self, password):
        
        command = '/System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -activate -configure -access -on -clientopts -setvnclegacy -vnclegacy yes -clientopts -setvncpw -vncpw \'{0}\' -restart -agent -privs -all'.format(
            password
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

    def run(self, password):
        if not self.enable_vnc_and_set_password(password):
            self._logger.error('failed enable_vnc_and_set_password; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    parser.add_argument(
        '-v',
        '--vnc-password',
        type=str,
        required=True,
        help='VNC password to set'
    )

    args = get_args(parser)

    actor = VNCConfigurator(
        sudo_password=args.sudo_password,
    )

    actor.run(
        password=args.vnc_password
    )
