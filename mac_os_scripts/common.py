from utils import get_username, get_logger, run_command, read_file, write_file


class CLITieIn(object):
    def __init__(self, sudo_password=None):
        self._logger = get_logger(self.__class__.__name__)
        self._sudo_password = sudo_password

        self._logger.debug('created')

    def get_username(self):
        username = get_username()
        self._logger.debug('get_username={0}'.format(username))
        return username

    def run_command(self, command_line, quiet=True, sudo_password_override=None):
        sudo_password = self._sudo_password
        if sudo_password_override is False:
            sudo_password = None
        elif sudo_password_override is not None:
            sudo_password = sudo_password_override

        if sudo_password is not None:
            command_line = 'echo "{0}" | sudo -S {1}'.format(sudo_password, command_line)

        log_prefix = 'run_command(command_line={0}, quiet={1})'.format(
            repr(command_line), quiet
        )

        self._logger.debug('{0} invoking'.format(log_prefix))

        command_output = run_command(
            command_line=command_line,
            quiet=quiet
        )
        self._logger.debug('{0} returned {1}'.format(
            log_prefix, command_output
        ))

        return command_output

    def command(self, command_line, quiet=True):
        self._logger.debug('command invoked')
        return self.run_command(
            command_line=command_line,
            quiet=quiet,
            sudo_password_override=False,
        )

    def sudo_command(self, command_line, quiet=True, sudo_password_override=None):
        self._logger.debug('sudo_command invoked')
        return self.run_command(
            command_line=command_line,
            quiet=quiet,
            sudo_password_override=sudo_password_override,
        )

    def read_file(self, path):
        self._logger.debug('reading file from {0}'.format(repr(path)))
        data = read_file(path)
        self._logger.debug('read {0} bytes'.format(len(data)))
        return data

    def write_file(self, path, data):
        self._logger.debug('writing file to {0}'.format(repr(path)))
        result = write_file(path, data)
        self._logger.debug('wrote {0} bytes'.format(len(data)))
        return result
