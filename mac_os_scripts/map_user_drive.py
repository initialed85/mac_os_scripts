import os

from common import CLITieIn


class UserDriveMapper(CLITieIn):
    def create_user_drive_folder(self, username):
        command = 'mkdir /Volumes/{0}'.format(username)
        command_output = self.sudo_command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def change_user_drive_folder_permission(self, username):
        command = 'chown {0} /Volumes/{0}'.format(username)
        command_output = self.sudo_command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def map_user_drive(self, username, server, share, domain=None, password=None):
        command = 'mount_smbfs -N "//{0}{1}{2}@{3}/{4}" /Volumes/{1}'.format(
            '{0};'.format(domain) if domain is not None else '',
            username,
            ':{0}'.format(password) if password is not None else '',
            server,
            share,
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

    def run(self, username, server, share, domain, password):
        if not self.create_user_drive_folder(username):
            self._logger.error('failed create_user_drive_folder; continuing anyway')

        if not self.change_user_drive_folder_permission(username):
            self._logger.error('failed change_user_drive_folder_permission; continuing anyway')

        if not self.map_user_drive(
                username=username,
                server=server,
                share=share,
                domain=domain,
                password=password
        ):
            self._logger.error('failed enable_security_logging; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from sys import argv

    try:
        username = os.environ['USER']
    except:
        raise Exception('unable to get USER environment variable; cannot continue')

    try:
        sudo_password = argv[1]
    except:
        raise Exception('arg 1 (sudo_password) missing; cannot continue')

    try:
        server = argv[2]
    except:
        raise Exception('arg 2 (server) missing; cannot continue')

    try:
        share = argv[3]
    except:
        raise Exception('arg 3 (share) missing; cannot continue')

    try:
        domain = argv[4]
    except:
        domain = None

    try:
        password = argv[5]
    except:
        password = None

    actor = UserDriveMapper(
        sudo_password=sudo_password,
    )

    actor.run(
        username=username,
        password=password,
        server=server,
        share=share,
        domain=domain,
    )
