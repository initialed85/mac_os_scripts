# TODO: Remove all credentials and domain stuff; not needed
# open smb://grayfs01.grayman.com.au/homedrives$/test.test

import os

from common import CLITieIn


class UserDriveMapper(CLITieIn):
    def map_user_drive(self, server, share, username):
        command = 'open "smb://{0}/{1}/{2}"'.format(
            server, share, username
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

    def run(self, server, share, username):
        if not self.map_user_drive(
                server=server,
                share=share,
                username=username,
        ):
            self._logger.error('failed enable_security_logging; cannot continue')
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from sys import argv

    try:
        server = argv[1]
    except:
        raise Exception('arg 1 (server) missing; cannot continue')

    try:
        share = argv[2]
    except:
        raise Exception('arg 2 (share) missing; cannot continue')

    try:
        username = os.environ['USER']
    except:
        raise Exception('unable to get USER environment variable; cannot continue')

    actor = UserDriveMapper(
    )

    actor.run(
        server=server,
        share=share,
        username=username,
    )
