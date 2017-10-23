from utils import get_logger, run_command


class CLITieIn(object):
    def __init__(self, sudo_password=None):
        self._logger = get_logger(self.__class__.__name__)
        self._sudo_password = sudo_password

        self._logger.debug('created')

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
        return self.run_command(
            command_line=command_line,
            quiet=quiet,
            sudo_password_override=False,
        )

    def sudo_command(self, command_line, quiet=True, sudo_password_override=None):
        return self.run_command(
            command_line=command_line,
            quiet=quiet,
            sudo_password_override=sudo_password_override,
        )
